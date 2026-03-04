"""
AST (Abstract Syntax Tree) node definitions for bongScript.
Each node represents a syntactic construct in the language.
"""


class ASTNode:
    """Base class for all AST nodes."""
    pass


# ─── Literals ───────────────────────────────────────────────────────────────────

class NumberLiteral(ASTNode):
    """Numeric literal: 42, 3.14"""
    def __init__(self, value):
        self.value = value


class StringLiteral(ASTNode):
    """String literal: "nomoskar" """
    def __init__(self, value):
        self.value = value


class BooleanLiteral(ASTNode):
    """Boolean literal: sotti / mittha"""
    def __init__(self, value):
        self.value = value


class NullLiteral(ASTNode):
    """Null literal: khali"""
    pass


class ListLiteral(ASTNode):
    """List literal: [1, 2, 3]"""
    def __init__(self, elements):
        self.elements = elements


# ─── Expressions ────────────────────────────────────────────────────────────────

class Identifier(ASTNode):
    """Variable reference: x, naam"""
    def __init__(self, name):
        self.name = name


class BinaryOp(ASTNode):
    """Binary operation: a + b, x == y, a ebong b"""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryOp(ASTNode):
    """Unary operation: -x, na sotti"""
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class FuncCall(ASTNode):
    """Function call: jog(a, b)"""
    def __init__(self, name, args):
        self.name = name
        self.args = args


class InputExpr(ASTNode):
    """Input expression: nao("prompt")"""
    def __init__(self, prompt):
        self.prompt = prompt


class IndexExpr(ASTNode):
    """Index access: taalika[0]"""
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index


# ─── Statements ─────────────────────────────────────────────────────────────────

class VarDecl(ASTNode):
    """Variable declaration: dhoro x = 10"""
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Assignment(ASTNode):
    """Variable assignment without dhoro: x = 10"""
    def __init__(self, name, value):
        self.name = name
        self.value = value


class PrintStmt(ASTNode):
    """Print statement: dekhao("hello"), dekhao "hello" """
    def __init__(self, expressions):
        self.expressions = expressions


class IfStmt(ASTNode):
    """
    If statement:
        jodi condition tahole
            ...
        nahole jodi condition tahole
            ...
        nahole
            ...
        ses
    """
    def __init__(self, condition, then_block, elseif_blocks, else_block):
        self.condition = condition
        self.then_block = then_block
        self.elseif_blocks = elseif_blocks  # list of (condition, block)
        self.else_block = else_block


class WhileStmt(ASTNode):
    """
    While loop:
        jotokhon condition tahole
            ...
        ses
    """
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class FuncDecl(ASTNode):
    """
    Function declaration:
        kaj naam(params)
            ...
        ses
    """
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class ReturnStmt(ASTNode):
    """Return statement: ferao value"""
    def __init__(self, value):
        self.value = value


class BreakStmt(ASTNode):
    """Break statement: thamo"""
    pass


class Program(ASTNode):
    """Top-level program node containing all statements."""
    def __init__(self, statements):
        self.statements = statements
