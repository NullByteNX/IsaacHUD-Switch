#!/usr/bin/env python3
"""Host regression of the generated loop and the real HUD overlay controls.

Mock Switch IPC/display/thread primitives: validates sequencing, not hardware.
Run after prepare_hud.sh: python3 tests/test_hud_runtime.py
"""
from pathlib import Path
import subprocess
import tempfile

project = Path(__file__).resolve().parents[1]
header = (project / 'switch_build/include/isaac/tesla_hud.hpp').read_text()
native = (project / 'native/hud_main.cpp').read_text()
start = header.index('    template<typename TOverlay, impl::LaunchFlags launchFlags>\n    static inline int loop(')
loop = header[start:header.index('\n\n}', start)]
start = native.index('class IsaacHudOverlay final')
overlay = native[start:native.index('\n} // namespace', start)]
stub = r'''
#include "isaac/hud.hpp"
#include "isaac/hud_controls.hpp"
#include <atomic>
#include <mutex>
#include <memory>
#include <string>
#include <cstring>
#include <strings.h>
#include <iostream>
#include <stdexcept>
#include <vector>
using u8=unsigned char; using u64=unsigned long long; using Result=int;
constexpr Result timeout=1;
#define R_FAILED(x) ((x)!=0)
#define KERNELRESULT(x) timeout
#define ASSERT_FATAL(x) do { if (R_FAILED(x)) throw std::runtime_error("unexpected mock service failure"); } while(0)
void require(bool ok) { if (!ok) throw std::runtime_error("runtime regression failed"); }
u64 nowNs=0; int mode=0, shows=0, hides=0, renders=0, events=0;
bool joined=false, closedThread=false, homeInjected=false;
bool sawValidBefore=false, sawInvalid=false, sawValidAfter=false;
std::string nextPath,nextArgs;
struct Event { bool signaled=false; };
struct Thread {};
struct PadState { u64 held=0; };
constexpr u64 HidNpadButton_L=1,HidNpadButton_Down=2,HidNpadButton_StickR=4,
              HidNpadButton_Plus=8,HidNpadButton_Minus=16,HidNpadButton_B=32;
bool between(u64 begin,u64 end) { return nowNs>=begin*1'000'000 && nowNs<end*1'000'000; }
u64 keys() {
    constexpr u64 chord=HidNpadButton_L|HidNpadButton_Down|HidNpadButton_StickR;
    constexpr u64 menu=HidNpadButton_Plus|HidNpadButton_Minus;
    if (mode==0) return between(300,800)?HidNpadButton_B:between(1300,2700)?menu:0;
    if (mode==1) return between(200,320)?chord:between(400,1600)?menu:0;
    if (mode==2) return (between(200,350)||between(400,550))?chord:between(700,1900)?menu:0;
    if (mode==3) return between(600,800)?chord:between(1000,2300)?menu:0;
    return between(500,1800)?menu:0;
}
void padInitializeAny(PadState* p) { p->held=0; }
void padUpdate(PadState* p) { p->held=keys(); }
u64 padGetButtons(PadState* p) { return p->held; }
u64 armGetSystemTick() { return nowNs; }
u64 armTicksToNs(u64 ticks) { return ticks; }
void advance(u64 amount) { nowNs+=amount; require(nowNs<5'000'000'000ULL); }
Result eventCreate(Event*,bool) { ++events; return 0; }
void eventFire(Event* e) { e->signaled=true; }
void eventClear(Event* e) { e->signaled=false; }
Result eventWait(Event* e,u64 wait) {
    if (e->signaled) return 0;
    require(wait==50'000'000ULL); advance(wait); return timeout;
}
void eventClose(Event*) { require(joined && closedThread); --events; }
namespace tsl {
namespace cfg { u64 launchCombo=7; }
namespace impl {
enum class LaunchFlags:u8 { CloseOnExit=1 };
struct SharedThreadData {
    std::atomic<bool> running{false},overlayOpen{false},hideRequested{false};
    Event comboEvent; std::mutex dataMutex; u64 keysDownPending=0;
};
SharedThreadData* shared=nullptr;
void backgroundEventPoller(void*) {}
}
class Gui { public: virtual ~Gui()=default; virtual void update() {} };
namespace hlp {
template<class F> void doWithSmSession(F f) { f(); }
void requestForeground(bool enabled) { (void)enabled; }
}
void setNextOverlay(const std::string& path,const std::string& args) { nextPath=path;nextArgs=args; }
class Overlay {
public:
    static inline Overlay* s_overlayInstance=nullptr;
    bool m_closeOnExit=false, hidden=false,closing=false;
    std::unique_ptr<Gui> gui;
    virtual ~Overlay()=default;
    virtual void initServices() {} virtual void exitServices() {}
    virtual bool onTick() { return false; }
    virtual void onShow() {} virtual void onHide() {}
    virtual std::unique_ptr<Gui> loadInitialGui()=0;
    template<class T> std::unique_ptr<T> initially() { return std::make_unique<T>(); }
    void initScreen() {} void exitScreen() {} void disableNextAnimation() {}
    void changeTo(std::unique_ptr<Gui> g) { gui=std::move(g); }
    void show() { ++shows; onShow(); }
    void hide() { ++hides; hidden=true; onHide(); }
    void close() { closing=true; }
    bool shouldClose() { return closing; } bool shouldHide() { return hidden; }
    void resetFlags() { hidden=false;closing=false; }
    void clearScreen() {}
    void loop() {
        ++renders; gui->update(); advance(20'000'000ULL);
        const bool homeTime=(mode==3 && nowNs>=300'000'000ULL)||
                            (mode==4 && nowNs>=1'500'000'000ULL);
        if (homeTime && !homeInjected) { impl::shared->hideRequested=true;homeInjected=true; }
    }
};
}
Result threadCreate(Thread*,void(*)(void*),void* args,void*,int,int,int) {
    require(events==1); tsl::impl::shared=static_cast<tsl::impl::SharedThreadData*>(args); return 0;
}
Result threadStart(Thread*) { return 0; }
void threadWaitForExit(Thread*) { require(!tsl::impl::shared->running);joined=true; }
void threadClose(Thread*) { require(joined);closedThread=true; }
struct MockWorker {
    bool visible=false;
    void start() {} void stop() { visible=false; }
    void setVisible(bool v) { visible=v; }
    isaac::Snapshot current() {
        isaac::Snapshot s;
        if (!visible) return s;
        if (mode==0 && between(300,900)) { s.status=isaac::Status::Invalid;sawInvalid=true;return s; }
        s.status=isaac::Status::Valid;s.process.pid=9;s.room=20;
        s.players.push_back(isaac::Entity{100,0,1,0,0,0,0});
        s.nearest=isaac::Item{200,5,50,0,350};
        if (nowNs<300'000'000ULL) sawValidBefore=true;
        if (nowNs>=900'000'000ULL) sawValidAfter=true;
        return s;
    }
} worker;
class HudGui:public tsl::Gui {
    isaac::HudGate gate;
    void update() override { (void)gate.update(worker.current()); }
};
'''
main = r'''
int main() {
    for (mode=0;mode<5;++mode) {
        nowNs=0;shows=hides=renders=events=0;
        joined=closedThread=homeInjected=sawValidBefore=sawInvalid=sawValidAfter=false;
        nextPath.clear();nextArgs.clear();worker.visible=false;
        char arg[]="--skipCombo";char* argv[]={arg};
        tsl::loop<IsaacHudOverlay,tsl::impl::LaunchFlags::CloseOnExit>(1,argv);
        require(nextPath=="sdmc:/switch/.overlays/ovlmenu.ovl" && nextArgs==nextPath);
        require(joined && closedThread && events==0 && renders>0);
        if (mode==0) require(sawValidBefore && sawInvalid && sawValidAfter && hides==0 && shows==1);
        if (mode==1) require(hides==1 && shows==1); // Menu return from hidden state.
        if (mode==2) require(hides==1 && shows==2); // Hide/reopen then menu.
        if (mode==3) require(homeInjected && hides==1 && shows==2); // HOME recovery.
        if (mode==4) require(homeInjected && hides==1); // Close wins over hide.
    }
    std::cout << "5 generated runtime/real HUD control scenarios PASS (mock Switch primitives)\n";
}
'''
code = stub + '\nnamespace tsl {\n' + loop + '\n}\n' + overlay + '\n' + main
with tempfile.TemporaryDirectory(prefix='isaac_hud_runtime_') as directory:
    source = Path(directory) / 'runtime.cpp'
    binary = Path(directory) / 'runtime'
    source.write_text(code)
    subprocess.run(['g++', '-std=c++20', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    '-I'+str(project/'include'), str(source), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True, timeout=10)
