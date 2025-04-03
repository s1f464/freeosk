#!/usr/bin/env python3

import logging
import os
import shutil
import subprocess
import sys

LOG_LEVEL = logging.DEBUG

BUILD_DIR = "build"
RSVG_CONVERT_PATH = "rsvg-convert"
MAGICK_PATH = "magick"
CSS_PATH = "src/style.css"

BLANK_IMG_PATH = f"{BUILD_DIR}/blank.png"
BLANK_SPRITES = [
    "cursortrail",
    "followpoint-0",
    "followpoint-2",
    "hit300",
    "hit300g",
    "hit300k",
    "lightning",
    "sliderendcircle",
    "sliderfollowcircle",
    "spinner-bottom",
    "spinner-glow",
    "spinner-middle2",
    "spinner-spin",
    "spinner-top",
    "star2",
]

CURSOR_WIDTH = 36
CURSOR_HEIGHT = CURSOR_WIDTH

HITX_WIDTH = 24
HITX_HEIGHT = HITX_WIDTH

APPROACHCIRCLE_WIDTH = 126
APPROACHCIRCLE_HEIGHT = APPROACHCIRCLE_WIDTH

FOLLOWPOINT_WIDTH = 128
FOLLOWPOINT_HEIGHT = 1

HITCIRCLE_WIDTH = 128
HITCIRCLE_HEIGHT = HITCIRCLE_WIDTH

REVERSEARROW_WIDTH = 64
REVERSEARROW_HEIGHT = REVERSEARROW_WIDTH

DEFAULTX_WIDTH = 160
DEFAULTX_HEIGHT = DEFAULTX_WIDTH

SLIDERB_WIDTH = 256
SLIDERB_HEIGHT = SLIDERB_WIDTH

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=LOG_LEVEL)

    try:
        os.mkdir(BUILD_DIR)
    except FileExistsError:
        pass
    except Exception as err:
        logging.critical(f"Failed to create {BUILD_DIR}: {err}")
        return 1

    retcode = create_blank_image(BLANK_IMG_PATH)
    if retcode != 0:
        return 1

    for e in BLANK_SPRITES:
        dst = f"{BUILD_DIR}/{e}.png"
        shutil.copy(BLANK_IMG_PATH, dst)

    os.remove(BLANK_IMG_PATH)

    _ = render_svg(
        "src/cursor.svg", f"{BUILD_DIR}/cursor.png", CURSOR_WIDTH, CURSOR_HEIGHT
    )
    _ = render_svg(
        "src/cursor.svg",
        f"{BUILD_DIR}/cursor@2x.png",
        CURSOR_WIDTH * 2,
        CURSOR_HEIGHT * 2,
    )

    _ = render_svg("src/hit0.svg", f"{BUILD_DIR}/hit0.png", HITX_WIDTH, HITX_HEIGHT)
    _ = render_svg(
        "src/hit0.svg", f"{BUILD_DIR}/hit0@2x.png", HITX_WIDTH * 2, HITX_HEIGHT * 2
    )

    _ = render_svg("src/hit100.svg", f"{BUILD_DIR}/hit100.png", HITX_WIDTH, HITX_HEIGHT)
    _ = render_svg(
        "src/hit100.svg", f"{BUILD_DIR}/hit100@2x.png", HITX_WIDTH * 2, HITX_HEIGHT * 2
    )
    shutil.copy(f"{BUILD_DIR}/hit100.png", f"{BUILD_DIR}/hit100k.png")
    shutil.copy(f"{BUILD_DIR}/hit100@2x.png", f"{BUILD_DIR}/hit100k@2x.png")

    _ = render_svg("src/hit50.svg", f"{BUILD_DIR}/hit50.png", HITX_WIDTH, HITX_HEIGHT)
    _ = render_svg(
        "src/hit50.svg", f"{BUILD_DIR}/hit50@2x.png", HITX_WIDTH * 2, HITX_HEIGHT * 2
    )

    _ = render_svg(
        "src/approachcircle.svg",
        f"{BUILD_DIR}/approachcircle.png",
        APPROACHCIRCLE_WIDTH,
        APPROACHCIRCLE_HEIGHT,
    )
    _ = render_svg(
        "src/approachcircle.svg",
        f"{BUILD_DIR}/approachcircle@2x.png",
        APPROACHCIRCLE_WIDTH * 2,
        APPROACHCIRCLE_HEIGHT * 2,
    )

    _ = render_svg(
        "src/hitcircle.svg",
        f"{BUILD_DIR}/hitcircle.png",
        HITCIRCLE_WIDTH,
        HITCIRCLE_HEIGHT,
    )
    _ = render_svg(
        "src/hitcircle.svg",
        f"{BUILD_DIR}/hitcircle@2x.png",
        HITCIRCLE_WIDTH * 2,
        HITCIRCLE_HEIGHT * 2,
    )

    shutil.copy(f"{BUILD_DIR}/hitcircle.png", f"{BUILD_DIR}/hitcircleoverlay.png")
    shutil.copy(f"{BUILD_DIR}/hitcircle@2x.png", f"{BUILD_DIR}/hitcircleoverlay@2x.png")

    _ = render_svg(
        "src/followpoint.svg",
        f"{BUILD_DIR}/followpoint-1.png",
        FOLLOWPOINT_WIDTH,
        FOLLOWPOINT_HEIGHT,
    )
    _ = render_svg(
        "src/followpoint.svg",
        f"{BUILD_DIR}/followpoint-1@2x.png",
        FOLLOWPOINT_WIDTH * 2,
        FOLLOWPOINT_HEIGHT * 2,
    )

    _ = render_svg(
        "src/reversearrow.svg",
        f"{BUILD_DIR}/reversearrow.png",
        REVERSEARROW_WIDTH,
        REVERSEARROW_HEIGHT,
    )
    _ = render_svg(
        "src/reversearrow.svg",
        f"{BUILD_DIR}/reversearrow@2x.png",
        REVERSEARROW_WIDTH * 2,
        REVERSEARROW_HEIGHT * 2,
    )

    for x in range(10):
        _ = render_svg(
            f"src/default-{x}.svg",
            f"{BUILD_DIR}/default-{x}.png",
            DEFAULTX_WIDTH,
            DEFAULTX_HEIGHT,
        )

        _ = render_svg(
            f"src/default-{x}.svg",
            f"{BUILD_DIR}/default-{x}@2x.png",
            DEFAULTX_WIDTH * 2,
            DEFAULTX_HEIGHT * 2,
        )

    _ = render_svg(
        "src/sliderb.svg", f"{BUILD_DIR}/sliderb.png", SLIDERB_WIDTH, SLIDERB_HEIGHT
    )
    _ = render_svg(
        "src/sliderb.svg",
        f"{BUILD_DIR}/sliderb@2x.png",
        SLIDERB_WIDTH * 2,
        SLIDERB_HEIGHT * 2,
    )


def create_blank_image(output: str) -> int:
    cmd = [
        MAGICK_PATH,
        "-size",
        "1x1",
        "xc:transparent",
        "-colors",
        "1",
        "-strip",
        output,
    ]
    logging.debug(" ".join(cmd))
    proc = subprocess.run(cmd)
    return proc.returncode


def render_svg(src: str, dst: str, width: int, height: int) -> int:
    cmd = [
        RSVG_CONVERT_PATH,
        "-w",
        str(width),
        "-h",
        str(height),
        "-s",
        CSS_PATH,
        "-o",
        dst,
        src,
    ]
    logging.debug(" ".join(cmd))
    proc = subprocess.run(cmd)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
