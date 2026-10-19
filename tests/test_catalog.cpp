#include "isaac/hud.hpp"
#include <iostream>
#include <stdexcept>

int main() {
    using namespace isaac;int checks=0;
    const auto check=[&](bool ok,const char* why){++checks;if(!ok)throw std::runtime_error(why);};
    check(Descriptions.size()==1004&&PillEffects.size()==50,"Full pinned coverage");
    std::uint64_t previous=0;
    for(const auto& e:Descriptions) {
        const auto key=(std::uint64_t(e.variant)<<32)|e.id;
        check(key>previous,"Ordered unique variant/ID namespace");previous=key;
        check(describe(e.variant,e.id)==&e,"Lookup finds every embedded entry");
        check(e.name[0]&&e.text[0],"Nonempty Italian summary");
    }
    check(std::string(describe(100,5)->name)=="My Reflection","Same number collectible");
    check(std::string(describe(350,5)->name)=="Purple Heart","Same number trinket");
    check(std::string(describe(300,5)->name)=="IV - The Emperor","Same number card");
    check(!describe(70,5),"Pill appearance is never looked up as effect");
    check(std::string(describe(100,474)->name)=="Broken Glass Cannon","Repentance replaces old ID 474");
    check(!describe(100,43)&&!describe(100,99999)&&!describe(350,47),"Undocumented/unused IDs stay unknown");
    check(!describe(350,0x8000+5),"Golden trinket raw IDs not guessed");
    check(PillEffects[0].effect==0&&std::string(PillEffects[0].name)=="Bad Gas","Effect zero valid in effect namespace");
    for(std::uint32_t color=1;color<=14;++color)for(const auto horse:{0U,2048U}) {
        const Item pill{10,color|horse,0,0,70};
        const auto text=presentItem(pill,false);
        check(text.title.find("???")!=std::string::npos&&text.description=="Effetto non disponibile.","No effects revealed from any pill color");
    }
    Snapshot s;s.status=Status::Valid;s.process.pid=9;s.room=20;
    s.players.push_back({1,0,1,0,0,0,0});s.nearest=Item{2,1,0,0,70};
    HudGate gate;check(gate.update(s)->title=="Pillola ???","Unknown pill near player visible");
    s.status=Status::Invalid;check(!gate.update(s),"Invalid pill snapshot clears HUD");
    s.status=Status::Valid;s.process.pid=10;s.room=21;
    check(gate.update(s)->title=="Pillola ???","New process/run cannot inherit a known pill effect");
    std::cout<<checks<<" catalog and pill-disclosure checks PASS\n";
}
