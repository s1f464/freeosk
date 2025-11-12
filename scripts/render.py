#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import PurePath
import shutil
import subprocess
import sys
import json

LOG_LEVEL = logging.DEBUG

DEFAULT_BUILD_DIR = "build"
DEFAULT_SPEC = "specs/triple_stacked.json"
DEFAULT_HD_MULTIPLIER = 2
DEFAULT_RSVG_CONVERT = "rsvg-convert"
DEFAULT_MAGICK = "magick"

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=LOG_LEVEL)

    args = parse_args()

    try:
        os.mkdir(args.build_dir)
    except FileExistsError:
        pass
    except Exception as err:
        logging.critical(f"Failed to create {args.build_dir}: {err}")
        return 1

    blank_image_path = PurePath(args.build_dir).joinpath("blank.png")
    retcode = create_blank_image(args.magick, str(blank_image_path))
    if retcode != 0:
        return 1

    with open(args.spec) as f:
        spec = json.load(f)

    for sprite in spec["sprites"]:
        dst = PurePath(args.build_dir).joinpath(sprite["name"])
        dst_hd = dst.with_stem(f"{dst.stem}@2x")

        if "blank" in sprite and sprite["blank"]:
            logger.debug(f"Copying {blank_image_path} to {dst}.")
            shutil.copy(blank_image_path, dst)
            continue

        height = sprite["height"] if "height" in sprite else sprite["width"]

        retcode = render_svg(
            args.rsvg_convert, sprite["src"], str(dst), sprite["width"], height
        )
        if retcode != 0:
            logger.warning(f"Non-zero return code: {retcode}.")
        retcode = render_svg(
            args.rsvg_convert,
            sprite["src"],
            str(dst_hd),
            sprite["width"] * args.hd_multiplier,
            height * args.hd_multiplier,
        )
        if retcode != 0:
            logger.warning(f"Non-zero return code: {retcode}.")

    os.remove(blank_image_path)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    _ = parser.add_argument(
        "--build-dir", default=DEFAULT_BUILD_DIR, help="build directory", metavar="PATH"
    )

    _ = parser.add_argument(
        "--spec", default=DEFAULT_SPEC, help="path to spec", metavar="PATH"
    )

    _ = parser.add_argument(
        "--hd-multiplier",
        default=DEFAULT_HD_MULTIPLIER,
        type=float,
        help="hd multiplier",
        metavar="NUM",
    )

    _ = parser.add_argument(
        "--rsvg-convert",
        default=DEFAULT_RSVG_CONVERT,
        help="path to rsvg-convert",
        metavar="PATH",
    )

    _ = parser.add_argument(
        "--magick", default=DEFAULT_MAGICK, help="path to magick", metavar="PATH"
    )

    return parser.parse_args()


def create_blank_image(magick: str, output: str) -> int:
    cmd = [
        magick,
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


def render_svg(
    rsvg_convert: str, src: str, dst: str, width: float, height: float
) -> int:
    cmd = [
        rsvg_convert,
        "-w",
        str(width),
        "-h",
        str(height),
        "-o",
        dst,
        src,
    ]
    logging.debug(" ".join(cmd))
    proc = subprocess.run(cmd)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
