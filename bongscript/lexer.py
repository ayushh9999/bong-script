"""
Lexer (Tokenizer) for bongScript.
Converts raw source code into a stream of tokens.
Supports Bengali Unicode characters in identifiers and keywords.
"""

from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """Error raised during tokenization."""

    def __init__(self, message: str, line: int, column: int):
        self.line = line
        self.column = column
        super().__init__(f"ভুল (Lexer Error) line {line}, column {column}: {message}")


class Lexer:
    """Tokenizes bongScript source code."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    # ─── Character Helpers ──────────────────────────────────────────────────

    def _at_end(self) -> bool:
        return self.pos >= len(self.source)

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        return self.source[self.pos]

    def _peek_next(self) -> str:
        if self.pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.pos + 1]

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _is_identifier_start(self, ch: str) -> bool:
        """Check if character can start an identifier (letters, _, or Bengali Unicode)."""
        return ch.isalpha() or ch == "_" or ord(ch) > 127

    def _is_identifier_char(self, ch: str) -> bool:
        """Check if character can continue an identifier."""
        return ch.isalnum() or ch == "_" or ord(ch) > 127

    # ─── Skippers ───────────────────────────────────────────────────────────

    def _skip_whitespace(self):
        """Skip spaces, tabs, and carriage returns (NOT newlines)."""
        while not self._at_end() and self.source[self.pos] in (" ", "\t", "\r"):
            self._advance()

    def _skip_comment(self):
        """Skip single-line comment until end of line."""
        while not self._at_end() and self.source[self.pos] != "\n":
            self._advance()

    # ─── Token Readers ──────────────────────────────────────────────────────

    def _read_string(self, quote: str) -> Token:
        """Read a string literal enclosed in matching quotes."""
        start_line = self.line
        start_col = self.column
        self._advance()  # skip opening quote

        result = ""
        while not self._at_end() and self.source[self.pos] != quote:
            if self.source[self.pos] == "\\":
                self._advance()  # skip backslash
                if self._at_end():
                    raise LexerError(
                        "String er moddhe escape sequence sesh hoyni (Unterminated escape)",
                        start_line, start_col,
                    )
                ch = self._advance()
                escape_map = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'", "0": "\0"}
                result += escape_map.get(ch, "\\" + ch)
            else:
                result += self._advance()

        if self._at_end():
            raise LexerError(
                "String ta close kora hoyni (Unterminated string literal)",
                start_line, start_col,
            )

        self._advance()  # skip closing quote
        return Token(TokenType.STRING, result, start_line, start_col)

    def _read_number(self) -> Token:
        """Read a numeric literal (integer or float)."""
        start_line = self.line
        start_col = self.column
        result = ""
        has_dot = False

        while not self._at_end() and (self.source[self.pos].isdigit() or self.source[self.pos] == "."):
            if self.source[self.pos] == ".":
                if has_dot:
                    break  # second dot — stop
                has_dot = True
            result += self._advance()

        value = float(result) if has_dot else int(result)
        return Token(TokenType.NUMBER, value, start_line, start_col)

    def _read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start_line = self.line
        start_col = self.column
        result = ""

        while not self._at_end() and self._is_identifier_char(self.source[self.pos]):
            result += self._advance()

        token_type = KEYWORDS.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, start_line, start_col)

    # ─── Main Tokenizer ────────────────────────────────────────────────────

    def tokenize(self) -> list:
        """Convert source code into a list of tokens."""
        tokens = []

        while not self._at_end():
            self._skip_whitespace()

            if self._at_end():
                break

            ch = self.source[self.pos]
            start_line = self.line
            start_col = self.column

            # ── Comments ──
            if ch == "#":
                self._skip_comment()
                continue
            if ch == "/" and self._peek_next() == "/":
                self._skip_comment()
                continue

            # ── Newlines ──
            if ch == "\n":
                if tokens and tokens[-1].type != TokenType.NEWLINE:
                    tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                self._advance()
                continue

            # ── Strings ──
            if ch in ('"', "'"):
                tokens.append(self._read_string(ch))
                continue

            # ── Numbers ──
            if ch.isdigit():
                tokens.append(self._read_number())
                continue

            # ── Identifiers & Keywords ──
            if self._is_identifier_start(ch):
                tokens.append(self._read_identifier())
                continue

            # ── Two-character operators ──
            two_char = ch + self._peek_next() if not self._at_end() else ""
            if two_char == "==":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.EQUAL, "==", start_line, start_col))
                continue
            if two_char == "!=":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.NOT_EQUAL, "!=", start_line, start_col))
                continue
            if two_char == "<=":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.LESS_EQ, "<=", start_line, start_col))
                continue
            if two_char == ">=":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.GREATER_EQ, ">=", start_line, start_col))
                continue

            # ── Single-character operators & punctuation ──
            single_char_map = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.STAR,
                "/": TokenType.SLASH,
                "%": TokenType.PERCENT,
                "=": TokenType.ASSIGN,
                "<": TokenType.LESS,
                ">": TokenType.GREATER,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                ",": TokenType.COMMA,
                "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET,
            }

            if ch in single_char_map:
                self._advance()
                tokens.append(Token(single_char_map[ch], ch, start_line, start_col))
                continue

            # ── Unknown character ──
            raise LexerError(
                f"Ei character ta chena jacchhe na: '{ch}' (Unexpected character: '{ch}')",
                start_line, start_col,
            )

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
