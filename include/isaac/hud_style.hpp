#pragma once
#include <array>
#include <cstdint>

namespace isaac {
// libtesla stores RGBA4444 with red in the low nibble (0xABGR).
inline constexpr std::uint16_t HudTitleColor=0xFB6B; // #BB66BB, like the reference.
inline constexpr std::uint16_t HudBodyColor=0xFFFF;
inline constexpr std::uint16_t HudOutlineColor=0xF000;
inline constexpr int HudBadgeScale=2, HudBadgeWidth=22, HudBadgeHeight=24;
inline constexpr int HudBadgeGap=6, HudBadgeTopOffset=-21;

// Original pixel shield and 3x5 numerals, drawn in code. No EID/game assets.
inline constexpr std::array<const char*,12> HudBadgeShape{{
    "...ooooo...", "..ohhhhho..", ".ohfffffho.", ".ohfffffho.",
    ".obfffffbo.", ".obfffffbo.", ".obfffffbo.", "..obfffbo..",
    "..obfffbo..", "...obfbo...", "....obo....", ".....o....."
}};
inline constexpr std::array<std::array<const char*,5>,5> HudBadgeDigits{{
    {{"111","101","101","101","111"}},
    {{"010","110","010","010","111"}},
    {{"111","001","111","100","111"}},
    {{"111","001","111","001","111"}},
    {{"101","101","111","001","001"}}
}};
// Every quality uses the reference's gold shield; the digit carries the value.
template<class DrawRect>
void drawHudQualityBadge(std::uint8_t quality,int x,int y,DrawRect rect) {
    if (quality>4) return;
    for (int row=0;row<12;++row) for (int col=0;col<11;++col) {
        const char pixel=HudBadgeShape[row][col];
        if (pixel=='.') continue;
        const std::uint16_t color=pixel=='o'?HudOutlineColor:pixel=='h'?0xF8EF:
            pixel=='b'?0xF169:0xF3BD;
        rect(x+col*HudBadgeScale,y+row*HudBadgeScale,HudBadgeScale,HudBadgeScale,color);
    }
    for (int row=0;row<5;++row) for (int col=0;col<3;++col)
        if (HudBadgeDigits[quality][row][col]=='1')
            rect(x+(col+4)*HudBadgeScale,y+(row+3)*HudBadgeScale,
                 HudBadgeScale,HudBadgeScale,HudOutlineColor);
}
} // namespace isaac
