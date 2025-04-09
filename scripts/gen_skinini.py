#!/usr/bin/env python3

import argparse
import configparser
import subprocess
import sys

DEFAULT_AUTHOR = "Unknown"
DEFAULT_GIT = "git"
DEFAULT_INPUT = "src/skin.ini"
DEFAULT_OUTPUT = "build/skin.ini"


def main():
    args = parse_args()

    commit_hash = get_latest_commit_hash(args.git)
    commit_date = get_latest_commit_date(args.git)

    config = configparser.ConfigParser(comment_prefixes="//", delimiters=[":"])
    config.optionxform = lambda option: option

    with open(args.input, "r") as f:
        config.read_file(f)
        config["General"]["Name"] += f" ({commit_hash} {commit_date})"
        config["General"]["Author"] = args.author

    with open(args.output, "w") as f:
        config.write(f)


def get_latest_commit_hash(git: str) -> str:
    cmd = [git, "rev-parse", "--short", "HEAD"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return "unknown"
    return str(proc.stdout.strip())


def get_latest_commit_date(git: str) -> str:
    cmd = [git, "log", "-1", "--format=%ad", "--date", "format:%Y-%m-%d"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return "unknown"
    return str(proc.stdout.strip())


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    _ = parser.add_argument(
        "--author", default=DEFAULT_AUTHOR, help="set author", metavar="NAME"
    )

    _ = parser.add_argument(
        "--git", default=DEFAULT_GIT, help="path to git", metavar="PATH"
    )

    _ = parser.add_argument(
        "-i", "--input", default=DEFAULT_INPUT, help="path to input", metavar="PATH"
    )

    _ = parser.add_argument(
        "-o", "--output", default=DEFAULT_OUTPUT, help="path to output", metavar="PATH"
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
