BUILD_DIR ?= build
SPECS := triple_stacked triple_stacked_nonumber instafade instafade_nonumber
AUTHOR := s1f464

.PHONY: all
all: base $(SPECS)

.PHONY: base
base:
	mkdir -p $(BUILD_DIR)
	./scripts/render.py --build-dir ${BUILD_DIR} ./specs/base.json

.PHONY: $(SPECS)
$(SPECS): %: base
	mkdir -p $(BUILD_DIR)/$*
	cp $(BUILD_DIR)/*.png $(BUILD_DIR)/$*
	./scripts/render.py --build-dir $(BUILD_DIR)/$* ./specs/$*.json
	./scripts/gen_skinini.py --name "freeosk $*" --author $(AUTHOR) -o $(BUILD_DIR)/$*/skin.ini
	cp ./src/MainHUDComponents.json $(BUILD_DIR)/$*

.PHONY: format-svg
format-svg:
	svgo --quiet --pretty --folder src

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
