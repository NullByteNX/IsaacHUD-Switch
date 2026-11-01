#include "isaac/hud.hpp"
#include "test_catalog_setup.hpp"
#include "isaac/hud_layout.hpp"
#include <iostream>
#include <stdexcept>

int main(int argc,char** argv) {
    testLoadCatalog(argc>1?argv[1]:"runtime/collectible_quality.tsv");
    using namespace isaac;
    int checks=0;
    const auto check=[&](bool ok) { ++checks; if (!ok) throw std::runtime_error("Quality regression"); };
    check(CollectibleQualities.size()<=719);
    std::uint32_t previous=0;
    for (const auto& entry:CollectibleQualities) {
        check(entry.id>previous); previous=entry.id;
        check(entry.quality<=4);
        check(collectibleQuality(100,entry.id)==entry.quality);
        check(describe(100,entry.id)!=nullptr);
        check(presentItem(Item{10,entry.id,0,0,100},false).quality==entry.quality);
        // Same numeric ID in another namespace must NEVER pick up a tier.
        for (const auto variant:{70U,300U,350U,999U}) {
            check(!collectibleQuality(variant,entry.id));
            check(!presentItem(Item{10,entry.id,0,0,variant},false).quality);
        }
    }
    // Unknown/missing metadata is distinct from an explicit quality of zero.
    if (CollectibleQualities.empty()) check(!collectibleQuality(100,234));
    check(!collectibleQuality(100,0));
    check(!collectibleQuality(100,43)); // Unused collectible ID.
    check(!collectibleQuality(100,99999));
    check(!presentItem(Item{10,99999,0,0,100},false).quality);
    const auto measure=[](const std::string& s) { return static_cast<int>(s.size())*10; };
    const auto noBadge=layoutHudTitle("Infestation 2",256,false,measure);
    const auto badge=layoutHudTitle("Infestation 2",256,true,measure);
    check(!noBadge.badge && badge.badge && badge.lines.size()==1);
    check(badge.suffixX==130);
    const auto longName=layoutHudTitle("A long collectible name with many words",256,true,measure);
    check(longName.lines.size()>1 && longName.badge);
    check(longName.suffixX+measure(" -")+HudBadgeGap+HudBadgeWidth<=256);
    check(!layoutHudTitle("X",24,true,measure).badge);
    check(!layoutHudTitle("",256,true,measure).badge);
    check(layoutHudTitle("X",0,true,measure).lines.empty());
    for (int tier=0;tier<=5;++tier) {
        int pixels=0;
        drawHudQualityBadge(tier,10,20,[&](int x,int y,int w,int h,std::uint16_t color) {
            ++pixels;
            check(x>=10 && x+w<=10+HudBadgeWidth);
            check(y>=20 && y+h<=20+HudBadgeHeight);
            check((color>>12)==0xF);
        });
        check(tier==5?pixels==0:pixels>0);
    }
    std::cout<<checks<<" collectible quality/layout/badge checks PASS\n";
}
