#!/usr/bin/env python

import argparse

import lbd.error as error
import lbd.evaluate as evl
import lbd.repl as repl

ap = argparse.ArgumentParser(
    description="""A lightweight programming language, based on functional paradigms."""
)

ap.add_argument("-l", "--load", nargs=1, default=[], help="""Execute, as well as load any
defintions into REPL.""")

args = ap.parse_args()


def load(filenames: list[str]) -> str | None:
    for filename in filenames:
        with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip()

                if line != "":
                    err = evl.eval_raw_term(line)

                    if isinstance(err, error.LambdaError):
                        return f"in '{filename}': {err}"


def main():
    err_msg = load(args.load)

    # Don't launch the REPL if any file had an error.
    if err_msg is not None:
        print(err_msg)
        return

    repl.repl()


if __name__ == "__main__":
    main()
