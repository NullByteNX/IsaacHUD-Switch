#pragma once
#include "isaac/catalog.hpp"
#include <optional>

namespace isaac {
inline std::optional<std::uint8_t> collectibleQuality(std::uint32_t variant,
                                                               std::uint32_t id) {
    if (variant!=100) return {};
    std::size_t low=0,high=CollectibleQualities.size();
    while (low<high) {
        const auto mid=low+(high-low)/2;
        if (CollectibleQualities[mid].id<id) low=mid+1; else high=mid;
    }
    if (low==CollectibleQualities.size() || CollectibleQualities[low].id!=id) return {};
    return CollectibleQualities[low].quality;
}
} // namespace isaac
