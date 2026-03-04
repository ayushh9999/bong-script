"""
Tree-walking Interpreter for bongScript.
Executes the AST produced by the parser.
"""

from .ast_nodes import (
    Program, NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    ListLiteral, Identifier, BinaryOp, UnaryOp, FuncCall, InputExpr,
    IndexExpr, VarDecl, Assignment, PrintStmt, IfStmt, WhileStmt,
    FuncDecl, ReturnStmt, BreakStmt,
)


# ─── Control Flow Exceptions ───────────────────────────────────────────────────

class ReturnSignal(Exception):
    """Raised when a 'ferao' (return) statement is executed."""
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    """Raised when a 'thamo' (break) statement is executed."""
    pass


class BongRuntimeError(Exception):
    """Runtime error in bongScript execution."""
    def __init__(self, message: str):
        super().__init__(f"ভুল (Runtime Error): {message}")


# ─── Environment (Scope) ───────────────────────────────────────────────────────

class Environment:
    """Variable scope with optional parent for lexical scoping."""

    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def get(self, name: str):
        """Look up a variable, searching parent scopes."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise BongRuntimeError(
            f"'{name}' variable ti define kora hoyni (Variable '{name}' is not defined)"
        )

    def set(self, name: str, value):
        """Set a variable in the current scope."""
        self.variables[name] = value

    def assign(self, name: str, value):
        """Update an existing variable, searching parent scopes."""
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise BongRuntimeError(
            f"'{name}' variable ti age define kora hoyni (Variable '{name}' is not defined)"
        )


# ─── Function Object ───────────────────────────────────────────────────────────

class BongFunction:
    """Represents a user-defined function with closure."""

    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self):
        return f"<kaj {self.name}>"


# ─── Interpreter ────────────────────────────────────────────────────────────────

class Interpreter:
    """Tree-walking interpreter for bongScript."""

    def __init__(self):
        self.global_env = Environment()
        self._setup_builtins()

    def _setup_builtins(self):
        """Register built-in functions."""
        self.builtins = {
            # Length
            "len":      self._builtin_len,
            "dorjho":   self._builtin_len,          # দৈর্ঘ্য
            # Type conversion
            "sonkhya":  self._builtin_to_number,     # সংখ্যা → to number
            "likhon":   self._builtin_to_string,     # লিখন → to string
            # Type checking
            "dhoron":   self._builtin_type,          # ধরন → type
            "type":     self._builtin_type,
            # Math
            "purno":    self._builtin_int,            # পূর্ণ → int/floor
            "golakrito": self._builtin_round,         # গোলাকৃত → round
        }

    # ─── Built-in Functions ─────────────────────────────────────────────

    def _builtin_len(self, args):
        self._check_arg_count("dorjho/len", args, 1)
        val = args[0]
        if isinstance(val, (str, list)):
            return len(val)
        raise BongRuntimeError("dorjho() sudhu string ba list e kaj kore (only works on strings/lists)")

    def _builtin_to_number(self, args):
        self._check_arg_count("sonkhya", args, 1)
        val = args[0]
        if isinstance(val, bool):
            return 1 if val else 0
        if isinstance(val, (int, float)):
            return val
        try:
            return float(val) if "." in str(val) else int(val)
        except (ValueError, TypeError):
            raise BongRuntimeError(f"'{val}' ke number e convert kora jacchhe na (Cannot convert to number)")

    def _builtin_to_string(self, args):
        self._check_arg_count("likhon", args, 1)
        return self._stringify(args[0])

    def _builtin_type(self, args):
        self._check_arg_count("dhoron", args, 1)
        val = args[0]
        if val is None:
            return "khali"
        if isinstance(val, bool):
            return "boolean"
        if isinstance(val, int):
            return "purno sonkhya"    # integer
        if isinstance(val, float):
            return "doshomik sonkhya"  # decimal
        if isinstance(val, str):
            return "likhon"            # string
        if isinstance(val, list):
            return "taalika"           # list
        if isinstance(val, BongFunction):
            return "kaj"               # function
        return "ojana"                 # unknown

    def _builtin_int(self, args):
        self._check_arg_count("purno", args, 1)
        val = args[0]
        if isinstance(val, (int, float)):
            return int(val)
        raise BongRuntimeError("purno() sudhu number e kaj kore (only works on numbers)")

    def _builtin_round(self, args):
        if len(args) < 1 or len(args) > 2:
            raise BongRuntimeError("golakrito() 1 ba 2 ta argument ney (takes 1-2 arguments)")
        val = args[0]
        if not isinstance(val, (int, float)):
            raise BongRuntimeError("golakrito() sudhu number e kaj kore")
        digits = int(args[1]) if len(args) == 2 else 0
        return round(val, digits)

    def _check_arg_count(self, name, args, expected):
        if len(args) != expected:
            raise BongRuntimeError(
                f"{name}() {expected} ta argument dorkar, {len(args)} ta deowa hoyeche "
                f"(Expected {expected} args, got {len(args)})"
            )

    # ─── Main Entry Point ──────────────────────────────────────────────

    def interpret(self, program: Program):
        """Execute a parsed program."""
        try:
            for stmt in program.statements:
                self._execute(stmt, self.global_env)
        except ReturnSignal:
            raise BongRuntimeError(
                "'ferao' kaj er baire use kora jayna (Cannot use 'ferao/return' outside a function)"
            )
        except BreakSignal:
            raise BongRuntimeError(
                "'thamo' loop er baire use kora jayna (Cannot use 'thamo/break' outside a loop)"
            )

    # ─── Statement Execution ───────────────────────────────────────────

    def _execute(self, node, env: Environment):
        """Execute a single AST node."""

        if isinstance(node, VarDecl):
            value = self._evaluate(node.value, env)
            env.set(node.name, value)

        elif isinstance(node, Assignment):
            value = self._evaluate(node.value, env)
            env.assign(node.name, value)

        elif isinstance(node, PrintStmt):
            values = [self._stringify(self._evaluate(expr, env)) for expr in node.expressions]
            print(" ".join(values))

        elif isinstance(node, IfStmt):
            self._exec_if(node, env)

        elif isinstance(node, WhileStmt):
            self._exec_while(node, env)

        elif isinstance(node, FuncDecl):
            func = BongFunction(node.name, node.params, node.body, env)
            env.set(node.name, func)

        elif isinstance(node, ReturnStmt):
            value = None
            if node.value is not None:
                value = self._evaluate(node.value, env)
            raise ReturnSignal(value)

        elif isinstance(node, BreakStmt):
            raise BreakSignal()

        else:
            # Expression statement (e.g., function call as statement)
            self._evaluate(node, env)

    def _exec_if(self, node: IfStmt, env: Environment):
        """Execute an if/else if/else chain."""
        if self._is_truthy(self._evaluate(node.condition, env)):
            for stmt in node.then_block:
                self._execute(stmt, env)
            return

        for condition, block in node.elseif_blocks:
            if self._is_truthy(self._evaluate(condition, env)):
                for stmt in block:
                    self._execute(stmt, env)
                return

        if node.else_block:
            for stmt in node.else_block:
                self._execute(stmt, env)

    def _exec_while(self, node: WhileStmt, env: Environment):
        """Execute a while loop."""
        while self._is_truthy(self._evaluate(node.condition, env)):
            try:
                for stmt in node.body:
                    self._execute(stmt, env)
            except BreakSignal:
                break

    # ─── Expression Evaluation ─────────────────────────────────────────

    def _evaluate(self, node, env: Environment):
        """Evaluate an expression node and return its value."""

        if isinstance(node, NumberLiteral):
            return node.value

        if isinstance(node, StringLiteral):
            return node.value

        if isinstance(node, BooleanLiteral):
            return node.value

        if isinstance(node, NullLiteral):
            return None

        if isinstance(node, Identifier):
            return env.get(node.name)

        if isinstance(node, BinaryOp):
            return self._eval_binary(node, env)

        if isinstance(node, UnaryOp):
            return self._eval_unary(node, env)

        if isinstance(node, FuncCall):
            return self._eval_call(node, env)

        if isinstance(node, InputExpr):
            prompt = ""
            if node.prompt is not None:
                prompt = self._stringify(self._evaluate(node.prompt, env))
            return input(prompt)

        if isinstance(node, ListLiteral):
            return [self._evaluate(el, env) for el in node.elements]

        if isinstance(node, IndexExpr):
            return self._eval_index(node, env)

        raise BongRuntimeError(f"Ei node ta execute kora jacchhe na: {type(node).__name__}")

    def _eval_binary(self, node: BinaryOp, env: Environment):
        """Evaluate a binary operation."""
        left = self._evaluate(node.left, env)

        # Short-circuit logical operators
        if node.op == "ebong":
            return self._evaluate(node.right, env) if self._is_truthy(left) else left
        if node.op == "othoba":
            return left if self._is_truthy(left) else self._evaluate(node.right, env)

        right = self._evaluate(node.right, env)

        # Arithmetic
        if node.op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return self._stringify(left) + self._stringify(right)
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            self._expect_numbers(left, right, "+")
            return left + right

        if node.op == "-":
            self._expect_numbers(left, right, "-")
            return left - right

        if node.op == "*":
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, int) and isinstance(right, str):
                return right * left
            self._expect_numbers(left, right, "*")
            return left * right

        if node.op == "/":
            self._expect_numbers(left, right, "/")
            if right == 0:
                raise BongRuntimeError("Shunno diye bhag kora jay na! (Division by zero)")
            return left / right

        if node.op == "%":
            self._expect_numbers(left, right, "%")
            if right == 0:
                raise BongRuntimeError("Shunno diye bhag kora jay na! (Division by zero)")
            return left % right

        # Comparison
        if node.op == "==":
            return left == right
        if node.op == "!=":
            return left != right
        if node.op in ("<", ">", "<=", ">="):
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise BongRuntimeError(
                    f"'{node.op}' sudhu number compare korte pare ('{node.op}' only compares numbers)"
                )
            ops = {"<": lambda a, b: a < b, ">": lambda a, b: a > b,
                   "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b}
            return ops[node.op](left, right)

        raise BongRuntimeError(f"Ei operator ta chena jacchhe na: '{node.op}'")

    def _eval_unary(self, node: UnaryOp, env: Environment):
        """Evaluate a unary operation."""
        operand = self._evaluate(node.operand, env)
        if node.op == "-":
            if not isinstance(operand, (int, float)):
                raise BongRuntimeError("Minus sudhu number e hoy (Unary minus only works on numbers)")
            return -operand
        if node.op == "na":
            return not self._is_truthy(operand)
        raise BongRuntimeError(f"Ei unary operator ta chena jacchhe na: '{node.op}'")

    def _eval_call(self, node: FuncCall, env: Environment):
        """Evaluate a function call."""
        # Check built-ins first
        if node.name in self.builtins:
            args = [self._evaluate(arg, env) for arg in node.args]
            return self.builtins[node.name](args)

        func = env.get(node.name)

        if not isinstance(func, BongFunction):
            raise BongRuntimeError(
                f"'{node.name}' ekta kaj (function) na ('{node.name}' is not a function)"
            )

        args = [self._evaluate(arg, env) for arg in node.args]

        if len(args) != len(func.params):
            raise BongRuntimeError(
                f"'{func.name}' kaj e {len(func.params)} ta argument dorkar, "
                f"kintu {len(args)} ta deowa hoyeche "
                f"(Expected {len(func.params)} arguments, got {len(args)})"
            )

        # Create a new scope for the function, with closure as parent
        func_env = Environment(func.closure)
        for param, arg in zip(func.params, args):
            func_env.set(param, arg)

        try:
            for stmt in func.body:
                self._execute(stmt, func_env)
        except ReturnSignal as r:
            return r.value

        return None

    def _eval_index(self, node: IndexExpr, env: Environment):
        """Evaluate an index access."""
        obj = self._evaluate(node.obj, env)
        index = self._evaluate(node.index, env)

        if isinstance(obj, (list, str)):
            if not isinstance(index, int):
                raise BongRuntimeError("Index ta integer howa dorkar (Index must be an integer)")
            if index < 0 or index >= len(obj):
                raise BongRuntimeError(
                    f"Index {index} simar baire (Index out of range, size: {len(obj)})"
                )
            return obj[index]

        raise BongRuntimeError(
            "Indexing sudhu list ba string e hoy (Indexing only works on lists and strings)"
        )

    # ─── Helpers ────────────────────────────────────────────────────────

    def _is_truthy(self, value) -> bool:
        """Determine truthiness of a value."""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
            return len(value) > 0
        return True

    def _stringify(self, value) -> str:
        """Convert a value to its string representation."""
        if value is None:
            return "khali"
        if isinstance(value, bool):
            return "sotti" if value else "mittha"
        if isinstance(value, float):
            # Display clean integers: 5.0 → "5"
            if value == int(value):
                return str(int(value))
            return str(value)
        if isinstance(value, list):
            items = ", ".join(self._stringify(item) for item in value)
            return f"[{items}]"
        if isinstance(value, BongFunction):
            return f"<kaj {value.name}>"
        return str(value)

    def _expect_numbers(self, left, right, op: str):
        """Validate both operands are numbers."""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise BongRuntimeError(
                f"'{op}' sudhu number er sathe kaj kore ('{op}' only works with numbers)"
            )
