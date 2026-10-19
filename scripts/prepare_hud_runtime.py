#!/usr/bin/env python3
"""Generate a HUD-only libtesla adaptation; never edit the dependency checkout.

Fail closed if the audited upstream blocks differ. The diagnostic keeps using
the original tesla.hpp. The generated header retains its license and credits.
"""
from pathlib import Path
import sys


def adapt(source):
    def replace(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise ValueError('Blocco libtesla non riconosciuto: ' + old.splitlines()[0])
        source = source.replace(old, new)

    replace('#include <mutex>', '#include <mutex>\n#include <atomic>')
    replace('        virtual void onHide() {}', '''        virtual void onHide() {}

        // Isaac HUD: runs on the overlay thread, also while hidden.
        // Return true to request a show; close() is checked before waiting again.
        virtual bool onTick() { return false; }''')
    replace('            bool running = false;', '            std::atomic<bool> running{false};')
    replace('            bool overlayOpen = false;', '''            std::atomic<bool> overlayOpen{false};
            std::atomic<bool> hideRequested{false};''')
    replace('''                    if (((shData->keysHeld & tsl::cfg::launchCombo) == tsl::cfg::launchCombo) && shData->keysDown & tsl::cfg::launchCombo) {
                        if (shData->overlayOpen) {
                            tsl::Overlay::get()->hide();
                            shData->overlayOpen = false;
                        }
                        else
                            eventFire(&shData->comboEvent);
                    }''', '''                    // Isaac HUD owns its raw input on the main thread.
                    // Do not race its show/hide decisions from this poller.''')
    replace('''                    if (shData->overlayOpen) {
                        tsl::Overlay::get()->hide();
                        shData->overlayOpen = false;
                    }''', '''                    if (shData->overlayOpen)
                        shData->hideRequested = true; // Apply HOME/sleep on main thread.''')
    replace('''        Thread backgroundThread;
        threadCreate(&backgroundThread, impl::backgroundEventPoller, &shData, nullptr, 0x1000, 0x2c, -2);
        threadStart(&backgroundThread);

        eventCreate(&shData.comboEvent, false);''', '''        // The event must exist before any background thread can use it.
        ASSERT_FATAL(eventCreate(&shData.comboEvent, false));
        Thread backgroundThread;
        ASSERT_FATAL(threadCreate(&backgroundThread, impl::backgroundEventPoller, &shData, nullptr, 0x1000, 0x2c, -2));
        ASSERT_FATAL(threadStart(&backgroundThread));''')
    replace('''            eventWait(&shData.comboEvent, UINT64_MAX);
            eventClear(&shData.comboEvent);
            shData.overlayOpen = true;''', '''            // Keep HUD controls alive while the GUI is hidden.
            const Result waitResult = eventWait(&shData.comboEvent, 50'000'000ULL);
            if (R_FAILED(waitResult) && waitResult != KERNELRESULT(TimedOut))
                ASSERT_FATAL(waitResult);
            const bool showRequested = overlay->onTick();
            if (overlay->shouldClose()) {
                shData.running = false;
                break;
            }
            if (R_FAILED(waitResult) && !showRequested)
                continue;
            eventClear(&shData.comboEvent);
            shData.overlayOpen = true;''')
    replace('''            while (shData.running) {
                overlay->loop();

                {
                    std::scoped_lock lock(shData.dataMutex);
                    if (!overlay->fadeAnimationPlaying()) {
                        overlay->handleInput(shData.keysDownPending, shData.keysHeld, shData.touchState.count, shData.touchState.touches[0], shData.joyStickPosLeft, shData.joyStickPosRight);
                    }
                    shData.keysDownPending = 0;
                }

                if (overlay->shouldHide())
                    break;

                if (overlay->shouldClose())
                    shData.running = false;
            }''', '''            while (shData.running) {
                if (shData.hideRequested.exchange(false))
                    overlay->hide();
                overlay->onTick();
                if (overlay->shouldClose()) {
                    shData.running = false;
                    break;
                }
                overlay->loop();

                // Game buttons/touches cannot navigate or dismiss a HUD GUI.
                // onTick reads its own PadState outside dataMutex.
                {
                    std::scoped_lock lock(shData.dataMutex);
                    shData.keysDownPending = 0;
                }

                // A menu return must win over a simultaneous hide/fade-out.
                if (overlay->shouldClose()) {
                    shData.running = false;
                    break;
                }
                if (overlay->shouldHide())
                    break;
            }''')
    replace('''        eventClose(&shData.comboEvent);

        threadWaitForExit(&backgroundThread);
        threadClose(&backgroundThread);''', '''        threadWaitForExit(&backgroundThread);
        threadClose(&backgroundThread);
        eventClose(&shData.comboEvent);''')
    return (
        '// Modified from libtesla for Isaac HUD v0.5.1 '
        '(2026-10-19): onTick, atomic state, thread '
        'synchronization, input and show/hide handling.\n'
        '// Original copyright and GPL notices retained below.\n'
    ) + source


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Uso: prepare_hud_runtime.py INPUT_TESLA_HPP OUTPUT_HUD_HPP')
    source_path, target_path = map(Path, sys.argv[1:])
    if source_path.resolve() == target_path.resolve():
        raise SystemExit('La copia HUD deve essere separata da libtesla originale.')
    try:
        generated = adapt(source_path.read_text(encoding='utf-8'))
    except ValueError as error:
        raise SystemExit(str(error) + '. Nessuna modifica al repository libtesla.')
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(generated, encoding='utf-8')
    print('Runtime HUD preparato: input controllato anche durante attesa/nascondimento.')
