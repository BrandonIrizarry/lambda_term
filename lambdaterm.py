#!/usr/bin/env python

import argparse
import sys

import lbd.directive as dtv
import lbd.evaluate as evl
import lbd.repl as repl
from lbd.error import LambdaError
from lbd.term import AST

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


def process_filename(filename: str) -> AST | LambdaError:
    """Process filename.

    """
    program = dtv.load_d(filename)

    if isinstance(program, Exception):
        return program

    ast = evl.eval_program(program)

    if isinstance(ast, Exception):
        return ast

    return ast


def main():
    filename: str = args.filename

    # Fill in the global environment with the given program
    if filename:
        processed = process_filename(filename)

        if isinstance(processed, LambdaError):
            print(processed)
            sys.exit(1)

        value = processed

        # If only the name of a program is given (no --repl), print
        # the program's final evaluation, and exit.
        if not args.repl:
            print(value)
            sys.exit(0)

    # In every other case, launch the REPL, possibly with a
    # pre-populated global environment.
    repl.repl()


if __name__ == "__main__":
    main()
