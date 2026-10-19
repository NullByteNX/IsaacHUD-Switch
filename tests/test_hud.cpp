#include "isaac/hud.hpp"
#include <iostream>
#include <limits>
#include <stdexcept>

int main() {
    using namespace isaac;
    int checks=0;
    const auto check=[&](bool ok) { ++checks; if (!ok) throw std::runtime_error("HUD proximity check failed"); };
    Snapshot s;
    s.status=Status::Valid; s.process.pid=9; s.room=20;
    s.players.push_back(Entity{100,0,1,0,0,0,0});
    s.nearest=Item{200,70,93,0,350};
    HudGate gate;
    check(!gate.update(s)); // Initially outside the appearance radius.
    s.nearest->x=92;
    const auto louse=gate.update(s);
    check(louse && louse->title=="Louse");
    s.nearest->x=110.39999f;
    check(gate.update(s).has_value()); // Hysteresis keeps the same object stable.
    s.nearest->x=110.40001f;
    check(!gate.update(s));
    s.nearest->x=100;
    check(!gate.update(s)); // Once hidden, must re-enter at 92.
    s.nearest->x=80; s.nearest->y=80;
    check(!gate.update(s)); // Euclidean radius, not an axis-aligned box.
    s.nearest->x=64; s.nearest->y=64;
    check(gate.update(s).has_value()); // Inside 92 on a diagonal.
    s.nearest->id=5; s.nearest->x=100; s.nearest->y=0;
    check(!gate.update(s)); // New target must satisfy appearance radius.
    s.nearest->x=60;
    const auto purple=gate.update(s);
    check(purple && purple->title=="Purple Heart" && purple->description!=louse->description);
    s.nearest->x=100; s.process.pid=10;
    check(!gate.update(s)); // A new process cannot inherit visibility.
    s.nearest->x=60;
    check(gate.update(s).has_value());
    s.room=21; s.nearest->x=100;
    check(!gate.update(s)); // Nor a different room.
    s.nearest->x=60;
    check(gate.update(s).has_value());
    s.nearest->address=201; s.nearest->x=100;
    check(!gate.update(s)); // Nor a replacement pickup.
    s.nearest->x=60; s.nearest->id=99999; s.nearest->variant=100;
    const auto unknown=gate.update(s);
    check(unknown && unknown->title=="COLLECTIBLE 99999");
    for (const auto status : {Status::Clear,Status::Unsupported,Status::ReadFailure,Status::Changed,Status::Invalid}) {
        s.status=status;
        check(!gate.update(s));
    }
    s.status=Status::Valid;
    s.players.push_back(Entity{101,0,1,0,0,0,0});
    check(!gate.update(s)); // Co-op selection is not defined.
    s.players.clear();
    check(!gate.update(s));
    s.players.push_back(Entity{100,0,1,0,0,0,0});
    s.nearest.reset();
    check(!gate.update(s));
    s.nearest=Item{200,70,std::numeric_limits<float>::quiet_NaN(),0,350};
    check(!gate.update(s));
    s.nearest->x=60; s.players.front().y=std::numeric_limits<float>::infinity();
    check(!gate.update(s));
    s.players.front().y=0; s.nearest->variant=300;s.nearest->id=14;
    const auto card=gate.update(s);
    check(card&&card->title=="XIII - Death");
    s.nearest->variant=70;s.nearest->id=1;
    const auto pill=gate.update(s);
    check(pill&&pill->title=="Pillola ???"&&pill->description.find("danno")==std::string::npos);
    s.nearest->id=2049;
    check(gate.update(s)->title=="Pillola gigante ???");
    s.nearest->variant=90;
    check(!gate.update(s));
    s.nearest->variant=350; s.nearest->id=0;
    check(!gate.update(s));
    s.nearest->id=70;
    check(gate.update(s).has_value());
    gate.reset(); s.nearest->x=100;
    check(!gate.update(s));
    s.nearest->x=90;
    check(gate.update(s).has_value()); // Now visible at a distance above the old 80.
    s.nearest->x=104;
    check(gate.update(s).has_value()); // Remains visible above the old exit of 96.
    s.nearest->x=110.4f; s.nearest->y=0.1f;
    check(!gate.update(s)); // A tiny diagonal excess is outside the exit circle.
    s.nearest->x=92; s.nearest->y=0.1f;
    check(!gate.update(s)); // Likewise for the entry circle.
    s.nearest->y=0;
    check(gate.update(s).has_value());
    s.status=Status::Invalid; s.nearest.reset();
    check(!gate.update(s));
    s.status=Status::Valid; s.room=22;
    s.nearest=Item{300,5,91,0,350};
    const auto resumed=gate.update(s);
    check(resumed && resumed->title=="Purple Heart");
    s.status=Status::ReadFailure;
    check(!gate.update(s));
    s.status=Status::Valid; s.nearest->x=100;
    check(!gate.update(s)); // A failed sample cannot retain the exit band.
    s.nearest->x=92;
    check(gate.update(s).has_value());
    std::cout << checks << " HUD proximity/presentation checks PASS\n";
}
