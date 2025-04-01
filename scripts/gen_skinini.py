#!/usr/bin/env python3

import argparse
import configparser
import subprocess
import sys

GIT_PATH = "git"
SKIN_INI_INPUT = "src/skin.ini"
SKIN_INI_OUTPUT = "build/skin.ini"


def main():
    args = parse_args()

    commit_hash = get_latest_commit_hash()
    commit_date = get_latest_commit_date()

    config = configparser.ConfigParser(comment_prefixes="//", delimiters=[":"])
    config.optionxform = lambda option: option

    with open(SKIN_INI_INPUT, "r") as f:
        config.read_file(f)
        config["General"]["Name"] += f" ({commit_hash} {commit_date})"
        config["General"]["Author"] = args.author

    with open(SKIN_INI_OUTPUT, "w") as f:
        config.write(f)


def get_latest_commit_hash() -> str:
    cmd = [GIT_PATH, "rev-parse", "--short", "HEAD"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return "unknown"
    return str(proc.stdout.strip())


def get_latest_commit_date() -> str:
    cmd = [GIT_PATH, "log", "-1", "--format=%ad", "--date", "format:%Y-%m-%d"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return "unknown"
    return str(proc.stdout.strip())


def parse_args():
    parser = argparse.ArgumentParser()

    _ = parser.add_argument(
        "--author", default="Unknown", metavar="NAME", help="set author"
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
