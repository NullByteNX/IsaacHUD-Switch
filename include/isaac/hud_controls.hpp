#pragma once
#include <cstdint>

namespace isaac {
enum class HudAction { None, Toggle, ReturnMenu };
// Independent of sample validity, proximity and whether the GUI is visible.
// Input arriving from the previous overlay must be released before arming.
class HudControls {
    bool exitArmed_{}, comboArmed_{}, holding_{}, closing_{};
    std::uint64_t began_{};
public:
    HudAction update(bool exitHeld, bool comboHeld, std::uint64_t nowNs) {
        if (closing_) return HudAction::None;
        if (!comboHeld) comboArmed_=true;
        if (!exitHeld) { exitArmed_=true; holding_=false; }
        if (exitHeld) {
            // Reserve the chord so a simultaneous Tesla combo cannot hide it.
            comboArmed_=false;
            if (!exitArmed_) return HudAction::None;
            if (!holding_) { holding_=true; began_=nowNs; }
            if (nowNs>=began_ && nowNs-began_>=1'000'000'000ULL) {
                closing_=true; return HudAction::ReturnMenu;
            }
            return HudAction::None;
        }
        if (comboHeld && comboArmed_) {
            comboArmed_=false; return HudAction::Toggle;
        }
        return HudAction::None;
    }
};
} // namespace isaac
