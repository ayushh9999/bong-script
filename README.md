# BongScript

### A Bengali Programming Language

<div align="center">

**Write code in Bengali — using transliterated Banglish or pure বাংলা script!**

</div>

---

## � Installation

### Windows (Standalone — No Python needed!)

**Option 1: Download the `.exe` (easiest)**
1. Go to [Releases](https://github.com/AyushMondal/bongScript/releases)
2. Download `bong.exe`
3. Put it in any folder and run from terminal:
   ```
   bong.exe hello.bong
   ```

**Option 2: Clone and install**
```powershell
git clone https://github.com/AyushMondal/bongScript.git
cd bongScript
install.bat
```
This copies `bong.exe` to your system and adds it to PATH. Restart terminal, then:
```
bong hello.bong
```

### Linux / macOS (requires Python 3.7+)

```bash
git clone https://github.com/AyushMondal/bongScript.git
cd bongScript
chmod +x install.sh
./install.sh
```

### pip install (any OS with Python)

```bash
pip install git+https://github.com/AyushMondal/bongScript.git
bong hello.bong
```

---

## 🚀 Quick Start

```bash
bong examples/hello.bong       # Run a .bong file
bong                           # Start interactive REPL
```

## 📝 Your First Program

Create a file called `hello.bong`:

```
dhoro naam = "Ayush"
dekhao("🙏 Nomoskar,", naam, "!")

jodi 5 > 3 tahole
    dekhao "Haan, 5 boro!"
ses
```

Run it:
```bash
python bong.py hello.bong
```

---

## 📖 Language Reference

### Variables (`dhoro` / `ধরো`)
```
dhoro x = 10
dhoro naam = "Rahim"
dhoro pi = 3.14159
dhoro active = sotti          # true
dhoro deleted = mittha        # false
dhoro nothing = khali         # null
dhoro fruits = ["আম", "লিচু"]  # list
```

### Print (`dekhao` / `দেখাও`)
```
dekhao("Hello, World!")
dekhao "Bracket chara o hoy!"       # without parens
dekhao("Naam:", naam, "Boyosh:", 25) # multiple values
```

### Input (`nao` / `নাও`)
```
dhoro naam = nao("Tomar naam ki? ")
dhoro age = sonkhya(nao("Boyosh: "))  # convert to number
```

### If / Else (`jodi` / `tahole` / `nahole` / `ses`)
```
jodi marks >= 90 tahole
    dekhao "A+"
nahole jodi marks >= 80 tahole
    dekhao "A"
nahole jodi marks >= 70 tahole
    dekhao "B"
nahole
    dekhao "Try again!"
ses
```

### While Loop (`jotokhon` / `যতক্ষণ`)
```
dhoro i = 1
jotokhon i <= 10 tahole
    dekhao(i)
    dhoro i = i + 1
ses
```

### Functions (`kaj` / `কাজ`)
```
kaj jog(a, b)
    ferao a + b
ses

kaj factorial(n)
    jodi n <= 1 tahole
        ferao 1
    ses
    ferao n * factorial(n - 1)
ses

dekhao(jog(3, 4))         # 7
dekhao(factorial(5))       # 120
```

### Lists
```
dhoro colors = ["lal", "nil", "sabuj"]
dekhao(colors[0])          # "lal"
dekhao(dorjho(colors))     # 3
```

### Operators
| Operator | Meaning | Example |
|----------|---------|---------|
| `+` | Addition / Concat | `5 + 3` or `"a" + "b"` |
| `-` | Subtraction | `10 - 4` |
| `*` | Multiplication | `6 * 7` |
| `/` | Division | `15 / 4` |
| `%` | Modulo | `10 % 3` |
| `==` | Equal | `x == 5` |
| `!=` | Not Equal | `x != 0` |
| `<` `>` `<=` `>=` | Comparison | `x >= 10` |
| `ebong` / `এবং` | Logical AND | `x > 0 ebong x < 10` |
| `othoba` / `অথবা` | Logical OR | `x == 0 othoba x == 1` |
| `na` / `না` | Logical NOT | `na sotti` |

---

## 🗝️ Complete Keyword Map

| Banglish | বাংলা | English | Usage |
|----------|--------|---------|-------|
| `dhoro` | `ধরো` | let/var | Variable declaration |
| `dekhao` | `দেখাও` | print | Output to console |
| `nao` | `নাও` | input | Read user input |
| `jodi` | `যদি` | if | Conditional start |
| `tahole` | `তাহলে` | then | Conditional block start |
| `nahole` | `নাহলে` | else | Alternative branch |
| `ses` | `শেষ` | end | Block terminator |
| `jotokhon` | `যতক্ষণ` | while | Loop |
| `kaj` | `কাজ` | function | Function declaration |
| `ferao` | `ফেরাও` | return | Return value |
| `sotti` | `সত্যি` | true | Boolean true |
| `mittha` | `মিথ্যা` | false | Boolean false |
| `khali` | `খালি` | null | Null/None |
| `ebong` | `এবং` | and | Logical AND |
| `othoba` | `অথবা` | or | Logical OR |
| `na` | `না` | not | Logical NOT |
| `thamo` | `থামো` | break | Break out of loop |

## 🔧 Built-in Functions

| Function | Bengali Alt | Description |
|----------|-------------|-------------|
| `len(x)` | `dorjho(x)` | Length of string/list |
| `sonkhya(x)` | — | Convert to number |
| `likhon(x)` | — | Convert to string |
| `type(x)` | `dhoron(x)` | Get type name |
| `purno(x)` | — | Convert float to int |
| `golakrito(x, n)` | — | Round to n decimals |

---

## 🎮 Interactive REPL

Start the REPL with no arguments:

```bash
python bong.py
```

```
╔═══════════════════════════════════════════════════════════╗
║        🙏 নমস্কার! bongScript এ স্বাগতম!                  ║
║           Nomoskar! Welcome to bongScript!                ║
╠═══════════════════════════════════════════════════════════╣
║  Version 1.0   |   .bong files supported                 ║
║  Type 'help' for keywords  |  'baire' to exit            ║
╚═══════════════════════════════════════════════════════════╝

বং> dhoro x = 42
বং> dekhao(x * 2)
84
বং> baire
  👋 আবার দেখা হবে! (See you again!)
```

## 📁 Examples

| File | Description |
|------|-------------|
| `examples/hello.bong` | Hello World & basics |
| `examples/fibonacci.bong` | Recursive & iterative Fibonacci |
| `examples/calculator.bong` | Arithmetic functions |
| `examples/fizzbuzz.bong` | Classic FizzBuzz, Bengali style |
| `examples/showcase.bong` | All features demonstrated |
| `examples/bangla_script.bong` | Pure Bengali (বাংলা) script |

## 🏗️ Architecture

```
bongScript/
├── bong.py                  # CLI entry point & REPL
├── bongscript/
│   ├── __init__.py
│   ├── tokens.py            # Token types & keyword maps
│   ├── lexer.py             # Tokenizer (source → tokens)
│   ├── parser.py            # Parser (tokens → AST)
│   ├── ast_nodes.py         # AST node definitions
│   └── interpreter.py       # Tree-walking interpreter
├── examples/                # Example .bong programs
└── README.md
```

**Pipeline:** Source Code → **Lexer** → Tokens → **Parser** → AST → **Interpreter** → Output

---

## 🌟 Features

- ✅ Bengali keywords (both Banglish & বাংলা script)
- ✅ Variables, strings, numbers, booleans, null
- ✅ Arithmetic & comparison operators
- ✅ If / else if / else conditionals
- ✅ While loops with break
- ✅ User-defined functions with closures
- ✅ Recursion support
- ✅ Lists with indexing
- ✅ User input
- ✅ Built-in utility functions
- ✅ Interactive REPL with multi-line support
- ✅ Helpful error messages in Bengali + English
- ✅ Comments (`#` and `//`)

---

<div align="center">

**বংScript** — কোডিং এখন বাংলায়! 🇧🇩

Made with ❤️ for the Bengali developer community

</div>
