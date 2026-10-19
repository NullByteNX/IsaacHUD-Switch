#include "isaac/core.hpp"
#include "isaac/pills.hpp"

#include <algorithm>
#include <bit>
#include <cmath>
#include <map>
#include <tuple>

namespace isaac {
namespace {
static_assert(std::endian::native == std::endian::little);
struct Failure { Status status; std::string reason; };
[[noreturn]] void reject(Status status, const char* reason) { throw Failure{status, reason}; }

bool inRange(Address p, std::size_t n, Address base, Address size) {
    return p >= base && n <= size && p - base <= size - n;
}
template<class T> T integer(std::span<const std::uint8_t> raw, std::size_t off = 0) {
    T value{};
    for (std::size_t i = 0; i < sizeof(T); ++i) value |= T(raw[off+i]) << (8*i);
    return value;
}
float floating(std::span<const std::uint8_t> raw, std::size_t off) {
    return std::bit_cast<float>(integer<std::uint32_t>(raw, off));
}
class Reader {
    Memory& memory;
public:
    Metadata meta;
    PickupCoverage coverage;
    explicit Reader(Memory& source,PickupCoverage scope) : memory(source),coverage(scope) {
        if (!memory.metadata(meta)) reject(Status::ReadFailure, "Processo non disponibile");
        if (meta.title != TitleId || !std::equal(BuildPrefix.begin(), BuildPrefix.end(), meta.build.begin()))
            reject(Status::Unsupported, "Title/Build non supportata");
        if (!meta.pid || !meta.main || !meta.heap || meta.main % 4096 || meta.heap % 4096
            || meta.mainSize < BssEnd || !meta.heapSize
            || meta.main > UINT64_MAX - meta.mainSize || meta.heap > UINT64_MAX - meta.heapSize)
            reject(Status::Invalid, "Metadati o estensioni memoria non validi");
    }
    void heapPointer(Address p, std::size_t n) const {
        if (p % 8 || !inRange(p, n, meta.heap, meta.heapSize))
            reject(Status::Invalid, "Puntatore fuori dall'heap dichiarato");
    }
    std::vector<std::uint8_t> read(Address p, std::size_t n, Context ctx) {
        if (!inRange(p,n,meta.main,meta.mainSize) && !inRange(p,n,meta.heap,meta.heapSize))
            reject(Status::Invalid, "Lettura fuori dalle estensioni dichiarate");
        std::vector<std::uint8_t> raw(n, 0);
        if (!memory.read(p, raw, ctx)) reject(Status::ReadFailure, "Lettura memoria fallita");
        return raw;
    }
    Address qword(Address p, Context ctx) { return integer<Address>(read(p,8,ctx)); }
    void checkProfile(Phase phase) {
        const auto raw = read(meta.main, 24, {Phase::Bootstrap,0});
        if (integer<std::uint32_t>(raw,4) != 8 || integer<std::uint32_t>(raw,8) != 0x30444F4D
            || integer<std::uint32_t>(raw,12) != 0x7ED910-8
            || integer<std::uint32_t>(raw,16) != CodeEnd-8
            || integer<std::uint32_t>(raw,20) != BssEnd-8)
            reject(Status::Unsupported, "MOD0 diverso dal profilo verificato");
        constexpr std::array<std::pair<Address,std::uint32_t>,16> words{{
            {0x774E0,0xF0003BA8},{0x774E4,0xF944A908},{0x774E8,0xF9400108},
            {0x774EC,0x5282AA09},{0x774F0,0x72A00049},{0x774F4,0xF8696914},
            {0x774F8,0xB959D688},{0x7752C,0xF94CE688},
            {0x79E00,0xB0003BA8},{0x79E04,0xF944A908},{0x79E08,0xF9400108},
            {0x79E0C,0x5282AA09},{0x79E10,0x72A00049},{0x79E14,0xF8696915},
            {0x79E18,0xB959D6A8},{0x79E40,0xF94CE6A8}
        }};
        for (const auto& [offset, expected] : words)
            if (integer<std::uint32_t>(read(meta.main+offset,4,{phase,0})) != expected)
                reject(Status::Unsupported, "Codice diverso dal profilo verificato");
    }
    std::array<Address,3> root(Phase phase) {
        const auto slot = qword(meta.main+EntryOffset,{phase,0});
        if (slot != meta.main+GlobalOffset) reject(Status::Invalid,"Slot globale inatteso");
        const auto game = qword(slot,{phase,0});
        heapPointer(game,GameRoomOffset+8);
        const auto room = qword(game+GameRoomOffset,{phase,0});
        heapPointer(room,0x19E0);
        return {slot,game,room};
    }
    void finish() {
        Metadata after{};
        if (!memory.metadata(after)) reject(Status::ReadFailure,"Processo non piu' disponibile");
        if (after != meta) reject(Status::Changed,"Processo o metadati cambiati");
    }
};
bool describable(const Entity& e,PickupCoverage coverage) {
    return e.type==5&&(e.variant==100||e.variant==350
        ||(coverage==PickupCoverage::CardsAndPills&&(e.variant==70||e.variant==300)));
}
bool relevant(const Entity& e,PickupCoverage coverage) { return e.type == 1 || describable(e,coverage); }
auto signature(const Entity& e) { return std::tuple{e.vtable,e.type,e.variant,e.subtype}; }
using Entities = std::map<Address,Entity>;
Entities projection(const Entities& entities,PickupCoverage coverage) {
    Entities result;
    for (const auto& [p,e] : entities) if (relevant(e,coverage)) result.emplace(p,e);
    return result;
}
bool sameIdentities(const Entities& a, const Entities& b) {
    if (a.size() != b.size()) return false;
    for (const auto& [p,e] : a) {
        const auto it = b.find(p);
        if (it == b.end() || signature(e) != signature(it->second)) return false;
    }
    return true;
}
Entity classify(Reader& reader, Address p, Context ctx) {
    reader.heapPointer(p,0x44);
    const auto raw = reader.read(p,0x44,ctx);
    Entity e{p,integer<Address>(raw),integer<std::uint32_t>(raw,0x38),
             integer<std::uint32_t>(raw,0x3C),integer<std::uint32_t>(raw,0x40),0,0};
    if (e.vtable % 8 || !inRange(e.vtable,8,reader.meta.main,CodeEnd))
        reject(Status::Invalid,"Slot contato non classificabile");
    if (e.type == 1 && e.vtable != reader.meta.main+PlayerVtable)
        reject(Status::Unsupported,"Vtable player non supportata");
    if (describable(e,reader.coverage) && e.vtable != reader.meta.main+PedestalVtable)
        reject(Status::Unsupported,"Vtable pickup non supportata");
    if (relevant(e,reader.coverage)) {
        reader.heapPointer(p,0x318);
        const auto xy = reader.read(p+0x310,8,ctx);
        e.x = floating(xy,0); e.y = floating(xy,4);
        if (!std::isfinite(e.x) || !std::isfinite(e.y)) reject(Status::Invalid,"Coordinate non finite");
    }
    return e;
}
void validateHeader(Reader& r, const std::vector<std::uint8_t>& raw) {
    r.heapPointer(integer<Address>(raw,8),8);
    const auto type = integer<std::uint32_t>(raw,0x10);
    const auto width = integer<std::uint32_t>(raw,0x14), height = integer<std::uint32_t>(raw,0x18);
    bool boundsOk = true;
    for (std::size_t off = 0x1C; off <= 0x28; off += 4) {
        const auto v = floating(raw,off);
        boundsOk &= std::isfinite(v) && v >= -2000 && v <= 4000;
    }
    if (raw[0] > 1 || raw[1] > 1 || type < 1 || type > 64
        || width < 3 || width > 128 || height < 3 || height > 128 || !boundsOk
        || floating(raw,0x24) <= floating(raw,0x1C) || floating(raw,0x28) <= floating(raw,0x20))
        reject(Status::Invalid,"Header stanza non compatibile");
}
struct List { Address array; std::uint32_t field8, count; Address field10; };
List decodeList(Reader& reader, const std::vector<std::uint8_t>& raw) {
    List list{integer<Address>(raw),integer<std::uint32_t>(raw,8),
              integer<std::uint32_t>(raw,12),integer<Address>(raw,16)};
    if (list.count < 1 || list.count > MaxEntities) reject(Status::Invalid,"Conteggio fuori dal limite diagnostico");
    reader.heapPointer(list.array,list.count*8);
    return list;
}
Entities classifyList(Reader& reader, const List& list, Context prefixCtx, Context entityCtx) {
    const auto raw = reader.read(list.array,list.count*8,prefixCtx);
    Entities result;
    for (std::uint32_t i=0;i<list.count;++i) {
        const auto p = integer<Address>(raw,i*8);
        if (!result.contains(p)) result.emplace(p,classify(reader,p,entityCtx));
    }
    return result;
}
struct View {
    std::vector<std::uint8_t> header;
    List list{};
    Entities entities;
};
View view(Reader& reader, Address room, std::uint8_t index) {
    const auto ctx = [index](Phase p) { return Context{p,index}; };
    View v;
    v.header = reader.read(room,48,ctx(Phase::Before));
    validateHeader(reader,v.header);
    v.list = decodeList(reader,reader.read(room+RoomListOffset,24,ctx(Phase::Before)));
    auto initial = classifyList(reader,v.list,ctx(Phase::Before),ctx(Phase::Entities));
    auto projected = projection(initial,reader.coverage);
    if (std::none_of(projected.begin(),projected.end(),[](const auto& pair){return pair.second.type==1;}))
        reject(Status::Invalid,"Player assente dalla lista contata");
    const auto headerAfter = reader.read(room,48,ctx(Phase::After));
    const auto listAfter = decodeList(reader,reader.read(room+RoomListOffset,24,ctx(Phase::After)));
    if (v.header != headerAfter || v.list.array != listAfter.array || v.list.field8 != listAfter.field8
        || v.list.field10 != listAfter.field10) reject(Status::Changed,"Stanza o lista cambiate durante la lettura");
    const auto finalEntities = classifyList(reader,listAfter,ctx(Phase::After),ctx(Phase::EntitiesAfter));
    if (!sameIdentities(projected,projection(finalEntities,reader.coverage)))
        reject(Status::Changed,"Player o pickup descrivibile cambiato nella lista finale");
    Entities reread;
    for (const auto& [p,e] : projected) { (void)e; reread.emplace(p,classify(reader,p,ctx(Phase::RelevantAfter))); }
    if (!sameIdentities(projected,reread)) reject(Status::Changed,"Identita' cambiata alla rilettura");
    v.entities = std::move(reread);
    v.list.count = listAfter.count;
    return v;
}
std::optional<PillTable> pillTable(Reader& reader,Address game,Phase phase) {
    // Missing optional pill data never invalidates unrelated pickup identities.
    // It only prevents publishing an effect for this current sample.
    try {
        reader.heapPointer(game,PillRevealGameOffset+PillColorCount);
        constexpr std::array<std::pair<Address,std::size_t>,4> ranges{{
            {0x3815F8,0x54},{0x3A1EA0,12},{0x2C0F6C,4},{0x2C0FAC,20}
        }};
        for(const auto& [start,size]:ranges) {
            const auto bytes=reader.read(reader.meta.main+start,size,{phase,0});
            for(const auto& [offset,expected]:PillCodeWords)
                if(offset>=start && offset-start<size
                    && integer<std::uint32_t>(bytes,offset-start)!=expected)return {};
        }
        return decodePillTable(reader.read(game+PillEffectsGameOffset,PillTableBytes,{phase,0}));
    } catch(const Failure&) {
        return {};
    }
}
} // namespace

std::optional<Item> selectNearest(std::span<const Entity> players, std::span<const Item> items) {
    if (players.empty()) return {};
    const auto& player = players[0];
    if (!std::isfinite(player.x) || !std::isfinite(player.y)) return {};
    for (const auto& other : players)
        if (other.address != player.address || other.x != player.x || other.y != player.y) return {};
    std::optional<Item> best;
    double bestDistance{};
    for (const auto& item : items) {
        if (!item.id || !descriptiveVariant(item.variant)
            || !std::isfinite(item.x) || !std::isfinite(item.y)) continue;
        const double dx = double(item.x)-player.x, dy = double(item.y)-player.y;
        const double distance = dx*dx+dy*dy;
        if (!best || std::tuple{distance,item.id,item.variant,item.address} < std::tuple{bestDistance,best->id,best->variant,best->address}) {
            best = item; bestDistance = distance;
        }
    }
    return best;
}
Snapshot sample(Memory& memory,PickupCoverage coverage) {
    try {
        Reader reader(memory,coverage);
        reader.checkProfile(Phase::CodeBefore);
        const auto rootBefore = reader.root(Phase::RootBefore);
        const auto first = view(reader,rootBefore[2],0);
        const bool hasStandardPill=std::any_of(first.entities.begin(),first.entities.end(),[](const auto& pair) {
            const auto& e=pair.second;
            return e.type==5 && e.variant==70 && standardPillColor(e.subtype);
        });
        const auto pillBefore=hasStandardPill?pillTable(reader,rootBefore[1],Phase::PillBefore):std::nullopt;
        const auto second = view(reader,rootBefore[2],1);
        if (first.header != second.header || first.list.array != second.list.array
            || first.list.field8 != second.list.field8 || first.list.field10 != second.list.field10
            || !sameIdentities(first.entities,second.entities))
            reject(Status::Changed,"Le due viste della stanza non concordano");
        const auto pillAfter=hasStandardPill?pillTable(reader,rootBefore[1],Phase::PillAfter):std::nullopt;
        if (reader.root(Phase::RootAfter) != rootBefore) reject(Status::Changed,"Catena della stanza cambiata");
        reader.checkProfile(Phase::CodeAfter);
        reader.finish();
        Snapshot result;
        result.status = Status::Valid;
        result.reason = "Dati coerenti; stato menu non verificato";
        result.process = reader.meta; result.room = rootBefore[2];
        result.roomType = integer<std::uint32_t>(second.header,0x10); result.count = second.list.count;
        for (const auto& [p,e] : second.entities) {
            if (e.type == 1) result.players.push_back(e);
            else if (e.subtype) {
                Item item{p,e.subtype,e.x,e.y,e.variant};
                if(e.variant==70 && pillBefore && pillAfter && *pillBefore==*pillAfter)
                    item.pillBaseEffect=revealedBaseEffect(*pillAfter,e.subtype);
                result.items.push_back(std::move(item));
            }
        }
        result.nearest = selectNearest(result.players,result.items);
        return result;
    } catch (const Failure& failure) {
        Snapshot cleared; // Never publish previous good items after any failure.
        cleared.status = failure.status; cleared.reason = failure.reason;
        return cleared;
    }
}
const char* statusName(Status status) {
    switch (status) {
        case Status::Valid:return "VALID";
        case Status::Unsupported:return "UNSUPPORTED";
        case Status::ReadFailure:return "READ_FAILED";
        case Status::Changed:return "CHANGED";
        case Status::Invalid:return "INVALID";
        default:return "CLEAR";
    }
}
} // namespace isaac
