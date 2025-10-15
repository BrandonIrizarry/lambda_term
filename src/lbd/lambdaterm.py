#!/usr/bin/env python

import argparse

import lambda_term.repl as repl
from load import load

ap = argparse.ArgumentParser(
    description="""A lightweight programming language, based on functional paradigms."""
)

ap.add_argument("-l", "--load", nargs=1, default=[], help="""Execute, as well as load any
defintions into REPL.""")

args = ap.parse_args()


def main():
    err_msg = load(args.load)

    # Don't launch the REPL if any file had an error.
    if err_msg is not None:
        print(err_msg)
        return

    repl.repl()


if __name__ == "__main__":
    main()
