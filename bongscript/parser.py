"""
Recursive Descent Parser for bongScript.
Converts a stream of tokens into an Abstract Syntax Tree (AST).

Grammar Overview:
    program     → statement*
    statement   → var_decl | print_stmt | if_stmt | while_stmt
                | func_decl | return_stmt | break_stmt | assignment | expr_stmt
    var_decl    → 'dhoro' IDENTIFIER '=' expression
    print_stmt  → 'dekhao' '(' expr_list ')' | 'dekhao' expression
    if_stmt     → 'jodi' expr 'tahole' block ('nahole jodi' expr 'tahole' block)* ('nahole' block)? 'ses'
    while_stmt  → 'jotokhon' expr 'tahole' block 'ses'
    func_decl   → 'kaj' IDENTIFIER '(' params? ')' block 'ses'
    return_stmt → 'ferao' expression?
    break_stmt  → 'thamo'
    expression  → or_expr
    or_expr     → and_expr ('othoba' and_expr)*
    and_expr    → equality ('ebong' equality)*
    equality    → comparison (('==' | '!=') comparison)*
    comparison  → addition (('<' | '>' | '<=' | '>=') addition)*
    addition    → multiply (('+' | '-') multiply)*
    multiply    → unary (('*' | '/' | '%') unary)*
    unary       → ('-' | 'na') unary | call
    call        → primary ('(' args? ')')* ('[' expr ']')*
    primary     → NUMBER | STRING | SOTTI | MITTHA | KHALI | IDENTIFIER
                | '(' expr ')' | '[' expr_list? ']' | 'nao' '(' expr? ')'
"""

from .tokens import TokenType
from .ast_nodes import (
    Program, NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    ListLiteral, Identifier, BinaryOp, UnaryOp, FuncCall, InputExpr,
    IndexExpr, VarDecl, Assignment, PrintStmt, IfStmt, WhileStmt,
    FuncDecl, ReturnStmt, BreakStmt,
)


class ParserError(Exception):
    """Error raised during parsing."""

    def __init__(self, message: str, token):
        self.token = token
        line_info = f"line {token.line}" if token else "unknown position"
        super().__init__(f"ভুল (Parser Error) {line_info}: {message}")


class Parser:
    """Recursive descent parser for bongScript."""

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    # ─── Token Navigation ──────────────────────────────────────────────────

    def _current(self):
        """Return the current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF

    def _advance(self):
        """Advance and return the current token."""
        token = self._current()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def _expect(self, token_type: TokenType):
        """Consume the current token if it matches, else raise error."""
        token = self._current()
        if token.type != token_type:
            raise ParserError(
                f"'{token_type.name}' asha hoyechilo, kintu '{token.value}' paowa gelo "
                f"(Expected {token_type.name}, got '{token.value}')",
                token,
            )
        return self._advance()

    def _match(self, *types: TokenType):
        """If current token matches any given type, consume and return it."""
        if self._current().type in types:
            return self._advance()
        return None

    def _check(self, token_type: TokenType) -> bool:
        """Check current token type without consuming."""
        return self._current().type == token_type

    def _skip_newlines(self):
        """Skip all consecutive newline tokens."""
        while self._current().type == TokenType.NEWLINE:
            self._advance()

    # ─── Top-Level ──────────────────────────────────────────────────────────

    def parse(self) -> Program:
        """Parse the entire program."""
        self._skip_newlines()
        statements = []

        while not self._check(TokenType.EOF):
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()

        return Program(statements)

    # ─── Statements ─────────────────────────────────────────────────────────

    def _parse_statement(self):
        """Parse a single statement."""
        token = self._current()

        if token.type == TokenType.DHORO:
            return self._parse_var_decl()
        elif token.type == TokenType.DEKHAO:
            return self._parse_print()
        elif token.type == TokenType.JODI:
            return self._parse_if()
        elif token.type == TokenType.JOTOKHON:
            return self._parse_while()
        elif token.type == TokenType.KAJ:
            return self._parse_func_decl()
        elif token.type == TokenType.FERAO:
            return self._parse_return()
        elif token.type == TokenType.THAMO:
            self._advance()
            self._skip_newlines()
            return BreakStmt()
        else:
            return self._parse_assignment_or_expr()

    def _parse_var_decl(self):
        """Parse: dhoro x = expression"""
        self._advance()  # consume 'dhoro'
        name_token = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.ASSIGN)
        value = self._parse_expression()
        self._skip_newlines()
        return VarDecl(name_token.value, value)

    def _parse_print(self):
        """Parse: dekhao("hello") or dekhao "hello" """
        self._advance()  # consume 'dekhao'

        # Support both: dekhao("x", "y") with parens, and dekhao "x" without
        if self._check(TokenType.LPAREN):
            self._advance()  # consume '('
            expressions = [self._parse_expression()]
            while self._match(TokenType.COMMA):
                expressions.append(self._parse_expression())
            self._expect(TokenType.RPAREN)
        else:
            # No parens — parse a single expression
            expressions = [self._parse_expression()]

        self._skip_newlines()
        return PrintStmt(expressions)

    def _parse_if(self):
        """
        Parse:
            jodi condition tahole
                ...
            nahole jodi condition tahole
                ...
            nahole
                ...
            ses
        """
        self._advance()  # consume 'jodi'
        condition = self._parse_expression()
        self._expect(TokenType.TAHOLE)
        self._skip_newlines()
        then_block = self._parse_block()

        elseif_blocks = []
        else_block = None

        while self._check(TokenType.NAHOLE):
            self._advance()  # consume 'nahole'

            if self._check(TokenType.JODI):
                # nahole jodi ... tahole (else if)
                self._advance()  # consume 'jodi'
                elif_condition = self._parse_expression()
                self._expect(TokenType.TAHOLE)
                self._skip_newlines()
                elif_block = self._parse_block()
                elseif_blocks.append((elif_condition, elif_block))
            else:
                # nahole (else)
                self._skip_newlines()
                else_block = self._parse_block()
                break

        self._expect(TokenType.SES)
        self._skip_newlines()
        return IfStmt(condition, then_block, elseif_blocks, else_block)

    def _parse_while(self):
        """Parse: jotokhon condition tahole ... ses"""
        self._advance()  # consume 'jotokhon'
        condition = self._parse_expression()
        self._expect(TokenType.TAHOLE)
        self._skip_newlines()
        body = self._parse_block()
        self._expect(TokenType.SES)
        self._skip_newlines()
        return WhileStmt(condition, body)

    def _parse_func_decl(self):
        """Parse: kaj name(param1, param2) ... ses"""
        self._advance()  # consume 'kaj'
        name_token = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.LPAREN)

        params = []
        if not self._check(TokenType.RPAREN):
            params.append(self._expect(TokenType.IDENTIFIER).value)
            while self._match(TokenType.COMMA):
                params.append(self._expect(TokenType.IDENTIFIER).value)

        self._expect(TokenType.RPAREN)
        self._skip_newlines()
        body = self._parse_block()
        self._expect(TokenType.SES)
        self._skip_newlines()
        return FuncDecl(name_token.value, params, body)

    def _parse_return(self):
        """Parse: ferao expression"""
        self._advance()  # consume 'ferao'
        value = None
        if self._current().type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.SES):
            value = self._parse_expression()
        self._skip_newlines()
        return ReturnStmt(value)

    def _parse_assignment_or_expr(self):
        """Parse an assignment (x = value) or expression statement."""
        expr = self._parse_expression()

        # Check if this is an assignment: identifier = value
        if isinstance(expr, Identifier) and self._check(TokenType.ASSIGN):
            self._advance()  # consume '='
            value = self._parse_expression()
            self._skip_newlines()
            return Assignment(expr.name, value)

        self._skip_newlines()
        return expr

    def _parse_block(self):
        """Parse a block of statements until 'ses' or 'nahole'."""
        statements = []
        block_enders = (TokenType.SES, TokenType.NAHOLE, TokenType.EOF)

        while self._current().type not in block_enders:
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()

        return statements

    # ─── Expressions (Precedence Climbing) ──────────────────────────────────

    def _parse_expression(self):
        return self._parse_or()

    def _parse_or(self):
        left = self._parse_and()
        while self._check(TokenType.OTHOBA):
            self._advance()
            right = self._parse_and()
            left = BinaryOp("othoba", left, right)
        return left

    def _parse_and(self):
        left = self._parse_equality()
        while self._check(TokenType.EBONG):
            self._advance()
            right = self._parse_equality()
            left = BinaryOp("ebong", left, right)
        return left

    def _parse_equality(self):
        left = self._parse_comparison()
        while self._current().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self._advance().value
            right = self._parse_comparison()
            left = BinaryOp(op, left, right)
        return left

    def _parse_comparison(self):
        left = self._parse_addition()
        while self._current().type in (TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQ, TokenType.GREATER_EQ):
            op = self._advance().value
            right = self._parse_addition()
            left = BinaryOp(op, left, right)
        return left

    def _parse_addition(self):
        left = self._parse_multiplication()
        while self._current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._parse_multiplication()
            left = BinaryOp(op, left, right)
        return left

    def _parse_multiplication(self):
        left = self._parse_unary()
        while self._current().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self._advance().value
            right = self._parse_unary()
            left = BinaryOp(op, left, right)
        return left

    def _parse_unary(self):
        if self._check(TokenType.MINUS):
            self._advance()
            operand = self._parse_unary()
            return UnaryOp("-", operand)
        if self._check(TokenType.NA):
            self._advance()
            operand = self._parse_unary()
            return UnaryOp("na", operand)
        return self._parse_call()

    def _parse_call(self):
        expr = self._parse_primary()

        while True:
            if self._check(TokenType.LPAREN):
                # Function call
                self._advance()
                args = []
                if not self._check(TokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expression())
                self._expect(TokenType.RPAREN)

                if isinstance(expr, Identifier):
                    expr = FuncCall(expr.name, args)
                else:
                    raise ParserError(
                        "Sudhu function ke call kora jay (Only functions can be called)",
                        self._current(),
                    )

            elif self._check(TokenType.LBRACKET):
                # Index access
                self._advance()
                index = self._parse_expression()
                self._expect(TokenType.RBRACKET)
                expr = IndexExpr(expr, index)
            else:
                break

        return expr

    def _parse_primary(self):
        token = self._current()

        if token.type == TokenType.NUMBER:
            self._advance()
            return NumberLiteral(token.value)

        if token.type == TokenType.STRING:
            self._advance()
            return StringLiteral(token.value)

        if token.type == TokenType.SOTTI:
            self._advance()
            return BooleanLiteral(True)

        if token.type == TokenType.MITTHA:
            self._advance()
            return BooleanLiteral(False)

        if token.type == TokenType.KHALI:
            self._advance()
            return NullLiteral()

        if token.type == TokenType.NAO:
            # nao("prompt") — input expression
            self._advance()
            self._expect(TokenType.LPAREN)
            prompt = None
            if not self._check(TokenType.RPAREN):
                prompt = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return InputExpr(prompt)

        if token.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(token.value)

        if token.type == TokenType.LPAREN:
            # Grouped expression
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return expr

        if token.type == TokenType.LBRACKET:
            # List literal: [1, 2, 3]
            self._advance()
            elements = []
            if not self._check(TokenType.RBRACKET):
                elements.append(self._parse_expression())
                while self._match(TokenType.COMMA):
                    elements.append(self._parse_expression())
            self._expect(TokenType.RBRACKET)
            return ListLiteral(elements)

        raise ParserError(
            f"Ei token ta asha hoyni ekhane: '{token.value}' (Unexpected token: '{token.value}')",
            token,
        )
