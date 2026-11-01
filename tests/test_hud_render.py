#!/usr/bin/env python3
"""Exercise the actual native HudGui with mock drawing/worker primitives.

Checks rendering decisions and framebuffer bounds; not a Switch/font emulator.
"""
from pathlib import Path
import os
import subprocess
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_quality import render

root = Path(__file__).resolve().parents[1]
native = (root / "native/hud_main.cpp").read_text(encoding="utf-8")
gui = native[native.index("class HudGui final"):native.index("class IsaacHudOverlay final")]
stub = r'''
#include "isaac/hud.hpp"
#include "isaac/hud_layout.hpp"
#include <functional>
#include <iostream>
#include <memory>
#include <stdexcept>
using s32=int; using u64=unsigned long long;
struct HidTouchState {}; struct HidAnalogStickState {};
u64 armGetSystemTick() { return 10; }
u64 armTicksToNs(u64 t) { return t; }
void require(bool ok) { if (!ok) throw std::runtime_error("Native HUD render regression"); }
namespace tsl {
namespace cfg { int FramebufferWidth=448,FramebufferHeight=720; }
struct Color { std::uint16_t rgba; explicit Color(std::uint16_t c):rgba(c) {} };
namespace gfx {
struct Text { std::string text; int x,y; float size; std::uint16_t color; };
struct Rect { int x,y,w,h; std::uint16_t color; };
class Renderer {
public:
    std::vector<Text> texts; std::vector<Rect> rects;
    static Color a(Color c) { return c; }
    void clearScreen() { texts.clear();rects.clear(); }
    static int width(const std::string& text,float size) {
        int w=0;
        for (unsigned char c:text) if ((c&0xC0)!=0x80) w+=c==' '?4:static_cast<int>(size/2);
        return w;
    }
    std::pair<unsigned,unsigned> drawString(const char* t,bool,int x,int y,float size,Color c) {
        if ((c.rgba>>12)!=0) texts.push_back({t,x,y,size,c.rgba});
        return {width(t,size),0};
    }
    void drawRect(int x,int y,int w,int h,Color c) { rects.push_back({x,y,w,h,c.rgba}); }
};
}
namespace elm {
struct Element { virtual ~Element()=default; };
struct CustomDrawer:Element {
    std::function<void(gfx::Renderer*,s32,s32,s32,s32)> callback;
    explicit CustomDrawer(decltype(callback) cb):callback(cb) {}
    void setBoundaries(int,int,int,int) {}
};
}
class Gui {
public:
    virtual ~Gui()=default;
    virtual elm::Element* createUI()=0;
    virtual void update() {}
    virtual bool handleInput(u64,u64,const HidTouchState&,HidAnalogStickState,HidAnalogStickState) { return false; }
};
}
struct MockWorker { isaac::Snapshot snapshot; isaac::Snapshot current() { return snapshot; } } worker;
'''
main = r'''
int main(int argc,char** argv) {
    require(argc==3 && isaac::loadHudDataFromFiles(argv[1],argv[2]));
    HudGui gui;
    std::unique_ptr<tsl::elm::Element> ui(gui.createUI());
    auto* drawer=static_cast<tsl::elm::CustomDrawer*>(ui.get());
    tsl::gfx::Renderer renderer;
    auto& s=worker.snapshot;
    s.status=isaac::Status::Valid; s.process.pid=9; s.room=20;
    s.players.push_back({1,0,1,0,0,0,0});
    int samples=0;
    for (const int framebuffer:{448,320}) {
        tsl::cfg::FramebufferWidth=framebuffer;
        for (const auto& e:isaac::Descriptions) {
            s.nearest=isaac::Item{2,e.id,0,0,e.variant};
            gui.update();drawer->callback(&renderer,0,0,framebuffer,720);
            require(!renderer.texts.empty());
            const bool hasTier=isaac::collectibleQuality(e.variant,e.id).has_value();
            require(renderer.rects.empty()==!hasTier);
            bool title=false,body=false;
            for (const auto& t:renderer.texts) {
                if (t.color==isaac::HudTitleColor) {
                    title=true;require(t.size==isaac::HudTitleSize);
                    require(t.x>=isaac::HudTextX);
                    require(t.x+renderer.width(t.text,t.size)<=framebuffer-isaac::HudRightMargin);
                }
                if (t.color==isaac::HudBodyColor) { body=true;require(t.size==isaac::HudBodySize); }
            }
            for (const auto& r:renderer.rects) {
                require(r.x>=isaac::HudTextX && r.x+r.w<=framebuffer-isaac::HudRightMargin);
                require(r.y>=0 && r.y+r.h<isaac::HudTitleY+isaac::HudTitleLineHeight*10);
            }
            require(title && body);++samples;
        }
    }
    tsl::cfg::FramebufferWidth=448;
    for (const auto variant:{70U,350U,300U,100U}) {
        s.nearest=isaac::Item{2,99999,0,0,variant};
        gui.update();drawer->callback(&renderer,0,0,448,720);
        require(renderer.rects.empty());
    }
    // A previously visible badge must disappear on an invalid sample.
    s.nearest=isaac::Item{2,234,0,0,100};
    gui.update();drawer->callback(&renderer,0,0,448,720);
    require(renderer.rects.empty()==!isaac::collectibleQuality(100,234).has_value());
    s.status=isaac::Status::Invalid;
    gui.update();drawer->callback(&renderer,0,0,448,720);require(renderer.rects.empty());
    std::cout<<samples<<" actual HudGui catalog render scenarios PASS (mock font/display)\n";
}
'''
with tempfile.TemporaryDirectory(prefix="isaac_hud_render_") as directory:
    source = Path(directory) / "render.cpp"
    binary = Path(directory) / "render"
    source.write_text(stub + gui + main, encoding="utf-8")
    command = [os.environ.get("CXX", "g++"), "-std=c++20", "-O2", "-Wall", "-Wextra",
                    "-Wpedantic", "-Werror", "-I" + str(root / "include"), str(source),
                    "-o", str(binary)]
    subprocess.run(command, check=True)
    subprocess.run([str(binary), str(root/"runtime/catalog_it.tsv"), str(root/"runtime/collectible_quality.tsv")], check=True, timeout=15)
    # Synthetic tiers exercise EVERY collectible and all five digits. They are
    # test fixtures, never shipped as gameplay data or substituted for metadata.
    from isaac_test_fixture import synthetic_qualities
    fixture = Path(directory) / "quality.tsv"
    fixture.write_text(render(synthetic_qualities(root)), encoding="utf-8")
    subprocess.run([str(binary),str(root / "runtime/catalog_it.tsv"),str(fixture)],check=True,timeout=15)
