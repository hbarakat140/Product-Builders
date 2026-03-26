"""Data models for AST-extracted information.

These Pydantic models represent the structural data extracted from source
files by tree-sitter parsers. They populate the CodebaseIndex.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ImportInfo(BaseModel):
    """A single import statement."""

    module: str
    names: list[str] = Field(default_factory=list)
    alias: str | None = None
    is_default: bool = False
    is_star: bool = False
    line: int = 0


class ExportInfo(BaseModel):
    """A single exported symbol."""

    name: str
    kind: str = ""  # function, class, variable, type, default
    line: int = 0


class DefinitionInfo(BaseModel):
    """A function, class, or interface definition."""

    name: str
    kind: str = ""  # function, class, interface, type_alias, method
    line: int = 0
    end_line: int | None = None
    decorators: list[str] = Field(default_factory=list)
    is_async: bool = False
    parameters: list[str] = Field(default_factory=list)


class ComponentInfo(BaseModel):
    """A JSX/TSX component usage."""

    name: str
    line: int = 0
    props: list[str] = Field(default_factory=list)


class NamingInfo(BaseModel):
    """A named symbol for convention detection."""

    name: str
    kind: str = ""  # variable, function, class, parameter
    file_path: str = ""
