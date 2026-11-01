#pragma once
#include "isaac/catalog.hpp"
#include <stdexcept>
inline void testLoadCatalog(const char* quality="runtime/collectible_quality.tsv") {
    if (!isaac::loadHudDataFromFiles("runtime/catalog_it.tsv",quality))
        throw std::runtime_error("Cannot load host catalog fixture");
}
