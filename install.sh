#!/bin/bash
# ─────────────────────────────────────────────────────────
# bongScript Installer for Linux/macOS
# Installs bongScript via pip
# ─────────────────────────────────────────────────────────

echo ""
echo "  ============================================"
echo "    🙏 bongScript Installer"
echo "    Bengali Programming Language"
echo "  ============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  ❌ Python 3 is not installed."
    echo "  Please install Python 3.7+ first:"
    echo "    Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "    macOS: brew install python3"
    exit 1
fi

echo "  [1/2] Installing bongScript..."
pip3 install . --user

echo "  [2/2] Verifying installation..."
echo ""

if command -v bong &> /dev/null; then
    bong --help
    echo ""
    echo "  ============================================"
    echo "    ✅ bongScript installed successfully!"
    echo ""
    echo "    Usage:"
    echo "      bong file.bong     Run a .bong file"
    echo "      bong               Start interactive REPL"
    echo "  ============================================"
else
    echo "  ⚠️  'bong' command not found in PATH."
    echo "  Try: python3 -m bongscript.cli"
    echo "  Or add ~/.local/bin to your PATH:"
    echo '    export PATH="$HOME/.local/bin:$PATH"'
fi

echo ""
