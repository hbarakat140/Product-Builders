"""CodebaseIndex — centralized AST-derived data for all analyzers.

Built once by the pre-pass before analyzers run. Provides query methods
for imports, exports, definitions, components, and naming patterns.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from product_builders.ast.models import (
    ComponentInfo,
    DefinitionInfo,
    ExportInfo,
    ImportInfo,
    NamingInfo,
)


class CodebaseIndex(BaseModel):
    """Centralized AST-derived codebase data."""

    imports: dict[str, list[ImportInfo]] = Field(default_factory=dict)
    exports: dict[str, list[ExportInfo]] = Field(default_factory=dict)
    definitions: dict[str, list[DefinitionInfo]] = Field(default_factory=dict)
    components: dict[str, list[ComponentInfo]] = Field(default_factory=dict)
    dependency_graph: dict[str, list[str]] = Field(default_factory=dict)
    naming_samples: list[NamingInfo] = Field(default_factory=list)
    file_count: int = 0
    parse_errors: int = 0

    # -- Query methods --

    def get_imports(self, file_path: str) -> list[ImportInfo]:
        """Return imports for a specific file."""
        return self.imports.get(file_path, [])

    def get_exports(self, file_path: str) -> list[ExportInfo]:
        """Return exports for a specific file."""
        return self.exports.get(file_path, [])

    def who_imports(self, module: str) -> list[str]:
        """Return file paths that import *module* (substring match on module name)."""
        results: list[str] = []
        for file_path, file_imports in self.imports.items():
            for imp in file_imports:
                if module in imp.module:
                    results.append(file_path)
                    break
        return results

    def get_definitions(
        self,
        file_path: str | None = None,
        kind: str | None = None,
    ) -> list[DefinitionInfo]:
        """Return definitions, optionally filtered by file and/or kind."""
        if file_path is not None:
            defs = self.definitions.get(file_path, [])
        else:
            defs = [d for file_defs in self.definitions.values() for d in file_defs]

        if kind is not None:
            defs = [d for d in defs if d.kind == kind]
        return defs

    def get_components(self, file_path: str | None = None) -> list[ComponentInfo]:
        """Return JSX component usages, optionally for a specific file."""
        if file_path is not None:
            return self.components.get(file_path, [])
        return [c for file_comps in self.components.values() for c in file_comps]

    def get_decorator_usage(
        self, decorator: str
    ) -> list[tuple[str, DefinitionInfo]]:
        """Find definitions decorated with *decorator* (substring match)."""
        results: list[tuple[str, DefinitionInfo]] = []
        for file_path, defs in self.definitions.items():
            for defn in defs:
                if any(decorator in d for d in defn.decorators):
                    results.append((file_path, defn))
        return results

    def get_naming_samples(self, kind: str | None = None) -> list[NamingInfo]:
        """Return naming samples, optionally filtered by kind."""
        if kind is not None:
            return [n for n in self.naming_samples if n.kind == kind]
        return list(self.naming_samples)
