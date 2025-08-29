#!/usr/bin/env python

import argparse

import lbd.repl as repl

ap = argparse.ArgumentParser(
    description="""A lightweight programming language, based on functional paradigms."""
)


args = ap.parse_args()


def main():
    repl.repl()


if __name__ == "__main__":
    main()
