CXX ?= g++
CXXFLAGS ?= -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror

.PHONY: host-test publication-audit switch-prepare switch-build clean
HOST_TESTS := catalog descriptions hud hud_layout hud_controls
HOST_HEADERS := $(wildcard include/isaac/*.hpp)

host-test: $(addprefix out/test_,$(HOST_TESTS))
	./out/test_catalog
	./out/test_descriptions
	./out/test_hud
	./out/test_hud_layout
	./out/test_hud_controls


out/test_%: tests/test_%.cpp core/core.cpp $(HOST_HEADERS)
	mkdir -p out
	$(CXX) $(CXXFLAGS) -Iinclude core/core.cpp $< -o $@

switch-prepare:
	bash scripts/prepare_hud.sh

switch-build:
	@test -f switch_build/Makefile || (echo 'Run make switch-prepare in a devkitPro environment first'; exit 1)
	$(MAKE) -C switch_build

clean:
	rm -rf out

publication-audit:
	python3 scripts/audit_publication.py
