BUILD_DIR ?= build
SPECS := triple_stacked triple_stacked_nonumber
AUTHOR := s1f464, team osu!
OSU_RESOURCES_TAG ?= 2026.1021.0
OSU_RESOURCES_ARCHIVE := $(BUILD_DIR)/osu-resources-$(OSU_RESOURCES_TAG).tar.gz

.PHONY: all
all: base $(SPECS)

.PHONY: base
base:
	mkdir -p $(BUILD_DIR)/base
	./scripts/render.py --build-dir $(BUILD_DIR)/base ./specs/base.json

$(OSU_RESOURCES_ARCHIVE):
	mkdir -p $(BUILD_DIR)
	curl -fsSL -o $@ https://github.com/ppy/osu-resources/archive/refs/tags/$(OSU_RESOURCES_TAG).tar.gz

.PHONY: audio
audio: $(OSU_RESOURCES_ARCHIVE)
	mkdir -p $(BUILD_DIR)/audio
	tar -xzf $(OSU_RESOURCES_ARCHIVE) \
		-C $(BUILD_DIR)/audio \
		--wildcards \
		--strip-components=4 \
		"osu-resources-$(OSU_RESOURCES_TAG)/osu.Game.Resources/Samples/Gameplay/Argon/*" \
		"osu-resources-$(OSU_RESOURCES_TAG)/osu.Game.Resources/Samples/Gameplay/normal-*.wav" \
		"osu-resources-$(OSU_RESOURCES_TAG)/osu.Game.Resources/Samples/Gameplay/drum-*.wav" \
		"osu-resources-$(OSU_RESOURCES_TAG)/osu.Game.Resources/Samples/Gameplay/soft-*.wav"

.PHONY: $(SPECS)
$(SPECS): %: base audio
	mkdir -p $(BUILD_DIR)/$*
	cp $(BUILD_DIR)/base/*.png $(BUILD_DIR)/$*
	./scripts/render.py --build-dir $(BUILD_DIR)/$* ./specs/$*.json
	./scripts/gen_skinini.py --name "freeosk $*" --author "$(AUTHOR)" -o $(BUILD_DIR)/$*/skin.ini
	cp ./src/MainHUDComponents.json $(BUILD_DIR)/$*
	cp $(BUILD_DIR)/audio/Argon/* $(BUILD_DIR)/$*
	cp $(BUILD_DIR)/audio/normal-*.wav \
		$(BUILD_DIR)/audio/drum-*.wav \
		$(BUILD_DIR)/audio/soft-*.wav \
		$(BUILD_DIR)/$*
	bsdtar -c -a --no-acls --no-fflags --no-xattrs --numeric-owner \
		--options zip:compression=store \
		--strip-components 1 \
		-f $(BUILD_DIR)/freeosk_$*.zip \
		-C $(BUILD_DIR)/$* \
		.
	mv $(BUILD_DIR)/freeosk_$*.zip $(BUILD_DIR)/freeosk_$*.osk

.PHONY: format-svg
format-svg:
	svgo --quiet --pretty --folder src

.PHONY: clean-audio
clean-audio:
	rm -rf $(BUILD_DIR)/audio

.PHONY: clean-sprites
clean-sprites:
	rm -rf $(BUILD_DIR)/base $(addprefix $(BUILD_DIR)/,$(SPECS))

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
