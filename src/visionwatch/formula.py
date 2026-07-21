"""Restricted expression evaluator for customer alert rules."""

from __future__ import annotations

import ast


class SafeFormula:
    """Evaluate arithmetic and comparisons using only the OCR value ``x``."""

    _allowed = {
        ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare,
        ast.Name, ast.Load, ast.Constant, ast.And, ast.Or, ast.Add, ast.Sub,
        ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.USub,
        ast.UAdd, ast.Not, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt,
        ast.GtE,
    }

    @classmethod
    def evaluate(cls, expression: str, x: float) -> bool:
        tree = ast.parse(expression.strip(), mode="eval")

        # Reject the expression before compilation if even one node is outside
        # the small language understood by the alert rule editor.
        for node in ast.walk(tree):
            if type(node) not in cls._allowed:
                raise ValueError(f"Unsupported formula element: {type(node).__name__}")
            if isinstance(node, ast.Name) and node.id != "x":
                raise ValueError("Only the recognized value 'x' may be used")
            if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float, bool)):
                raise ValueError("Only numeric constants are allowed")
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if abs(node.value) > 1_000_000_000_000:
                    raise ValueError("Numeric constant exceeds the safety limit")
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
                exponent = node.right
                if not isinstance(exponent, ast.Constant) or not isinstance(exponent.value, (int, float)):
                    raise ValueError("Exponent must be a numeric constant")
                if abs(exponent.value) > 8:
                    raise ValueError("Exponent must be between -8 and 8")

        compiled = compile(tree, "<alert-rule>", "eval")
        return bool(eval(compiled, {"__builtins__": {}}, {"x": x}))
