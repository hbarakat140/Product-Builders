"""TypeScript / JavaScript / TSX / JSX extractor.

Uses tree-sitter AST nodes to extract imports, exports, definitions,
JSX component usages, and naming samples from TS/JS source files.
"""

from __future__ import annotations

import logging

from tree_sitter import Node

from product_builders.ast.extractors.base import BaseExtractor
from product_builders.ast.models import (
    ComponentInfo,
    DefinitionInfo,
    ExportInfo,
    ImportInfo,
    NamingInfo,
)

logger = logging.getLogger(__name__)

_MAX_NAMING_SAMPLES = 100


class TypeScriptExtractor(BaseExtractor):
    """Extract structural information from TypeScript/JavaScript ASTs."""

    # ------------------------------------------------------------------
    # Imports
    # ------------------------------------------------------------------

    def extract_imports(self, root: Node, source: bytes) -> list[ImportInfo]:
        results: list[ImportInfo] = []

        # --- import statements ---
        for stmt in self._walk_descendants(root, "import_statement"):
            results.extend(self._parse_import_statement(stmt, source))

        # --- require() calls ---
        for decl in self._walk_descendants(root, "variable_declarator"):
            info = self._parse_require(decl, source)
            if info is not None:
                results.append(info)

        return results

    def _parse_import_statement(
        self, stmt: Node, source: bytes
    ) -> list[ImportInfo]:
        """Parse a single ``import_statement`` node into ImportInfo(s)."""
        module = self._extract_module_string(stmt, source)
        if module is None:
            return []

        line = stmt.start_point[0] + 1

        # Side-effect import: import "module"
        import_clause = self._find_child(stmt, "import_clause")
        if import_clause is None:
            return [ImportInfo(module=module, line=line)]

        results: list[ImportInfo] = []

        # Namespace import: import * as name from "module"
        ns_import = self._find_child(import_clause, "namespace_import")
        if ns_import is not None:
            alias_node = self._find_child(ns_import, "identifier")
            alias = self._node_text(alias_node, source) if alias_node else None
            results.append(
                ImportInfo(module=module, is_star=True, alias=alias, line=line)
            )

        # Default import: import Foo from "module"
        default_id = self._find_child(import_clause, "identifier")
        if default_id is not None:
            results.append(
                ImportInfo(
                    module=module,
                    names=[self._node_text(default_id, source)],
                    is_default=True,
                    line=line,
                )
            )

        # Named imports: import { a, b as c } from "module"
        named_imports = self._find_child(import_clause, "named_imports")
        if named_imports is not None:
            names: list[str] = []
            for spec in self._find_children(named_imports, "import_specifier"):
                name_node = self._find_child(spec, "identifier")
                if name_node is not None:
                    names.append(self._node_text(name_node, source))
            if names:
                results.append(ImportInfo(module=module, names=names, line=line))

        # If clause was present but none of the above matched, still record
        if not results:
            results.append(ImportInfo(module=module, line=line))

        return results

    def _parse_require(
        self, decl: Node, source: bytes
    ) -> ImportInfo | None:
        """Parse ``const x = require("module")`` patterns."""
        name_node = self._find_child(decl, "identifier")
        value_node = self._find_child(decl, "call_expression")
        if name_node is None or value_node is None:
            return None

        func = self._find_child(value_node, "identifier")
        if func is None or self._node_text(func, source) != "require":
            return None

        args = self._find_child(value_node, "arguments")
        if args is None:
            return None

        str_node = self._find_child(args, "string")
        if str_node is None:
            return None

        module = self._strip_quotes(self._node_text(str_node, source))
        name = self._node_text(name_node, source)
        return ImportInfo(
            module=module,
            names=[name],
            line=decl.start_point[0] + 1,
        )

    # ------------------------------------------------------------------
    # Exports
    # ------------------------------------------------------------------

    def extract_exports(self, root: Node, source: bytes) -> list[ExportInfo]:
        results: list[ExportInfo] = []

        for stmt in self._walk_descendants(root, "export_statement"):
            results.extend(self._parse_export_statement(stmt, source))

        return results

    def _parse_export_statement(
        self, stmt: Node, source: bytes
    ) -> list[ExportInfo]:
        line = stmt.start_point[0] + 1
        text = self._node_text(stmt, source)
        is_default = "default" in text.split("export", 1)[-1].split("(")[0].split("{")[0]

        # Look for a declaration child
        for child in stmt.children:
            ctype = child.type

            if ctype == "function_declaration":
                name = self._extract_identifier_name(child, source) or "default"
                kind = "default" if is_default else "function"
                return [ExportInfo(name=name, kind=kind, line=line)]

            if ctype in (
                "generator_function_declaration",
            ):
                name = self._extract_identifier_name(child, source) or "default"
                kind = "default" if is_default else "function"
                return [ExportInfo(name=name, kind=kind, line=line)]

            if ctype == "class_declaration":
                name = self._extract_identifier_name(child, source) or "default"
                kind = "default" if is_default else "class"
                return [ExportInfo(name=name, kind=kind, line=line)]

            if ctype in ("interface_declaration", "type_alias_declaration"):
                name = self._extract_identifier_name(child, source) or "default"
                return [ExportInfo(name=name, kind="type", line=line)]

            if ctype in ("lexical_declaration", "variable_declaration"):
                return self._exports_from_var_declaration(child, source, line, is_default)

        # Fallback for bare ``export default expr``
        if is_default:
            ident = self._find_child(stmt, "identifier")
            name = self._node_text(ident, source) if ident else "default"
            return [ExportInfo(name=name, kind="default", line=line)]

        return []

    def _exports_from_var_declaration(
        self,
        decl: Node,
        source: bytes,
        line: int,
        is_default: bool,
    ) -> list[ExportInfo]:
        results: list[ExportInfo] = []
        for vd in self._find_children(decl, "variable_declarator"):
            name_node = self._find_child(vd, "identifier")
            if name_node is not None:
                name = self._node_text(name_node, source)
                kind = "default" if is_default else "variable"
                results.append(ExportInfo(name=name, kind=kind, line=line))
        return results

    # ------------------------------------------------------------------
    # Definitions
    # ------------------------------------------------------------------

    def extract_definitions(
        self, root: Node, source: bytes
    ) -> list[DefinitionInfo]:
        results: list[DefinitionInfo] = []

        # Top-level function declarations (including exported ones)
        for node in self._walk_descendants(root, "function_declaration"):
            results.append(self._definition_from_function(node, source, "function"))

        # Generator functions
        for node in self._walk_descendants(root, "generator_function_declaration"):
            results.append(self._definition_from_function(node, source, "function"))

        # Class declarations
        for node in self._walk_descendants(root, "class_declaration"):
            results.append(self._definition_from_class(node, source))

        # Interface declarations
        for node in self._walk_descendants(root, "interface_declaration"):
            name = self._extract_identifier_name(node, source) or ""
            results.append(
                DefinitionInfo(
                    name=name,
                    kind="interface",
                    line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                )
            )

        # Type alias declarations
        for node in self._walk_descendants(root, "type_alias_declaration"):
            name = self._extract_identifier_name(node, source) or ""
            results.append(
                DefinitionInfo(
                    name=name,
                    kind="type_alias",
                    line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                )
            )

        # Method definitions inside classes
        for node in self._walk_descendants(root, "method_definition"):
            results.append(self._definition_from_method(node, source))

        # Arrow functions assigned to const/let/var
        for node in self._walk_descendants(root, "lexical_declaration"):
            for vd in self._find_children(node, "variable_declarator"):
                arrow = self._find_child(vd, "arrow_function")
                if arrow is not None:
                    name_node = self._find_child(vd, "identifier")
                    if name_node is not None:
                        name = self._node_text(name_node, source)
                        text = self._node_text(arrow, source)
                        is_async = text.startswith("async")
                        params = self._extract_parameters(arrow, source)
                        decorators = self._extract_decorators(node, source)
                        results.append(
                            DefinitionInfo(
                                name=name,
                                kind="function",
                                line=node.start_point[0] + 1,
                                end_line=arrow.end_point[0] + 1,
                                is_async=is_async,
                                parameters=params,
                                decorators=decorators,
                            )
                        )

        return results

    def _definition_from_function(
        self, node: Node, source: bytes, kind: str
    ) -> DefinitionInfo:
        name = self._extract_identifier_name(node, source) or ""
        text = self._node_text(node, source)
        is_async = text.startswith("async")
        params = self._extract_parameters(node, source)
        decorators = self._extract_decorators(node, source)
        return DefinitionInfo(
            name=name,
            kind=kind,
            line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            is_async=is_async,
            parameters=params,
            decorators=decorators,
        )

    def _definition_from_class(
        self, node: Node, source: bytes
    ) -> DefinitionInfo:
        name = self._extract_identifier_name(node, source) or ""
        decorators = self._extract_decorators(node, source)
        return DefinitionInfo(
            name=name,
            kind="class",
            line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=decorators,
        )

    def _definition_from_method(
        self, node: Node, source: bytes
    ) -> DefinitionInfo:
        # Method name can be a property_identifier or computed_property_name
        name_node = self._find_child(node, "property_identifier")
        if name_node is None:
            name_node = self._find_child(node, "identifier")
        name = self._node_text(name_node, source) if name_node else ""

        text = self._node_text(node, source)
        is_async = text.startswith("async")
        params = self._extract_parameters(node, source)
        decorators = self._extract_decorators(node, source)
        return DefinitionInfo(
            name=name,
            kind="method",
            line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            is_async=is_async,
            parameters=params,
            decorators=decorators,
        )

    # ------------------------------------------------------------------
    # Components (JSX)
    # ------------------------------------------------------------------

    def extract_components(
        self, root: Node, source: bytes
    ) -> list[ComponentInfo]:
        results: list[ComponentInfo] = []
        seen: set[tuple[str, int]] = set()

        # Full JSX elements: <Component prop1 prop2>...</Component>
        for elem in self._walk_descendants(root, "jsx_element"):
            opening = self._find_child(elem, "jsx_opening_element")
            if opening is None:
                continue
            info = self._component_from_opening(opening, source)
            if info is not None:
                key = (info.name, info.line)
                if key not in seen:
                    seen.add(key)
                    results.append(info)

        # Self-closing JSX elements: <Component prop1 />
        for elem in self._walk_descendants(root, "jsx_self_closing_element"):
            info = self._component_from_opening(elem, source)
            if info is not None:
                key = (info.name, info.line)
                if key not in seen:
                    seen.add(key)
                    results.append(info)

        return results

    def _component_from_opening(
        self, node: Node, source: bytes
    ) -> ComponentInfo | None:
        """Extract a ComponentInfo from a JSX opening or self-closing element.

        Only returns components with PascalCase names (skips HTML tags).
        """
        # Tag name can be identifier, member_expression, or nested_identifier
        tag_node = (
            self._find_child(node, "identifier")
            or self._find_child(node, "member_expression")
            or self._find_child(node, "nested_identifier")
        )
        if tag_node is None:
            return None

        name = self._node_text(tag_node, source)
        if not name or not name[0].isupper():
            return None

        # Collect prop names
        props: list[str] = []
        for attr in self._find_children(node, "jsx_attribute"):
            attr_name_node = self._find_child(attr, "property_identifier")
            if attr_name_node is None:
                attr_name_node = self._find_child(attr, "identifier")
            if attr_name_node is not None:
                props.append(self._node_text(attr_name_node, source))

        return ComponentInfo(
            name=name,
            line=node.start_point[0] + 1,
            props=props,
        )

    # ------------------------------------------------------------------
    # Naming Samples
    # ------------------------------------------------------------------

    def extract_naming_samples(
        self, root: Node, source: bytes
    ) -> list[NamingInfo]:
        results: list[NamingInfo] = []

        for node in self._walk_descendants(root, "function_declaration"):
            name = self._extract_identifier_name(node, source)
            if name:
                results.append(NamingInfo(name=name, kind="function"))
            if len(results) >= _MAX_NAMING_SAMPLES:
                return results

        for node in self._walk_descendants(root, "class_declaration"):
            name = self._extract_identifier_name(node, source)
            if name:
                results.append(NamingInfo(name=name, kind="class"))
            if len(results) >= _MAX_NAMING_SAMPLES:
                return results

        for node in self._walk_descendants(root, "variable_declarator"):
            name_node = self._find_child(node, "identifier")
            if name_node is not None:
                results.append(
                    NamingInfo(
                        name=self._node_text(name_node, source), kind="variable"
                    )
                )
            if len(results) >= _MAX_NAMING_SAMPLES:
                return results

        # Parameters from all formal_parameters blocks
        for fp in self._walk_descendants(root, "formal_parameters"):
            for param in fp.children:
                if param.type in (
                    "required_parameter",
                    "optional_parameter",
                ):
                    ident = self._find_child(param, "identifier")
                    if ident is not None:
                        results.append(
                            NamingInfo(
                                name=self._node_text(ident, source),
                                kind="parameter",
                            )
                        )
                elif param.type == "identifier":
                    results.append(
                        NamingInfo(
                            name=self._node_text(param, source),
                            kind="parameter",
                        )
                    )
                if len(results) >= _MAX_NAMING_SAMPLES:
                    return results

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _extract_module_string(
        self, stmt: Node, source: bytes
    ) -> str | None:
        """Extract the module path string from an import statement node."""
        str_node = self._find_child(stmt, "string")
        if str_node is None:
            return None
        return self._strip_quotes(self._node_text(str_node, source))

    def _extract_identifier_name(
        self, node: Node, source: bytes
    ) -> str | None:
        """Extract the name identifier text from a declaration node."""
        ident = self._find_child(node, "identifier")
        if ident is None:
            ident = self._find_child(node, "type_identifier")
        if ident is None:
            return None
        return self._node_text(ident, source)

    def _extract_parameters(
        self, node: Node, source: bytes
    ) -> list[str]:
        """Extract parameter names from a function/method node."""
        fp = self._find_child(node, "formal_parameters")
        if fp is None:
            return []
        params: list[str] = []
        for child in fp.children:
            if child.type in ("required_parameter", "optional_parameter"):
                ident = self._find_child(child, "identifier")
                if ident is not None:
                    params.append(self._node_text(ident, source))
            elif child.type == "identifier":
                params.append(self._node_text(child, source))
        return params

    def _extract_decorators(
        self, node: Node, source: bytes
    ) -> list[str]:
        """Extract decorator names preceding a declaration.

        In TypeScript, decorators are sibling nodes that appear before
        the declaration in the parent's children list.
        """
        if node.parent is None:
            return []
        decorators: list[str] = []
        for sibling in node.parent.children:
            if sibling == node:
                break
            if sibling.type == "decorator":
                text = self._clean_decorator_text(self._node_text(sibling, source))
                if text:
                    decorators.append(text)
        return decorators
