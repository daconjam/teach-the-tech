import ast
from typing import Dict, Any


class ParadigmVisitor(ast.NodeVisitor):
    """
    Optimized event-driven AST Visitor. Instead of walking the whole tree flat,
    the compiler engine alerts this class only when it hits specific nodes.
    """
    def __init__(self) -> None:
        self.metrics: Dict[str, int] = {
            "total_nodes": 0,
            "function_definitions": 0,
            "class_definitions": 0,
            "lambda_expressions": 0,
            "global_statements": 0,
            "pure_functional_indicators": 0,  # e.g., ListComps, GeneratorExps
        }

    def generic_visit(self, node: ast.AST) -> None:
        self.metrics["total_nodes"] += 1
        super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.metrics["function_definitions"] += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.metrics["class_definitions"] += 1
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.metrics["lambda_expressions"] += 1
        self.generic_visit(node)

    def visit_Global(self, node: ast.Global) -> None:
        self.metrics["global_statements"] += 1
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self.metrics["pure_functional_indicators"] += 1
        self.generic_visit(node)


class ASTCodeAnalyzer:
    """
    Hardened AST Analyzer using deterministic structural ratios
    to classify multi-paradigm source implementations.
    """
    def __init__(self, source_code: str) -> None:
        self.source_code: str = source_code
        self.error_diagnostics: str | None = None
        self._metrics: Dict[str, int] = {}

        try:
            self.tree: ast.Module = ast.parse(source_code)
            self._run_analysis()
        except SyntaxError as e:
            self.tree = None
            self.error_diagnostics = f"Line {e.lineno}, Col {e.offset}: {e.msg}"

    def _run_analysis(self) -> None:
        """Executes the specialized visitor pattern across the tree."""
        if self.tree:
            visitor = ParadigmVisitor()
            visitor.visit(self.tree)
            self._metrics = visitor.metrics  # now includes total_nodes

    def analyze_structure(self) -> Dict[str, Any]:
        if self.error_diagnostics:
            return {"success": False, "error": self.error_diagnostics}

        # Flatten so test_analyzer sees top-level metrics
        return {
            "success": True,
            "total_nodes": self._metrics["total_nodes"],
            "function_definitions": self._metrics["function_definitions"],
            "class_definitions": self._metrics["class_definitions"],
            "lambda_expressions": self._metrics["lambda_expressions"],
            "global_statements": self._metrics["global_statements"],
            "pure_functional_indicators": self._metrics["pure_functional_indicators"],
        }

    def deduce_dominant_paradigm(self) -> str:
        if self.error_diagnostics or not self._metrics:
            return "Undetermined (Syntax/Parsing Failure)"

        m = self._metrics
        total_signals = sum(m.values())

        if total_signals == 0:
            return "Procedural Programming (Linear/Flat Script)"

        # Enterprise Hardening: Compute structural density ratios rather than simple existence checks
        oop_ratio = m["class_definitions"] / total_signals
        fp_ratio = (m["lambda_expressions"] + m["pure_functional_indicators"]) / total_signals

        if oop_ratio > 0.25:
            return "Object-Oriented Programming (OOP)"
        elif fp_ratio > 0.30 and m["global_statements"] == 0:
            return "Functional Programming (FP)"
        else:
            return "Procedural Programming"
