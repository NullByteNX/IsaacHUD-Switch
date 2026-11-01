#pragma once
// Runtime readers only: no names, descriptions or quality table are compiled in.
#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <fstream>
#include <istream>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

namespace isaac {
inline constexpr char RuntimeCatalogPath[]="sdmc:/switch/IsaacHUD/catalog_it.tsv";
inline constexpr char RuntimeQualityPath[]="sdmc:/switch/IsaacHUD/collectible_quality.tsv";
struct Description {std::uint32_t variant,id;std::string name,text;};
struct PillDescription {std::uint32_t effect;std::string name,text,horse;};
struct CollectibleQuality {std::uint32_t id;std::uint8_t quality;};
inline std::vector<Description> Descriptions;
inline std::vector<PillDescription> PillEffects;
inline std::vector<CollectibleQuality> CollectibleQualities;
inline bool CatalogLoaded=false,QualityLoaded=false;

inline const Description* describe(std::uint32_t variant,std::uint32_t id) {
    if (variant==70) return nullptr; // Pill appearance is not an effect ID.
    const auto key=(std::uint64_t(variant)<<32)|id;
    const auto it=std::lower_bound(Descriptions.begin(),Descriptions.end(),key,
        [](const Description& d,std::uint64_t k) { return ((std::uint64_t(d.variant)<<32)|d.id)<k; });
    return it!=Descriptions.end() && it->variant==variant && it->id==id?&*it:nullptr;
}
inline const PillDescription* describePillEffect(std::uint32_t effect) {
    return effect<PillEffects.size() && PillEffects[effect].effect==effect?&PillEffects[effect]:nullptr;
}

namespace catalog_detail {
inline constexpr std::size_t MaxBytes=1024*1024,MaxLine=16384;
// Bound allocations even for a corrupt file on the SD card.
inline bool line(std::istream& input,std::string& result,std::size_t& bytes) {
    result.clear();
    char ch;
    while (input.get(ch)) {
        if (++bytes>MaxBytes || ch=='\0' || result.size()>=MaxLine) {
            input.setstate(std::ios::badbit);return false;
        }
        if (ch=='\n') {
            if (!result.empty() && result.back()=='\r') result.pop_back();
            return true;
        }
        result+=ch;
    }
    if (input.bad()) return false;
    if (!result.empty() && result.back()=='\r') result.pop_back();
    return !result.empty();
}
inline std::vector<std::string_view> fields(const std::string& line) {
    std::vector<std::string_view> out;
    std::size_t start=0;
    for (std::size_t i=0;i<=line.size();++i) if (i==line.size() || line[i]=='\t') {
        out.emplace_back(line.data()+start,i-start);start=i+1;
    }
    return out;
}
inline bool number(std::string_view text,std::uint32_t& value) {
    if (text.empty()) return false;
    const auto r=std::from_chars(text.data(),text.data()+text.size(),value);
    return r.ec==std::errc{} && r.ptr==text.data()+text.size();
}
inline bool text(std::string_view input,std::string& out,std::size_t limit) {
    out.clear();
    for (std::size_t i=0;i<input.size();++i) {
        char ch=input[i];
        if (ch=='\\') {
            if (++i==input.size()) return false;
            switch (input[i]) {
                case '\\':ch='\\';break;
                case 'n':ch='\n';break;
                case 'r':ch='\r';break;
                case 't':ch='\t';break;
                default:return false;
            }
        } else if (static_cast<unsigned char>(ch)<0x20) return false;
        out+=ch;
        if (out.size()>limit) return false;
    }
    return !out.empty();
}
} // namespace catalog_detail

inline void clearCatalog() {
    CatalogLoaded=QualityLoaded=false;
    Descriptions.clear();PillEffects.clear();CollectibleQualities.clear();
}
inline bool loadCatalog(std::istream& input) {
    clearCatalog();
    std::string row;
    std::size_t bytes=0;
    if (!catalog_detail::line(input,row,bytes) || row!="# isaac-hud-catalog-v1") return false;
    std::vector<Description> items;
    std::vector<PillDescription> pills;
    std::array<std::size_t,3> counts{};
    std::uint64_t previous=0;
    while (catalog_detail::line(input,row,bytes)) {
        if (row.empty() || row[0]=='#') continue;
        const auto parts=catalog_detail::fields(row);
        if (parts.size()<3) return false;
        std::uint32_t variant=0,id=0;
        if (!catalog_detail::number(parts[1],variant) || !catalog_detail::number(parts[2],id)) return false;
        if (parts[0]=="D" && parts.size()==5) {
            const int category=variant==100?0:variant==300?1:variant==350?2:-1;
            if (category<0 || !id || id>(variant==100?732U:variant==300?97U:189U)) return false;
            const auto key=(std::uint64_t(variant)<<32)|id;
            if (key<=previous || items.size()>=1004) return false;
            previous=key;
            Description d{variant,id,{},{}};
            if (!catalog_detail::text(parts[3],d.name,256) || !catalog_detail::text(parts[4],d.text,4096)) return false;
            ++counts[category];items.push_back(std::move(d));
        } else if (parts[0]=="P" && parts.size()==6 && variant==70) {
            if (id!=pills.size() || id>=50) return false;
            PillDescription p{id,{},{},{}};
            if (!catalog_detail::text(parts[3],p.name,256) || !catalog_detail::text(parts[4],p.text,4096)
                || !catalog_detail::text(parts[5],p.horse,4096)) return false;
            pills.push_back(std::move(p));
        } else return false;
    }
    if (input.bad() || counts!=std::array<std::size_t,3>{719,97,188} || pills.size()!=50) return false;
    Descriptions=std::move(items);PillEffects=std::move(pills);CatalogLoaded=true;
    return true;
}

inline bool loadQuality(std::istream& input) {
    CollectibleQualities.clear();QualityLoaded=false;
    if (!CatalogLoaded) return false;
    std::size_t bytes=0;
    std::string row;
    if (!catalog_detail::line(input,row,bytes) || row!="# isaac-hud-quality-v1") return false;
    std::vector<CollectibleQuality> qualities;
    std::uint32_t previous=0;
    while (catalog_detail::line(input,row,bytes)) {
        if (row.empty() || row[0]=='#') continue;
        const auto parts=catalog_detail::fields(row);
        std::uint32_t id=0,q=0;
        if (parts.size()!=2 || !catalog_detail::number(parts[0],id) || !catalog_detail::number(parts[1],q)
            || id<=previous || q>4 || !describe(100,id) || qualities.size()>=719) return false;
        previous=id;qualities.push_back({id,static_cast<std::uint8_t>(q)});
    }
    if (input.bad()) return false;
    CollectibleQualities=std::move(qualities);QualityLoaded=true;
    return true;
}
inline bool loadHudDataFromFiles(const char* catalogPath=RuntimeCatalogPath,
                                 const char* qualityPath=RuntimeQualityPath) {
    clearCatalog();
    std::ifstream catalog(catalogPath,std::ios::binary);
    if (!catalog || !loadCatalog(catalog)) return false;
    catalog.close();
    std::ifstream quality(qualityPath,std::ios::binary);
    if (quality) loadQuality(quality); // Optional: descriptions survive a bad/missing tier file.
    return true;
}
} // namespace isaac
