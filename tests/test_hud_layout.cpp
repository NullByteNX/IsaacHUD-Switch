#include "isaac/hud_layout.hpp"
#include <iostream>
#include <stdexcept>

int main() {
    int checks=0;
    const auto check=[&](bool ok) { ++checks; if (!ok) throw std::runtime_error("HUD wrapping failed"); };
    // Deterministic proportional font model for wrapping; live HUD measures
    // with libtesla's actual font, not this host model.
    const auto measure=[](const std::string& text) {
        unsigned width=0;
        for (const auto c : text) {
            const auto byte=static_cast<unsigned char>(c);
            if ((byte&0xC0)!=0x80) width+=c=='W'?14:c=='i'?3:c==' '?4:8;
        }
        return width;
    };
    const auto wrap=[&](std::string_view text, int width) {
        return isaac::wrapHudText(text,width,measure);
    };
    check(isaac::HudTextX>24);
    check(isaac::hudTextWidth(448)==256);
    check(isaac::HudTextX+isaac::hudTextWidth(448)==448-isaac::HudRightMargin);
    check(isaac::hudTextWidth(128)==0);
    check(wrap("Purple Heart",256)==std::vector<std::string>{"Purple Heart"});
    check(wrap("",256).empty());
    check(wrap("hello",0).empty());
    check(wrap("hello",-1).empty());
    check(wrap("A\nB",256)==std::vector<std::string>{"A","B"});
    check(wrap("A\n\nB",256)==std::vector<std::string>{"A","","B"});
    check(wrap("  A   B\tC\r\nD",256)==std::vector<std::string>{"A B C","D"});
    check(wrap("aa bb cc",36)==std::vector<std::string>{"aa bb","cc"});
    check(wrap("WW ii",28)==std::vector<std::string>{"WW","ii"});
    check(wrap("abcde",16)==std::vector<std::string>{"ab","cd","e"});
    check(wrap("àèéòù",16)==std::vector<std::string>{"àè","éò","ù"});
    const std::string longTitle="COLLECTIBLE 4294967295";
    const auto title=wrap(longTitle,100);
    check(title.size()>1);
    for (const auto& line : title) check(measure(line)<=100);
    const auto body=wrap("Raddoppia la probabilita'\ndi incontrare nemici campioni.",256);
    check(!body.empty());
    for (const auto& line : body) check(measure(line)<=256);
    std::string recovered;
    for (const auto& line : wrap("averylongwordwithnospace",24)) recovered+=line;
    check(recovered=="averylongwordwithnospace");
    std::cout << checks << " HUD position/wrapping checks PASS\n";
}
