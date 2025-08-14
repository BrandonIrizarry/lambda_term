#!/usr/bin/env python

import argparse
import sys

import directive as dtv
import evaluate as evl
import repl
import status

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
def process_filename(filename: str) -> status.Status:
    """Process filename.

    """
    genv: evl.Genv = []

    loaded = dtv.load_d(filename)

    if loaded["error"]:
        return loaded

    program = loaded["user_data"]

    evaled = evl.eval_program(program, genv)

    if evaled["error"]:
        return evaled

    value = evaled["user_data"]

    return {"user_data": (genv, value), "error": None}


def main():
    filename: str = args.filename
    genv: evl.Genv = []

    # Fill in the global environment with the given program
    if filename:
        processed = process_filename(filename)

        if err := processed["error"]:
            print(err)
            sys.exit(1)

        fgenv, value = processed["user_data"]

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
