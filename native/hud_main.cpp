#define TESLA_INIT_IMPL
#include "isaac/tesla_hud.hpp"
#include "dmnt_memory.hpp"
#include "isaac/hud.hpp"
#include "isaac/hud_layout.hpp"
#include "isaac/hud_controls.hpp"
#include <atomic>
#include <cstdio>
#include <exception>

namespace {
// Diagnostic worker: no network, no writes, no pause/resume commands.
class Worker {
    DmntMemory memory_;
    Thread thread_{};
    Mutex mutex_{};
    std::atomic<bool> running_{};
    bool started_{}, visible_{};
    std::uint64_t generation_{};
    u64 completed_{};
    isaac::Snapshot result_;

    static void entry(void* object) { static_cast<Worker*>(object)->run(); }
    void run() {
        while (running_.load()) {
            mutexLock(&mutex_);
            const bool visible=visible_; const auto generation=generation_;
            mutexUnlock(&mutex_);
            if (visible) {
                isaac::Snapshot next;
                try { next=isaac::sample(memory_); }
                catch (const std::exception&) { next.reason="Errore interno del lettore"; }
                mutexLock(&mutex_);
                if (visible_ && generation_==generation && running_.load()) {
                    result_=std::move(next); completed_=armGetSystemTick();
                }
                mutexUnlock(&mutex_);
            }
            // Provisional cadence for the diagnostic panel; not a measured refresh promise.
            for (int i=0;i<(visible?50:5) && running_.load();++i) svcSleepThread(10'000'000);
        }
    }
public:
    void start() {
        if (!memory_.initialize()) { result_.reason="Servizi memoria non disponibili"; return; }
        running_=true;
        if (R_FAILED(threadCreate(&thread_,entry,this,nullptr,0x20000,0x2C,-2))) {
            running_=false; memory_.shutdown(); result_.reason="Creazione lettore fallita"; return;
        }
        if (R_FAILED(threadStart(&thread_))) {
            running_=false; threadClose(&thread_); memory_.shutdown(); result_.reason="Avvio lettore fallito"; return;
        }
        started_=true;
    }
    void stop() {
        setVisible(false); running_=false;
        if (started_) { threadWaitForExit(&thread_); threadClose(&thread_); started_=false; }
        memory_.shutdown();
    }
    void setVisible(bool visible) {
        mutexLock(&mutex_);
        visible_=visible; ++generation_; completed_=0; result_={};
        if (visible && !started_) result_.reason="Lettore non avviato";
        mutexUnlock(&mutex_);
    }
    isaac::Snapshot current() {
        mutexLock(&mutex_);
        auto copy=result_;
        // Never render an indefinitely retained last-good result after a stalled worker.
        if (!visible_ || (completed_ && armTicksToNs(armGetSystemTick()-completed_)>2'000'000'000ULL)) {
            copy={}; copy.reason="In attesa di dati attuali";
        }
        mutexUnlock(&mutex_); return copy;
    }
} worker;

// Text-only HUD: no opaque OverlayFrame, list, focusable elements or footer.
class HudGui final : public tsl::Gui {
    isaac::HudGate gate_;
    std::optional<isaac::Presentation> presentation_;
    u64 firstFrame_{};
    int cachedWidth_=-1;
    std::string cachedTitle_, cachedDescription_;
    std::vector<std::string> titleLines_, descriptionLines_;
    static void drawText(tsl::gfx::Renderer* renderer, const std::string& text,
                         s32 x, s32 y, float size) {
        const auto shadow=tsl::gfx::Renderer::a(tsl::Color(0xF000));
        const auto foreground=tsl::gfx::Renderer::a(tsl::Color(0xFFFF));
        for (const auto& offset : std::array<std::array<s32,2>,4>{{{{-1,0}},{{1,0}},{{0,-1}},{{0,1}}}})
            renderer->drawString(text.c_str(),false,x+offset[0],y+offset[1],size,shadow);
        renderer->drawString(text.c_str(),false,x,y,size,foreground);
    }
    void drawPresentation(tsl::gfx::Renderer* renderer, const std::string& title,
                          const std::string& description) {
        const int width=isaac::hudTextWidth(tsl::cfg::FramebufferWidth);
        if (width<=0) return;
        if (width!=cachedWidth_ || title!=cachedTitle_ || description!=cachedDescription_) {
            const auto measure=[&](float size) {
                return [renderer,size](const std::string& text) {
                    // Alpha zero measures without drawing into the framebuffer.
                    return renderer->drawString(text.c_str(),false,0,0,size,tsl::Color(0x0000)).first;
                };
            };
            titleLines_=isaac::wrapHudText(title,width,measure(isaac::HudTitleSize));
            descriptionLines_=isaac::wrapHudText(description,width,measure(isaac::HudBodySize));
            cachedWidth_=width; cachedTitle_=title; cachedDescription_=description;
        }
        int y=isaac::HudTitleY;
        for (const auto& line : titleLines_) {
            drawText(renderer,line,isaac::HudTextX,y,isaac::HudTitleSize);
            y+=isaac::HudTitleLineHeight;
        }
        if (!titleLines_.empty()) y+=isaac::HudTitleBodyGap-isaac::HudTitleLineHeight;
        for (const auto& line : descriptionLines_) {
            drawText(renderer,line,isaac::HudTextX,y,isaac::HudBodySize);
            y+=isaac::HudBodyLineHeight;
        }
    }
public:
    tsl::elm::Element* createUI() override {
        auto* drawer=new tsl::elm::CustomDrawer(
            [this](tsl::gfx::Renderer* renderer, s32, s32, s32, s32) {
                // Every buffer must be cleared, including when nothing is shown.
                // Merely skipping draw calls would retain an earlier description.
                renderer->clearScreen();
                if (presentation_) {
                    drawPresentation(renderer,presentation_->title,presentation_->description);
                } else if (firstFrame_ && armTicksToNs(armGetSystemTick()-firstFrame_)<2'000'000'000ULL) {
                    drawPresentation(renderer,"Isaac HUD 0.5.1 attivo",
                                     "Avvicinati a un oggetto.\nPer Tesla: tieni + e -.");
                }
            });
        // Unlike OverlayFrame, a root CustomDrawer does not lay itself out.
        drawer->setBoundaries(0,0,tsl::cfg::FramebufferWidth,tsl::cfg::FramebufferHeight);
        return drawer;
    }
    void update() override {
        if (!firstFrame_) firstFrame_=armGetSystemTick();
        presentation_=gate_.update(worker.current());
    }
    bool handleInput(u64, u64, const HidTouchState&,
                     HidAnalogStickState, HidAnalogStickState) override {
        // No Tesla GUI navigation while game input is passed through.
        // Raw controls are processed by the overlay even when this GUI is hidden.
        return true;
    }
};
class IsaacHudOverlay final : public tsl::Overlay {
    PadState pad_{};
    isaac::HudControls controls_;
    bool visible_{};
public:
    void initServices() override {
        padInitializeAny(&pad_);
        worker.start();
    }
    void exitServices() override { worker.stop(); }
    bool onTick() override {
        // Runs on the main overlay thread, including the hidden wait loop.
        // Do not depend on GUI keysDown or on there being a nearby object.
        padUpdate(&pad_);
        const u64 held=padGetButtons(&pad_);
        constexpr u64 exitCombo=HidNpadButton_Plus|HidNpadButton_Minus;
        const bool exitHeld=(held&exitCombo)==exitCombo;
        const bool comboHeld=tsl::cfg::launchCombo &&
            (held&tsl::cfg::launchCombo)==tsl::cfg::launchCombo;
        switch (controls_.update(exitHeld,comboHeld,armTicksToNs(armGetSystemTick()))) {
            case isaac::HudAction::ReturnMenu: {
                constexpr auto menuPath="sdmc:/switch/.overlays/ovlmenu.ovl";
                tsl::setNextOverlay(menuPath,menuPath);
                close();
                break;
            }
            case isaac::HudAction::Toggle:
                if (visible_) hide();
                else return true; // Wake and show the HUD from the hidden loop.
                break;
            default: break;
        }
        return false;
    }
    void onShow() override {
        visible_=true;
        worker.setVisible(true);
        // Upstream loop requested foreground immediately before this callback.
        // Restore input to the game while keeping the render layer running.
        tsl::hlp::requestForeground(false);
    }
    void onHide() override {
        visible_=false;
        worker.setVisible(false);
    }
    std::unique_ptr<tsl::Gui> loadInitialGui() override { return initially<HudGui>(); }
};
} // namespace
int main(int argc,char** argv) { return tsl::loop<IsaacHudOverlay>(argc,argv); }
