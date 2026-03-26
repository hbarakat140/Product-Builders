"""Tree-sitter parser factory — loads language grammars on demand.

Provides ``get_parser()`` to obtain a configured Parser for a given
language and ``get_extractor()`` to obtain the matching AST extractor.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tree_sitter import Parser

    from product_builders.ast.extractors.base import BaseExtractor

logger = logging.getLogger(__name__)

# Map from file extension to (grammar loader, extractor class path)
_EXT_TO_LANG: dict[str, str] = {
    ".ts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "tsx",  # JSX uses TSX grammar
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".py": "python",
}

# Map from TechStackResult.languages keys to file extensions
LANGUAGE_EXTENSIONS: dict[str, list[str]] = {
    "TypeScript": [".ts", ".tsx"],
    "JavaScript": [".js", ".jsx", ".mjs", ".cjs"],
    "Python": [".py"],
}


def get_supported_extensions(languages: dict[str, float]) -> set[str]:
    """Return file extensions we can parse based on detected languages."""
    extensions: set[str] = set()
    for lang in languages:
        exts = LANGUAGE_EXTENSIONS.get(lang, [])
        extensions.update(exts)
    return extensions


def get_parser(extension: str) -> Parser | None:
    """Return a configured tree-sitter Parser for the given file extension.

    Returns None if the language is not supported or tree-sitter is unavailable.
    """
    lang_name = _EXT_TO_LANG.get(extension)
    if lang_name is None:
        return None

    try:
        from tree_sitter import Language, Parser

        language = _load_language(lang_name)
        if language is None:
            return None
        return Parser(language)
    except Exception as exc:
        logger.debug("Failed to create parser for %s: %s", extension, exc)
        return None


def get_extractor(extension: str) -> BaseExtractor | None:
    """Return the appropriate extractor for a file extension."""
    lang_name = _EXT_TO_LANG.get(extension)
    if lang_name is None:
        return None

    if lang_name in ("typescript", "tsx", "javascript"):
        from product_builders.ast.extractors.typescript import TypeScriptExtractor
        return TypeScriptExtractor()
    elif lang_name == "python":
        from product_builders.ast.extractors.python_extractor import PythonExtractor
        return PythonExtractor()

    return None


def _load_language(lang_name: str) -> Language | None:
    """Load a tree-sitter Language grammar."""
    from tree_sitter import Language

    try:
        if lang_name == "typescript":
            import tree_sitter_typescript
            return Language(tree_sitter_typescript.language_typescript())
        elif lang_name == "tsx":
            import tree_sitter_typescript
            return Language(tree_sitter_typescript.language_tsx())
        elif lang_name == "javascript":
            import tree_sitter_javascript
            return Language(tree_sitter_javascript.language())
        elif lang_name == "python":
            import tree_sitter_python
            return Language(tree_sitter_python.language())
    except ImportError:
        logger.debug("Grammar package for %s not installed", lang_name)
    except Exception as exc:
        logger.warning("Failed to load grammar for %s: %s", lang_name, exc)

    return None
