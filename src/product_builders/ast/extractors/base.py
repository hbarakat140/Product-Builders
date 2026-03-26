"""Base extractor interface for language-specific AST extraction."""

from __future__ import annotations

from abc import ABC, abstractmethod

from tree_sitter import Node

from product_builders.ast.models import (
    ComponentInfo,
    DefinitionInfo,
    ExportInfo,
    ImportInfo,
    NamingInfo,
)


class BaseExtractor(ABC):
    """Abstract base for language-specific AST extractors."""

    @abstractmethod
    def extract_imports(self, root: Node, source: bytes) -> list[ImportInfo]:
        """Extract import statements from the AST."""

    @abstractmethod
    def extract_exports(self, root: Node, source: bytes) -> list[ExportInfo]:
        """Extract exported symbols from the AST."""

    @abstractmethod
    def extract_definitions(self, root: Node, source: bytes) -> list[DefinitionInfo]:
        """Extract function, class, and interface definitions."""

    def extract_components(self, root: Node, source: bytes) -> list[ComponentInfo]:
        """Extract JSX/TSX component usages. Override in JSX-capable languages."""
        return []

    @abstractmethod
    def extract_naming_samples(self, root: Node, source: bytes) -> list[NamingInfo]:
        """Extract named symbols for convention detection."""

    # -- Helpers --

    @staticmethod
    def _node_text(node: Node, source: bytes) -> str:
        """Get the text content of a node."""
        return source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")

    @staticmethod
    def _find_children(node: Node, type_name: str) -> list[Node]:
        """Find all direct children of a specific type."""
        return [c for c in node.children if c.type == type_name]

    @staticmethod
    def _find_child(node: Node, type_name: str) -> Node | None:
        """Find the first direct child of a specific type."""
        for c in node.children:
            if c.type == type_name:
                return c
        return None

    @staticmethod
    def _walk_descendants(node: Node, type_name: str) -> list[Node]:
        """Find all descendants of a specific type (recursive)."""
        results: list[Node] = []
        stack = list(node.children)
        while stack:
            child = stack.pop()
            if child.type == type_name:
                results.append(child)
            stack.extend(child.children)
        return results

    @staticmethod
    def _strip_quotes(s: str) -> str:
        """Remove surrounding quotes from a string literal."""
        if len(s) >= 2 and s[0] in ("'", '"', "`") and s[-1] == s[0]:
            return s[1:-1]
        return s

    @staticmethod
    def _clean_decorator_text(text: str) -> str:
        """Normalize decorator text: strip ``@`` prefix and call arguments."""
        text = text.lstrip("@").strip()
        paren = text.find("(")
        if paren != -1:
            text = text[:paren]
        return text
