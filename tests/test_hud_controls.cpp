#include "isaac/hud_controls.hpp"
#include <iostream>
#include <stdexcept>

int main() {
    using isaac::HudAction;
    int checks=0;
    const auto check=[&](bool ok) { ++checks; if (!ok) throw std::runtime_error("HUD controls failed"); };
    isaac::HudControls c;
    check(c.update(true,true,0)==HudAction::None); // Carried-over launch keys.
    check(c.update(true,true,2'000'000'000ULL)==HudAction::None);
    check(c.update(false,false,3'000'000'000ULL)==HudAction::None);
    check(c.update(false,true,3'100'000'000ULL)==HudAction::Toggle);
    check(c.update(false,true,4'100'000'000ULL)==HudAction::None); // No repeated toggle.
    check(c.update(false,false,4'200'000'000ULL)==HudAction::None);
    check(c.update(false,true,4'300'000'000ULL)==HudAction::Toggle); // Works after release.
    check(c.update(true,false,5'000'000'000ULL)==HudAction::None);
    check(c.update(true,false,5'999'999'999ULL)==HudAction::None);
    check(c.update(false,false,6'000'000'000ULL)==HudAction::None); // Interrupted hold.
    check(c.update(true,false,6'100'000'000ULL)==HudAction::None);
    check(c.update(true,false,7'100'000'000ULL)==HudAction::ReturnMenu);
    check(c.update(true,false,9'000'000'000ULL)==HudAction::None); // One chainload only.
    check(c.update(false,false,9'100'000'000ULL)==HudAction::None);
    check(c.update(false,true,9'200'000'000ULL)==HudAction::None);
    isaac::HudControls simultaneous;
    check(simultaneous.update(false,false,0)==HudAction::None);
    check(simultaneous.update(true,true,1)==HudAction::None);
    check(simultaneous.update(true,true,1'000'000'001ULL)==HudAction::ReturnMenu);
    isaac::HudControls origin;
    check(origin.update(false,false,0)==HudAction::None);
    check(origin.update(true,false,0)==HudAction::None);
    check(origin.update(true,false,1'000'000'000ULL)==HudAction::ReturnMenu); // Zero is a valid timestamp.
    std::cout << checks << " HUD control checks PASS\n";
}
