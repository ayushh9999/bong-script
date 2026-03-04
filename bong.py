#!/usr/bin/env python3
"""
বংScript (bongScript) — A Bengali Programming Language

Usage:
    python bong.py <filename.bong>     Run a .bong file
    python bong.py                     Start interactive REPL
    python bong.py --help              Show help

After installing with pip, use the `bong` command instead:
    bong <filename.bong>
    bong
"""

from bongscript.cli import main

if __name__ == "__main__":
    main()
