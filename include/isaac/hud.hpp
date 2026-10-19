#pragma once
#include "isaac/descriptions.hpp"
#include <cmath>

namespace isaac {
// Provisional proximity thresholds in the game's XY units, not screen pixels.
// Both thresholds increased by 15% over the original 80/96.
inline constexpr double HudEnterRadius=92.0, HudExitRadius=110.4;
class HudGate {
    bool shown_{};
    Address pid_{}, room_{}, address_{};
    std::uint32_t variant_{}, id_{};
public:
    void reset() { shown_=false; pid_=room_=address_=0; variant_=id_=0; }
    std::optional<Presentation> update(const Snapshot& snapshot) {
        if (snapshot.status!=Status::Valid || snapshot.players.size()!=1 || !snapshot.nearest) {
            reset(); return {};
        }
        const auto& player=snapshot.players.front();
        const auto& item=*snapshot.nearest;
        if (!item.id || !descriptiveVariant(item.variant)
            || !std::isfinite(player.x) || !std::isfinite(player.y)
            || !std::isfinite(item.x) || !std::isfinite(item.y)) {
            reset(); return {};
        }
        const bool same=shown_ && pid_==snapshot.process.pid && room_==snapshot.room
            && address_==item.address && variant_==item.variant && id_==item.id;
        const double dx=double(item.x)-player.x, dy=double(item.y)-player.y;
        const double radius=same?HudExitRadius:HudEnterRadius;
        if (dx*dx+dy*dy>radius*radius) { reset(); return {}; }
        shown_=true; pid_=snapshot.process.pid; room_=snapshot.room;
        address_=item.address; variant_=item.variant; id_=item.id;
        // Known objects show only the name during gameplay; diagnostic IDs stay
        // in the separate 0.3 overlay. An unknown ID remains explicit.
        return presentItem(item,false);
    }
};
} // namespace isaac
