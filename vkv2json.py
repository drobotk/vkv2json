#!/usr/bin/env python3

import argparse
import json
import os
import re


__version__ = "0.1.1"
__all__ = ("parse",)


def parse(text: str, i: int = 0) -> tuple[list, int]:
    out = []
    key = None
    while i < len(text):
        c = text[i]
        if c == '"':
            end = text.index('"', i + 1)
            buf = text[i + 1 : end]
            i = end + 1

            if not key:
                key = buf
            else:
                out.append({key: buf})
                key = None
        elif c == "{":
            i += 1
            assert key
            o, i = parse(text, i)
            out.append({key: o})
            key = None
        elif c == "}":
            i += 1
            break
        else:
            i += 1

    return out, i


def main():
    # fmt: off
    parser = argparse.ArgumentParser(description='Convert Valve KeyValue files into JSON')
    parser.add_argument("--version",    action="version", version=__version__)
    parser.add_argument("-o", "--out",  metavar="FILE", help="Output file")
    parser.add_argument("file",         metavar="FILE", help="Input file")
    # fmt: on

    args = parser.parse_args()

    with open(args.file) as f:
        text = f.read()

    # Remove comments
    text = re.sub(r"//.+?\n", "\n", text)

    out, _ = parse(text)

    outfile = args.out
    if not outfile:
        outfile = os.path.basename(args.file) + ".json"

    with open(outfile, "w") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
