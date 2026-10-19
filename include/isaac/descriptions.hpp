#pragma once
#include "isaac/core.hpp"
#include "isaac/catalog_data.hpp"
#include "isaac/pills.hpp"

namespace isaac {
inline constexpr const Description* describe(std::uint32_t variant,std::uint32_t id) {
    // Pill colors do not share the PillEffect namespace.
    if(variant==70)return nullptr;
    std::size_t low=0,high=Descriptions.size();
    const auto key=(std::uint64_t(variant)<<32)|id;
    while(low<high) {
        const auto mid=low+(high-low)/2;
        const auto& e=Descriptions[mid];
        const auto other=(std::uint64_t(e.variant)<<32)|e.id;
        if(other<key)low=mid+1;else high=mid;
    }
    return low<Descriptions.size()&&Descriptions[low].variant==variant&&Descriptions[low].id==id
        ?&Descriptions[low]:nullptr;
}
inline std::string rawItemLabel(const Item& item) {
    const std::string category=item.variant==350?"TRINKET ":
        item.variant==100?"COLLECTIBLE ":item.variant==300?"CARTA/RUNA ":
        item.variant==70?"PILLOLA COLORE ":"VARIANT "+std::to_string(item.variant)+" ID ";
    return category+std::to_string(item.id);
}
inline constexpr const PillDescription* describePillEffect(std::uint32_t effect) {
    return effect<PillEffects.size() && PillEffects[effect].effect==effect?&PillEffects[effect]:nullptr;
}
inline const PillDescription* identifiedPillDescription(const Item& item) {
    return item.variant==70 && standardPillColor(item.id) && item.pillBaseEffect
        ?describePillEffect(*item.pillBaseEffect):nullptr;
}
inline std::string itemCaption(const Item& item) {
    if(item.variant==70) {
        const auto* e=identifiedPillDescription(item);
        return (e?std::string(e->name):"Pillola ???")+" ["+rawItemLabel(item)+"]";
    }
    const auto* e=describe(item.variant,item.id);
    return e?std::string(e->name)+" ["+rawItemLabel(item)+"]":rawItemLabel(item);
}
struct Presentation {std::string title,description;};
inline Presentation presentItem(const Item& item,bool diagnostic) {
    if(item.variant==70) {
        if(const auto* e=identifiedPillDescription(item))
            return {diagnostic?itemCaption(item):e->name,e->text};
        const bool horse=(item.id&2048U)!=0;
        // Unknown, unsupported variants, absent/failed/changed optional reads:
        // preserve the fallback and never look up a pill by appearance ID.
        return {diagnostic?itemCaption(item):horse?"Pillola gigante ???":"Pillola ???",
            diagnostic?"Effetto identificato non disponibile per questo campione."
                :"Effetto non disponibile."};
    }
    const auto* e=describe(item.variant,item.id);
    return {diagnostic?itemCaption(item):e?e->name:rawItemLabel(item),
        e?e->text:"Descrizione non disponibile.\nID non incluso nel catalogo."};
}
inline Presentation presentNearest(const Snapshot& snapshot) {
    if(snapshot.status!=Status::Valid)return {"Oggetto vicino: -","Dati non disponibili."};
    if(!snapshot.nearest)return {"Oggetto vicino: -",snapshot.items.empty()
        ?"Nessun oggetto descrivibile nella stanza.":"Selezione non disponibile."};
    return presentItem(*snapshot.nearest,true);
}
} // namespace isaac
