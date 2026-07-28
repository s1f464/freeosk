# freeosk

Minimalist [osu!](https://osu.ppy.sh/) skin assets.

## Developing

Refer to
[Skin set list for the ranking criteria](https://osu.ppy.sh/wiki/en/Ranking_criteria/Skin_set_list)
as a general skinning guideline.

SVG files are optimized using [SVGO](https://github.com/svg/svgo):

    make format-svg

## Building

A [Makefile](Makefile) is provided for building `.osk`. It automatically
downloads hitsounds from [osu-resources](https://github.com/ppy/osu-resources)
([CC-BY-NC-4.0](https://raw.githubusercontent.com/ppy/osu-resources/refs/heads/master/LICENCE.md)).

Before building, ensure the following executables are available in `PATH`:

- bsdtar
- curl
- magick
- python
- rsvg-convert
- tar

Build all variants:

    make

Build a specific variant (e.g. `triple_stacked`):

    make triple_stacked

Variant definitions can be found in the [specs/](specs) directory.

## License

SVG files are licensed under Creative Commons Zero v1.0 Universal
([LICENSE-CC0-1.0](LICENSE-CC0-1.0) or
<https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt>). Other files
are licensed under BSD Zero Clause License ([LICENSE-0BSD](LICENSE-0BSD) or
<https://opensource.org/license/0BSD>) unless explicitly stated.
