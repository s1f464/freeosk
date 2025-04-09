# freeosk

Minimalist [osu!](https://osu.ppy.sh/) skin assets focusing on osu gameplay.

## Features

- Minimalist design
- "Triple stacked" (hitcircle + hitcircleoverlay + default-x)
- SVG source
- Free as in freedom

## Developing

SVG files are created in Inkscape then optimized using
[SVGO](https://github.com/svg/svgo). Refer to
[Skin set list for the ranking criteria](https://osu.ppy.sh/wiki/en/Ranking_criteria/Skin_set_list)
as a general skinning guideline.

To optimize SVG:

    svgo --pretty --folder src

## Building

To build a complete .osk file:

1. Render SVG to formats supported by osu!.
2. Create configuration files.
3. Get additional assets.
4. Archive

[scripts/render.py](scripts/render.py) can be used for step 1. The following
executables are required to run the script.

- rsvg-convert: render SVG
- magick: create a 1x1 transparent PNG

[scripts/gen_skinini.py](scripts/gen_skinini.py) can be used for step 2.

For additional assets, a good starting point is
[osu-resources](https://github.com/ppy/osu-resources) (CC-BY-NC 4.0).

## License

SVG files are licensed under Creative Commons Zero v1.0 Universal
([LICENSE-CC0-1.0](LICENSE-CC0-1.0) or
<https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt>). Other files
are licensed under BSD Zero Clause License ([LICENSE-0BSD](LICENSE-0BSD) or
<https://opensource.org/license/0BSD>) unless explicitly stated.
