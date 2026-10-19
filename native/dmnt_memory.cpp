#include "dmnt_memory.hpp"
#include "dmntcht.h"
#include <algorithm>

bool DmntMemory::initialize() {
    if (ready_) return true;
    if (R_FAILED(pminfoInitialize())) return false;
    if (R_FAILED(dmntchtInitialize())) { pminfoExit(); return false; }
    // pmdmnt is owned by libtesla, as documented in Tesla-Template.
    ready_=true; return true;
}
void DmntMemory::shutdown() {
    if (!ready_) return;
    dmntchtExit(); pminfoExit(); ready_=false;
    // Close our IPC sessions only; do not close dmnt's shared process handle.
}
bool DmntMemory::metadata(isaac::Metadata& out) {
    out={};
    if (!ready_) return false;
    u64 pid{}, title{};
    if (R_FAILED(pmdmntGetApplicationProcessId(&pid)) || R_FAILED(pminfoGetProgramId(&title,pid))
        || title != isaac::TitleId) return false;
    bool attached{};
    if (R_FAILED(dmntchtHasCheatProcess(&attached))) return false;
    if (!attached && R_FAILED(dmntchtForceOpenCheatProcess())) return false;
    DmntCheatProcessMetadata current{};
    if (R_FAILED(dmntchtGetCheatProcessMetadata(&current)) || current.process_id != pid
        || current.title_id != title) return false;
    out.pid=current.process_id; out.title=current.title_id;
    out.main=current.main_nso_extents.base; out.mainSize=current.main_nso_extents.size;
    out.heap=current.heap_extents.base; out.heapSize=current.heap_extents.size;
    std::copy_n(current.main_nso_build_id,out.build.size(),out.build.begin());
    return true;
}
bool DmntMemory::read(isaac::Address address, std::span<std::uint8_t> out, isaac::Context) {
    std::fill(out.begin(),out.end(),0);
    if (!ready_ || out.empty()) return false;
    const auto rc=dmntchtReadCheatProcessMemory(address,out.data(),out.size());
    if (R_FAILED(rc)) { std::fill(out.begin(),out.end(),0); return false; }
    return true;
}
