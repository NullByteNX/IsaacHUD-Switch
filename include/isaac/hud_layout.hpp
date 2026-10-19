#pragma once
#include <algorithm>
#include <string>
#include <string_view>
#include <vector>

namespace isaac {
// Framebuffer coordinates (448x720 in the validated libtesla), not game XY.
// Raise the title to the coin row based on the user's 0.4.2 console photo.
inline constexpr int HudTextX=176, HudTitleY=160, HudRightMargin=16;
inline constexpr float HudTitleSize=22.0f, HudBodySize=18.0f;
inline constexpr int HudTitleLineHeight=28, HudBodyLineHeight=22, HudTitleBodyGap=28;
inline int hudTextWidth(int framebufferWidth) {
    return std::max(0,framebufferWidth-HudTextX-HudRightMargin);
}

// Measure uses the actual UI font. Preserve explicit newlines, wrap at words,
// and split oversized tokens only at UTF-8 boundaries. No ellipsis/data loss.
template<class Measure>
std::vector<std::string> wrapHudText(std::string_view text, int width, Measure measure) {
    std::vector<std::string> lines;
    if (text.empty() || width<=0) return lines;
    std::string line;
    const auto flush=[&] { lines.push_back(line); line.clear(); };
    for (std::size_t pos=0;pos<text.size();) {
        if (text[pos]=='\n') { flush(); ++pos; continue; }
        if (text[pos]==' ' || text[pos]=='\t' || text[pos]=='\r') { ++pos; continue; }
        const auto begin=pos;
        while (pos<text.size() && text[pos]!=' ' && text[pos]!='\t'
               && text[pos]!='\r' && text[pos]!='\n') ++pos;
        std::string word(text.substr(begin,pos-begin));
        const std::string candidate=line.empty()?word:line+" "+word;
        if (static_cast<long long>(measure(candidate))<=width) { line=candidate; continue; }
        if (!line.empty()) flush();
        for (std::size_t start=0;start<word.size();) {
            std::size_t end=start+1;
            while (end<word.size() && (static_cast<unsigned char>(word[end])&0xC0)==0x80) ++end;
            const auto glyph=word.substr(start,end-start);
            if (!line.empty() && static_cast<long long>(measure(line+glyph))>width) flush();
            line+=glyph; start=end;
        }
    }
    if (!line.empty()) flush();
    return lines;
}
} // namespace isaac
