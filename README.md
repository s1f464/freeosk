# freeosk

Minimalist [osu!](https://osu.ppy.sh/) skin assets.

## Developing

SVG files are optimized using [SVGO](https://github.com/svg/svgo). Refer to
[Skin set list for the ranking criteria](https://osu.ppy.sh/wiki/en/Ranking_criteria/Skin_set_list)
as a general skinning guideline.

To optimize SVG:

    make format-svg

## Building

Before building, ensure the following executables are available in `PATH`:

- magick
- python
- rsvg-convert

Build all variants:

    make

Build a specific variant (e.g. `instafade`):

    make instafade

Variant definitions can be found in the [specs/](specs) directory.

## License

SVG files are licensed under Creative Commons Zero v1.0 Universal
([LICENSE-CC0-1.0](LICENSE-CC0-1.0) or
<https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt>). Other files
are licensed under BSD Zero Clause License ([LICENSE-0BSD](LICENSE-0BSD) or
<https://opensource.org/license/0BSD>) unless explicitly stated.
