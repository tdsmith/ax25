import argparse
import sys

from .kiss import KissStream
from .version import __version__


def parse_main():
    parser = argparse.ArgumentParser(
        description="Parses AX.25 frames from KISS TNC output"
    )
    parser.add_argument("--version", "-V", action="version",
                        version="%(prog)s " + __version__)
    parser.add_argument("filename", default="-", nargs="?")
    args = parser.parse_args()

    if args.filename == "-":
        f = sys.stdin.buffer
    else:
        f = open(args.filename, "rb")

    for frame in KissStream(f):
        print(frame)

    f.close()
    sys.exit(0)
