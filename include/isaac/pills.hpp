#pragma once
#include <array>
#include <cstdint>
#include <optional>
#include <span>
#include <utility>

namespace isaac {
// Traced in capture 010 and checked live in 011..014, build BDB0590D4BA00019.
// These offsets belong to the freshly resolved GameCandidate, not main/heap.
inline constexpr std::uint64_t PillEffectsGameOffset=0x24CEC;
inline constexpr std::uint64_t PillRevealGameOffset=0x24D28;
inline constexpr std::size_t PillColorCount=15, PillTableBytes=75;
inline constexpr std::uint32_t PillEffectCount=50;
inline constexpr bool standardPillColor(std::uint32_t raw) { return raw>=1 && raw<=13; }

struct PillTable {
    std::array<std::uint32_t,PillColorCount> effects{};
    std::array<std::uint8_t,PillColorCount> revealed{};
    bool operator==(const PillTable&) const = default;
};
inline std::optional<PillTable> decodePillTable(std::span<const std::uint8_t> bytes) {
    if(bytes.size()!=PillTableBytes)return {};
    PillTable result;
    for(std::size_t color=0;color<PillColorCount;++color) {
        auto& value=result.effects[color];
        for(std::size_t i=0;i<4;++i)value|=std::uint32_t(bytes[color*4+i])<<(8*i);
        if(value>=PillEffectCount && value!=UINT32_MAX)return {};
        result.revealed[color]=bytes[PillColorCount*4+color];
        if(result.revealed[color]>1)return {};
    }
    return result;
}
inline std::optional<std::uint32_t> revealedBaseEffect(const PillTable& table,std::uint32_t rawColor) {
    // Horse/golden/invalid colors need their own live verification. Do not
    // silently strip flags and claim the ordinary capture proves those cases.
    if(!standardPillColor(rawColor) || table.revealed[rawColor]!=1
        || table.effects[rawColor]>=PillEffectCount)return {};
    return table.effects[rawColor]; // Effect 0 is valid; raw color 0 is empty.
}
inline constexpr std::array<std::pair<std::uint64_t,std::uint32_t>,22> PillCodeWords{{
    {0x3815F8,0xB0002368},{0x3815FC,0xF944A908},{0x381600,0xF9400108},
    {0x381604,0x92402921},{0x381608,0x8B010109},{0x38160C,0x5289A50A},
    {0x381610,0x72A0004A},{0x381614,0x386A6929},
    {0x381628,0x52885809},{0x38162C,0x72A00049},{0x381630,0x8B090108},
    {0x381644,0xAA1903E2},{0x381648,0x94008208},
    {0x3A1EA0,0x12002828},{0x3A1EA4,0x8B284808},{0x3A1EA8,0xB94A2D14},
    {0x2C0F6C,0x12002AA9},{0x2C0FAC,0x8B090108},{0x2C0FB0,0x5289A509},
    {0x2C0FB4,0x72A00049},{0x2C0FB8,0x5280002A},{0x2C0FBC,0x3829690A},
}};
} // namespace isaac
