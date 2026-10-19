#pragma once

#include <array>
#include <cstdint>
#include <optional>
#include <span>
#include <string>
#include <vector>

namespace isaac {
using Address = std::uint64_t;
inline constexpr Address TitleId = 0x01009CD0167E2000ULL;
inline constexpr std::array<std::uint8_t, 8> BuildPrefix{0xBD,0xB0,0x59,0x0D,0x4B,0xA0,0x00,0x19};
inline constexpr Address EntryOffset = 0x7EE950, GlobalOffset = 0x7FB210;
inline constexpr Address GameRoomOffset = 0x21550, RoomListOffset = 0x19C8;
inline constexpr Address CodeEnd = 0x7F3000, BssEnd = 0xE509E8;
inline constexpr Address PlayerVtable = 0x7BA0A8, PedestalVtable = 0x7B9DC0;
inline constexpr std::uint32_t MaxEntities = 256; // Diagnostic bound, not a proven capacity.

struct Metadata {
    Address pid{}, title{}, main{}, mainSize{}, heap{}, heapSize{};
    std::array<std::uint8_t, 32> build{};
    bool operator==(const Metadata&) const = default;
};

// Contexts identify repeated reads in recorded fixtures. The Switch backend ignores them.
enum class Phase : std::uint8_t {
    Bootstrap, CodeBefore, RootBefore, Before, Entities, After,
    EntitiesAfter, RelevantAfter, RootAfter, CodeAfter, PillBefore, PillAfter
};
struct Context {
    Phase phase{};
    std::uint8_t view{};
    bool operator==(const Context&) const = default;
};
class Memory {
public:
    virtual ~Memory() = default;
    virtual bool metadata(Metadata& out) = 0;
    virtual bool read(Address address, std::span<std::uint8_t> out, Context context) = 0;
};

struct Entity {
    Address address{}, vtable{};
    std::uint32_t type{}, variant{}, subtype{};
    float x{}, y{};
};
struct Item {
    Address address{};
    std::uint32_t id{};
    float x{}, y{};
    // Pill IDs are appearance/color codes, NEVER effect IDs.
    std::uint32_t variant{100}; // 70 pill, 100 collectible, 300 card/rune, 350 trinket.
    // Set only from two matching current-run table reads with reveal byte 1.
    // This is the base effect; player-dependent conversions remain separate.
    std::optional<std::uint32_t> pillBaseEffect{};
};
inline constexpr bool descriptiveVariant(std::uint32_t variant) {
    return variant==70 || variant==100 || variant==300 || variant==350;
}
enum class Status { Clear, Valid, Unsupported, ReadFailure, Changed, Invalid };
enum class PickupCoverage { CollectiblesAndTrinkets, CardsAndPills };
struct Snapshot {
    Status status{Status::Clear};
    std::string reason{"In attesa"};
    Metadata process{};
    Address room{};
    std::uint32_t roomType{}, count{};
    std::vector<Entity> players;
    std::vector<Item> items;
    std::optional<Item> nearest;
    // Positions are not atomic. No verified menu/run flag exists yet.
};

// Deterministic diagnostic rule: distance, then raw ID, variant, then entity address.
// Co-op selection remains undecided: no nearest result with != 1 distinct player.
std::optional<Item> selectNearest(std::span<const Entity> players, std::span<const Item> items);
Snapshot sample(Memory& memory,PickupCoverage coverage=PickupCoverage::CardsAndPills);
const char* statusName(Status status);
} // namespace isaac
