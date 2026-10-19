#pragma once
#include "isaac/core.hpp"
#include <switch.h>

// Official Atmosphere dmntcht.c/.h are acquired by prepare_switch.sh at build time.
class DmntMemory final : public isaac::Memory {
    bool ready_{};
public:
    bool initialize();
    void shutdown();
    bool metadata(isaac::Metadata& out) override;
    bool read(isaac::Address address, std::span<std::uint8_t> out, isaac::Context) override;
};
