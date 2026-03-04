"""
Token types and keyword mappings for bongScript.
Supports both transliterated Bengali (Banglish) and Unicode Bengali (বাংলা) keywords.
"""

from enum import Enum, auto


class TokenType(Enum):
    # ─── Literals ───
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # ─── Keywords (Bengali) ───
    DHORO = auto()          # ধরো      → let / var
    DEKHAO = auto()         # দেখাও     → print
    JODI = auto()           # যদি      → if
    TAHOLE = auto()         # তাহলে     → then
    NAHOLE = auto()         # নাহলে     → else
    SES = auto()            # শেষ      → end
    JOTOKHON = auto()       # যতক্ষণ    → while
    KAJ = auto()            # কাজ      → function
    FERAO = auto()          # ফেরাও     → return
    NAO = auto()            # নাও      → input
    SOTTI = auto()          # সত্যি     → true
    MITTHA = auto()         # মিথ্যা    → false
    KHALI = auto()          # খালি     → null / none
    EBONG = auto()          # এবং      → and
    OTHOBA = auto()         # অথবা     → or
    NA = auto()             # না       → not
    THAMO = auto()          # থামো     → break

    # ─── Operators ───
    PLUS = auto()           # +
    MINUS = auto()          # -
    STAR = auto()           # *
    SLASH = auto()          # /
    PERCENT = auto()        # %
    ASSIGN = auto()         # =
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    LESS = auto()           # <
    GREATER = auto()        # >
    LESS_EQ = auto()        # <=
    GREATER_EQ = auto()     # >=

    # ─── Punctuation ───
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    COMMA = auto()          # ,
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]

    # ─── Special ───
    NEWLINE = auto()
    EOF = auto()


class Token:
    """Represents a single token with type, value, and position info."""

    def __init__(self, type: TokenType, value, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"


# ─── Keyword Mappings ───────────────────────────────────────────────────────────
# Both transliterated (Banglish) and Unicode Bengali script are supported.

KEYWORDS = {
    # Transliterated (Banglish)
    "dhoro":     TokenType.DHORO,
    "dekhao":    TokenType.DEKHAO,
    "jodi":      TokenType.JODI,
    "tahole":    TokenType.TAHOLE,
    "nahole":    TokenType.NAHOLE,
    "ses":       TokenType.SES,
    "jotokhon":  TokenType.JOTOKHON,
    "kaj":       TokenType.KAJ,
    "ferao":     TokenType.FERAO,
    "nao":       TokenType.NAO,
    "sotti":     TokenType.SOTTI,
    "mittha":    TokenType.MITTHA,
    "khali":     TokenType.KHALI,
    "ebong":     TokenType.EBONG,
    "othoba":    TokenType.OTHOBA,
    "na":        TokenType.NA,
    "thamo":     TokenType.THAMO,

    # Bengali Script (বাংলা)
    "ধরো":       TokenType.DHORO,
    "দেখাও":     TokenType.DEKHAO,
    "যদি":       TokenType.JODI,
    "তাহলে":     TokenType.TAHOLE,
    "নাহলে":     TokenType.NAHOLE,
    "শেষ":       TokenType.SES,
    "যতক্ষণ":    TokenType.JOTOKHON,
    "কাজ":       TokenType.KAJ,
    "ফেরাও":     TokenType.FERAO,
    "নাও":       TokenType.NAO,
    "সত্যি":     TokenType.SOTTI,
    "মিথ্যা":    TokenType.MITTHA,
    "খালি":      TokenType.KHALI,
    "এবং":       TokenType.EBONG,
    "অথবা":      TokenType.OTHOBA,
    "না":        TokenType.NA,
    "থামো":      TokenType.THAMO,
}
