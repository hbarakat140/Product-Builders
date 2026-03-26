"""CodebaseIndex builder — orchestrates tree-sitter parsing across the repo.

Walks the repository, parses source files with tree-sitter, and collects
all extracted data into a single CodebaseIndex.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path

from product_builders.analyzers.base import SKIP_DIRS
from product_builders.ast.index import CodebaseIndex
from product_builders.ast.models import (
    ComponentInfo,
    DefinitionInfo,
    ExportInfo,
    ImportInfo,
    NamingInfo,
)
from product_builders.ast.parsers import get_extractor, get_parser, get_supported_extensions

logger = logging.getLogger(__name__)

MAX_FILE_BYTES = 1_000_000  # 1 MB — same limit as BaseAnalyzer.read_file
MAX_NAMING_SAMPLES = 500
DEFAULT_MAX_FILES = 500


def build_codebase_index(
    repo_path: Path,
    languages: dict[str, float],
    *,
    max_files: int = DEFAULT_MAX_FILES,
) -> CodebaseIndex | None:
    """Build a CodebaseIndex by parsing source files with tree-sitter.

    Returns None if tree-sitter is not available or no files could be parsed.
    """
    try:
        from product_builders.ast import TREE_SITTER_AVAILABLE
    except ImportError:
        return None

    if not TREE_SITTER_AVAILABLE:
        return None

    supported_exts = get_supported_extensions(languages)
    if not supported_exts:
        logger.debug("No supported languages detected for AST indexing")
        return None

    all_imports: dict[str, list[ImportInfo]] = {}
    all_exports: dict[str, list[ExportInfo]] = {}
    all_definitions: dict[str, list[DefinitionInfo]] = {}
    all_components: dict[str, list[ComponentInfo]] = {}
    all_naming: list[NamingInfo] = []
    file_count = 0
    parse_errors = 0

    # Cache parsers and extractors by extension to avoid recreating per file
    parser_cache: dict[str, object] = {}
    extractor_cache: dict[str, object] = {}

    for source_file in _iter_source_files(repo_path, supported_exts, max_files):
        rel_path = source_file.relative_to(repo_path).as_posix()
        ext = source_file.suffix.lower()

        # Read file
        try:
            stat = source_file.stat()
            if stat.st_size > MAX_FILE_BYTES:
                continue
            source_bytes = source_file.read_bytes()
        except Exception:
            continue

        # Get parser and extractor (cached per extension)
        if ext not in parser_cache:
            parser_cache[ext] = get_parser(ext)
            extractor_cache[ext] = get_extractor(ext)
        parser = parser_cache[ext]
        extractor = extractor_cache[ext]
        if parser is None or extractor is None:
            continue

        # Parse
        try:
            tree = parser.parse(source_bytes)
            root = tree.root_node
        except Exception as exc:
            logger.debug("Parse error for %s: %s", rel_path, exc)
            parse_errors += 1
            continue

        file_count += 1

        # Extract
        try:
            file_imports = extractor.extract_imports(root, source_bytes)
            if file_imports:
                all_imports[rel_path] = file_imports

            file_exports = extractor.extract_exports(root, source_bytes)
            if file_exports:
                all_exports[rel_path] = file_exports

            file_defs = extractor.extract_definitions(root, source_bytes)
            if file_defs:
                all_definitions[rel_path] = file_defs

            file_components = extractor.extract_components(root, source_bytes)
            if file_components:
                all_components[rel_path] = file_components

            if len(all_naming) < MAX_NAMING_SAMPLES:
                samples = extractor.extract_naming_samples(root, source_bytes)
                for s in samples:
                    s.file_path = rel_path
                remaining = MAX_NAMING_SAMPLES - len(all_naming)
                all_naming.extend(samples[:remaining])
        except Exception as exc:
            logger.debug("Extraction error for %s: %s", rel_path, exc)
            parse_errors += 1

    if file_count == 0:
        return None

    # Build dependency graph from imports
    dep_graph = _build_dependency_graph(all_imports)

    return CodebaseIndex(
        imports=all_imports,
        exports=all_exports,
        definitions=all_definitions,
        components=all_components,
        dependency_graph=dep_graph,
        naming_samples=all_naming,
        file_count=file_count,
        parse_errors=parse_errors,
    )


def _iter_source_files(
    repo_path: Path,
    extensions: set[str],
    max_files: int,
) -> Iterator[Path]:
    """Yield source files matching supported extensions, up to *max_files*."""
    count = 0
    for item in _walk_repo(repo_path):
        if count >= max_files:
            return
        if item.suffix.lower() in extensions:
            yield item
            count += 1


def _walk_repo(repo_path: Path) -> Iterator[Path]:
    """Walk the repository lazily, skipping common non-source directories."""

    def _walk(directory: Path, depth: int = 0) -> Iterator[Path]:
        if depth > 10:
            return
        try:
            entries = sorted(directory.iterdir())
        except PermissionError:
            return
        for entry in entries:
            if entry.is_dir():
                if entry.name in SKIP_DIRS or entry.name.startswith("."):
                    continue
                yield from _walk(entry, depth + 1)
            elif entry.is_file():
                yield entry

    yield from _walk(repo_path)


def _build_dependency_graph(
    all_imports: dict[str, list[ImportInfo]],
) -> dict[str, list[str]]:
    """Build a module dependency graph from collected imports.

    Maps each file to the list of modules it imports. Uses the raw module
    names from import statements — no path resolution attempted.
    """
    graph: dict[str, list[str]] = {}
    for file_path, imports in all_imports.items():
        modules = list({imp.module for imp in imports if imp.module})
        if modules:
            graph[file_path] = sorted(modules)
    return graph
