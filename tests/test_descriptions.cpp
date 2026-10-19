#include "isaac/descriptions.hpp"
#include <iostream>
#include <stdexcept>

int main() {
    using namespace isaac;
    int checks=0;
    const auto check=[&](bool ok) { ++checks; if (!ok) throw std::runtime_error("Catalog/presentation check failed"); };
    check(std::string(describe(100,24)->name)=="Dessert");
    check(std::string(describe(100,316)->name)=="Cursed Eye");
    check(std::string(describe(350,5)->name)=="Purple Heart");
    check(std::string(describe(350,61)->name)=="The Left Hand");
    check(std::string(describe(350,70)->name)=="Louse");
    // The full 0.5 catalog includes IDs absent from the former small catalog.
    // Equal numeric IDs must still resolve within their own variant namespace.
    check(std::string(describe(100,5)->name)=="My Reflection" &&
          std::string(describe(300,5)->name)=="IV - The Emperor");
    check(std::string(describe(350,24)->name)=="Butt Penny" && !describe(350,316));
    check(!describe(350,0x8000+70)); // No assumption about golden-trinket flags.
    Snapshot snapshot;
    snapshot.status=Status::Valid;
    snapshot.nearest=Item{1,70,10,20,350};
    snapshot.items.push_back(*snapshot.nearest);
    const auto known=presentNearest(snapshot);
    check(known.title=="Louse [TRINKET 70]" && known.description==describe(350,70)->text);
    snapshot.nearest=Item{2,99999,10,20,100};
    const auto unknown=presentNearest(snapshot);
    check(unknown.title=="COLLECTIBLE 99999" && unknown.description.find("non disponibile")!=std::string::npos);
    // Even an inconsistent caller retaining a nearest item must not publish it.
    for (const auto status : {Status::Clear,Status::Unsupported,Status::ReadFailure,Status::Changed,Status::Invalid}) {
        snapshot.status=status;
        const auto cleared=presentNearest(snapshot);
        check(cleared.title=="Oggetto vicino: -" && cleared.description=="Dati non disponibili.");
    }
    snapshot.status=Status::Valid;
    snapshot.nearest.reset(); snapshot.items.clear();
    const auto empty=presentNearest(snapshot);
    check(empty.title=="Oggetto vicino: -" && empty.description.find("Nessun")!=std::string::npos);
    snapshot.items.push_back(Item{1,70,10,20,350});
    check(presentNearest(snapshot).description=="Selezione non disponibile.");
    std::cout << checks << " catalog/presentation checks PASS\n";
}
