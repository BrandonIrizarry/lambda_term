#!/usr/bin/env python

import argparse
import sys
from typing import Any

import lbd.directive as dtv
import lbd.evaluate as evl
import lbd.repl as repl

ap = argparse.ArgumentParser(
    description="""A lightweight programming language, based on functional paradigms."""
)

ap.add_argument("filename", nargs="?", help="Execute this source file.")

ap.add_argument(
    "-r",
    "--repl",
    help="""When FILENAME is provided, load result and definitions
    into a new REPL session.""",
    action="store_true"
)

args = ap.parse_args()


# FIXME: This might have to return a tuple of the last evaluation,
# coupled with the genv.
def process_filename(filename: str) -> tuple[evl.Genv, dict[str, Any]] | Exception:
    """Process filename.

    """
    genv: evl.Genv = []

    program = dtv.load_d(filename)

    if isinstance(program, Exception):
        return program

    ast = evl.eval_program(program, genv)

    if isinstance(ast, Exception):
        return ast

    return (genv, ast)


def main():
    filename: str = args.filename
    genv: evl.Genv = []

    # Fill in the global environment with the given program
    if filename:
        processed = process_filename(filename)

        if isinstance(processed, Exception):
            print(processed)
            sys.exit(1)

        fgenv, value = processed

        # Extend the initial genv with the given program.
        genv.extend(fgenv)

        # If only the name of a program is given (no --repl), print
        # the program's final evaluation, and exit.
        if not args.repl:
            print(value)
            sys.exit(0)

    # In every other case, launch the REPL, possibly with a
    # pre-populated global environment.
    repl.repl(genv)


if __name__ == "__main__":
    main()
