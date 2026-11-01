CXX ?= g++
CXXFLAGS ?= -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror
# Resolve local roots in both MSYS and Windows notation before compiling.
ISAAC_PRIVACY_FLAGS = $(or $(shell python3 scripts/build_privacy.py flags),$(error Unable to generate build privacy flags))

.PHONY: host-test publication-audit switch-prepare switch-build clean data sdcard-data release-package
HOST_TESTS := catalog descriptions hud hud_layout hud_controls quality runtime_catalog
HOST_HEADERS := $(wildcard include/isaac/*.hpp)

host-test: $(addprefix out/test_,$(HOST_TESTS))
	./out/test_catalog
	./out/test_descriptions
	./out/test_hud
	./out/test_hud_layout
	./out/test_hud_controls
	./out/test_quality
	./out/test_runtime_catalog
	python3 scripts/generate_catalog.py --check
	python3 scripts/generate_quality.py --check
	python3 tests/test_quality_import.py
	python3 tests/test_wiki_quality.py
	python3 tests/test_hud_render.py
	python3 tests/test_package_sd.py
	python3 tests/test_build_privacy.py


out/test_%: tests/test_%.cpp core/core.cpp $(HOST_HEADERS) tests/test_catalog_setup.hpp scripts/build_privacy.py Makefile
	mkdir -p out
	$(CXX) $(CXXFLAGS) $(ISAAC_PRIVACY_FLAGS) -Iinclude core/core.cpp $< -o $@

switch-prepare:
	bash scripts/prepare_hud.sh

switch-build:
	@test -f switch_build/Makefile || (echo 'Run make switch-prepare in a devkitPro environment first'; exit 1)
	$(MAKE) -C switch_build
	python3 scripts/build_privacy.py check switch_build/IsaacHUD.elf switch_build/IsaacHUD.ovl

clean:
	rm -rf out

publication-audit:
	python3 scripts/audit_publication.py

data:
	python3 scripts/generate_catalog.py
	python3 scripts/generate_quality.py

sdcard-data: data
	python3 scripts/package_sd.py

release-package: data
	@test -n "$(OVL)" || (echo 'Specify OVL=/path/to/compiled/IsaacHUD.ovl'; exit 1)
	python3 scripts/package_sd.py --ovl "$(OVL)" --require-quality
