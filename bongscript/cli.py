#!/usr/bin/env python3
"""
বংScript (bongScript) — CLI Entry Point

This module is the console_scripts entry point for the `bong` command.
After `pip install bongscript`, users can run:
    bong <filename.bong>     Run a .bong file
    bong                     Start interactive REPL
    bong --help              Show help
"""

import sys
import os

from .lexer import Lexer, LexerError
from .parser import Parser, ParserError
from .interpreter import Interpreter, BongRuntimeError


# ─── Colors (ANSI) ──────────────────────────────────────────────────────────────

class Colors:
    RESET   = "\033[0m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"


def colored(text, color):
    """Wrap text with ANSI color codes."""
    return f"{color}{text}{Colors.RESET}"


# ─── Core Runner ────────────────────────────────────────────────────────────────

def run(source: str, interpreter: Interpreter = None) -> Interpreter:
    """Lex, parse, and interpret bongScript source code."""
    if interpreter is None:
        interpreter = Interpreter()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter.interpret(program)
    except (LexerError, ParserError, BongRuntimeError) as e:
        print(colored(f"  {e}", Colors.RED))

    return interpreter


def run_file(filename: str):
    """Run a .bong file."""
    if not os.path.exists(filename):
        print(colored(f"  File ta paowa jacchhe na: {filename}", Colors.RED))
        print(colored(f"  (File not found: {filename})", Colors.DIM))
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    run(source)


# ─── Interactive REPL ───────────────────────────────────────────────────────────

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║        🙏 নমস্কার! bongScript এ স্বাগতম!                  ║
║           Nomoskar! Welcome to bongScript!                ║
╠═══════════════════════════════════════════════════════════╣
║  Version 1.0   |   .bong files supported                 ║
║  Type 'help' for keywords  |  'baire' to exit            ║
╚═══════════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
╔══════════════════════════════════════════════════════════════════════╗
║                    bongScript — Keyword Reference                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  Keyword          Bengali      English     Example                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  dhoro            ধরো          let/var     dhoro x = 10             ║
║  dekhao           দেখাও         print       dekhao("hello")          ║
║  nao              নাও          input       dhoro x = nao("naam: ")  ║
║  jodi...tahole    যদি...তাহলে   if...then   jodi x > 5 tahole       ║
║  nahole           নাহলে         else        nahole                   ║
║  nahole jodi      নাহলে যদি     else if     nahole jodi x > 3 tahole║
║  ses              শেষ          end         ses                      ║
║  jotokhon         যতক্ষণ        while       jotokhon x < 10 tahole  ║
║  kaj              কাজ          function    kaj jog(a, b)            ║
║  ferao            ফেরাও         return      ferao a + b              ║
║  sotti            সত্যি         true        dhoro flag = sotti       ║
║  mittha           মিথ্যা        false       dhoro flag = mittha      ║
║  khali            খালি         null        dhoro x = khali          ║
║  ebong            এবং          and         jodi x > 0 ebong x < 10 ║
║  othoba           অথবা         or          jodi x == 0 othoba y == 1║
║  na               না           not         jodi na sotti            ║
║  thamo            থামো         break       thamo                    ║
╠══════════════════════════════════════════════════════════════════════╣
║  Built-in Functions:                                                ║
║  dorjho(x)/len(x)     Length of string/list                         ║
║  sonkhya(x)            Convert to number                            ║
║  likhon(x)             Convert to string                            ║
║  dhoron(x)/type(x)     Get type name                                ║
║  purno(x)              Convert float to integer                     ║
║  golakrito(x, n)       Round number to n decimals                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  Operators:  +  -  *  /  %  ==  !=  <  >  <=  >=                   ║
║  Comments:   # ei line ta comment    // ei o comment                ║
║  Lists:      dhoro nums = [1, 2, 3]  dekhao(nums[0])               ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def repl():
    """Start an interactive REPL session."""
    print(colored(BANNER, Colors.CYAN))

    interpreter = Interpreter()
    block_starters = {"jodi", "jotokhon", "kaj", "যদি", "যতক্ষণ", "কাজ"}

    while True:
        try:
            line = input(colored("\nবং> ", Colors.GREEN + Colors.BOLD))
            stripped = line.strip()

            # Exit commands
            if stripped in ("baire", "বাইরে", "exit", "quit"):
                print(colored("\n  👋 আবার দেখা হবে! (See you again!)\n", Colors.CYAN))
                break

            # Help
            if stripped == "help":
                print(colored(HELP_TEXT, Colors.YELLOW))
                continue

            if not stripped:
                continue

            # Multi-line block input
            if any(stripped.startswith(kw) for kw in block_starters):
                lines = [line]
                depth = 1
                while depth > 0:
                    try:
                        continuation = input(colored("...  ", Colors.DIM))
                    except (KeyboardInterrupt, EOFError):
                        print()
                        depth = 0
                        lines = []
                        break
                    lines.append(continuation)
                    cont_stripped = continuation.strip()
                    # Count block openings
                    for kw in block_starters:
                        if cont_stripped.startswith(kw):
                            depth += 1
                    # Count block closings
                    if cont_stripped in ("ses", "শেষ"):
                        depth -= 1

                if not lines:
                    continue
                line = "\n".join(lines)

            interpreter = run(line, interpreter)

        except KeyboardInterrupt:
            print(colored("\n\n  👋 আবার দেখা হবে! (See you again!)\n", Colors.CYAN))
            break
        except EOFError:
            print(colored("\n\n  👋 আবার দেখা হবে! (See you again!)\n", Colors.CYAN))
            break


# ─── CLI Entry Point ────────────────────────────────────────────────────────────

USAGE = """
বংScript (bongScript) — Bengali Programming Language

Usage:
    bong                        Start interactive REPL
    bong <file.bong>            Run a bongScript file
    bong --help                 Show this help

Examples:
    bong hello.bong
    bong examples/fibonacci.bong
"""


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("--help", "-h", "help"):
            print(USAGE)
            sys.exit(0)
        run_file(arg)
    else:
        repl()


if __name__ == "__main__":
    main()
