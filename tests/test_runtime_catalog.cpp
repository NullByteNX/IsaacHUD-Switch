#include "isaac/descriptions.hpp"
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <stdexcept>

int main() {
    using namespace isaac;
    int checks=0;
    const auto check=[&](bool ok) { ++checks;if (!ok) throw std::runtime_error("External catalog regression"); };
    std::ifstream file("runtime/catalog_it.tsv",std::ios::binary);
    const std::string original{std::istreambuf_iterator<char>(file),{}};
    const auto load=[&](const std::string& s) { std::istringstream in(s);return loadCatalog(in); };
    const auto quality=[&](const std::string& s) { std::istringstream in(s);return loadQuality(in); };
    check(load(original));
    check(CatalogLoaded && Descriptions.size()==1004 && PillEffects.size()==50);
    const auto originalName=describe(100,1)->name,originalText=describe(100,1)->text;
    check(quality("# isaac-hud-quality-v1\n1\t0\n2\t4\n"));
    check(collectibleQuality(100,1)==0 && collectibleQuality(100,2)==4);
    for (const auto variant:{70U,300U,350U}) check(!collectibleQuality(variant,1));
    check(!collectibleQuality(100,3));
    for (const auto& bad:std::vector<std::string>{
        "1\t4\n", "# isaac-hud-quality-v1\n1\t5\n", "# isaac-hud-quality-v1\n1\t-1\n",
        "# isaac-hud-quality-v1\n1\t4\n1\t2\n", "# isaac-hud-quality-v1\n2\t4\n1\t2\n",
        "# isaac-hud-quality-v1\n43\t4\n", "# isaac-hud-quality-v1\n1\t4\textra\n",
        "# isaac-hud-quality-v1\n1x\t4\n", "# isaac-hud-quality-v1\n1\t4x\n"}) {
        check(!quality(bad));check(!QualityLoaded && CollectibleQualities.empty());
        check(CatalogLoaded && describe(100,1)->name==originalName);
    }
    // Empty quality file with a valid header is explicit unavailability, not Q0.
    check(quality("# isaac-hud-quality-v1\n# no confirmed values\n"));
    check(CollectibleQualities.empty() && !collectibleQuality(100,1));
    check(quality("# isaac-hud-quality-v1\r\n1\t0")); // CRLF and missing final LF.
    std::string crlf;
    for (char c:original) { if(c=='\n') crlf+='\r';crlf+=c; }
    check(load(crlf));
    check(describe(100,1)->text==originalText);
    // Escapes round-trip without being interpreted as raw TSV delimiters.
    std::string escaped=original;
    const auto begin=escaped.find("D\t100\t1\t");
    const auto end=escaped.find('\n',begin);
    escaped.replace(begin,end-begin,"D\t100\t1\tNome\\tcon\\\\barra\tRiga 1\\nRiga 2");
    check(load(escaped));
    check(describe(100,1)->name=="Nome\tcon\\barra" && describe(100,1)->text=="Riga 1\nRiga 2");
    std::vector<std::string> badCatalogs{"", "# wrong-format\n", original.substr(0,original.size()/2)};
    auto invalid=original;invalid.insert(invalid.find("D\t100\t1\t"),"D\t100\t1\tDuplicate\tDuplicate\n");badCatalogs.push_back(invalid);
    invalid=original;invalid.replace(invalid.find("D\t100\t1\t"),7,"D\t70\t1");badCatalogs.push_back(invalid);
    invalid=original;invalid.push_back('\0');badCatalogs.push_back(invalid);
    invalid=original;invalid+="#"+std::string(catalog_detail::MaxLine+1,'x')+"\n";badCatalogs.push_back(invalid);
    invalid=original;invalid.replace(invalid.find("D\t100\t1\t"),9,"D\t100\t1\tX\\q\t");badCatalogs.push_back(invalid);
    for (const auto& bad:badCatalogs) {
        check(!load(bad));check(!CatalogLoaded && Descriptions.empty() && PillEffects.empty());
        check(!quality("# isaac-hud-quality-v1\n1\t4\n"));
    }
    check(loadHudDataFromFiles("runtime/catalog_it.tsv","out/does-not-exist-quality.tsv"));
    check(CatalogLoaded && CollectibleQualities.empty());
    check(!loadHudDataFromFiles("out/does-not-exist-catalog.tsv","runtime/collectible_quality.tsv"));
    check(!CatalogLoaded && Descriptions.empty() && CollectibleQualities.empty());
    std::cout<<checks<<" external catalog/quality failure and recovery checks PASS\n";
}
