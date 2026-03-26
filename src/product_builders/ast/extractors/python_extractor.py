"""Python-specific AST extractor using tree-sitter."""

from __future__ import annotations

from tree_sitter import Node

from product_builders.ast.extractors.base import BaseExtractor
from product_builders.ast.models import (
    DefinitionInfo,
    ExportInfo,
    ImportInfo,
    NamingInfo,
)


class PythonExtractor(BaseExtractor):
    """Extract imports, exports, definitions, and naming samples from Python."""

    # -- Imports ---------------------------------------------------------------

    def extract_imports(self, root: Node, source: bytes) -> list[ImportInfo]:
        """Extract import and from-import statements."""
        results: list[ImportInfo] = []

        for node in root.children:
            try:
                if node.type == "import_statement":
                    results.extend(self._parse_import_statement(node, source))
                elif node.type == "import_from_statement":
                    results.extend(self._parse_import_from_statement(node, source))
            except Exception:  # noqa: BLE001
                continue

        return results

    def _parse_import_statement(
        self, node: Node, source: bytes
    ) -> list[ImportInfo]:
        """Parse `import x` and `import x as y` statements."""
        results: list[ImportInfo] = []
        line = node.start_point[0] + 1

        for child in node.children:
            if child.type == "dotted_name":
                module = self._node_text(child, source)
                results.append(
                    ImportInfo(module=module, names=[module], line=line)
                )
            elif child.type == "aliased_import":
                name_node = self._find_child(child, "dotted_name")
                alias_node = self._find_child(child, "identifier")
                if name_node is not None:
                    module = self._node_text(name_node, source)
                    alias = (
                        self._node_text(alias_node, source)
                        if alias_node is not None
                        else None
                    )
                    results.append(
                        ImportInfo(
                            module=module,
                            names=[module],
                            alias=alias,
                            line=line,
                        )
                    )

        return results

    def _parse_import_from_statement(
        self, node: Node, source: bytes
    ) -> list[ImportInfo]:
        """Parse `from x import y` statements."""
        line = node.start_point[0] + 1

        # Extract the module name (dotted_name or relative_import)
        module_node = self._find_child(node, "dotted_name")
        if module_node is None:
            module_node = self._find_child(node, "relative_import")
        module = self._node_text(module_node, source) if module_node else ""

        # Check for wildcard import: from x import *
        wildcard = self._find_child(node, "wildcard_import")
        if wildcard is not None:
            return [ImportInfo(module=module, is_star=True, line=line)]

        # Collect imported names from the import list or bare identifiers
        names: list[str] = []
        alias: str | None = None

        import_list = self._find_child(node, "import_list")
        if import_list is not None:
            for item in import_list.children:
                if item.type == "dotted_name" or item.type == "identifier":
                    names.append(self._node_text(item, source))
                elif item.type == "aliased_import":
                    name_node = self._find_child(item, "dotted_name")
                    if name_node is None:
                        name_node = self._find_child(item, "identifier")
                    if name_node is not None:
                        names.append(self._node_text(name_node, source))
        else:
            # Single import without parenthesized list
            for child in node.children:
                if child.type == "dotted_name" and child != module_node:
                    names.append(self._node_text(child, source))
                elif child.type == "identifier":
                    names.append(self._node_text(child, source))
                elif child.type == "aliased_import":
                    name_node = self._find_child(child, "dotted_name")
                    if name_node is None:
                        name_node = self._find_child(child, "identifier")
                    alias_id = self._find_child(child, "identifier")
                    if name_node is not None:
                        imported = self._node_text(name_node, source)
                        names.append(imported)
                        # The alias is the identifier that comes after 'as'
                        # In aliased_import, children are: name, 'as', alias
                        ids = self._find_children(child, "identifier")
                        if len(ids) >= 2:
                            alias = self._node_text(ids[-1], source)
                        elif alias_id is not None and name_node.type == "dotted_name":
                            alias = self._node_text(alias_id, source)

        if not names and not alias:
            return []

        return [
            ImportInfo(module=module, names=names, alias=alias, line=line)
        ]

    # -- Exports ---------------------------------------------------------------

    def extract_exports(self, root: Node, source: bytes) -> list[ExportInfo]:
        """Extract exported symbols.

        Python has no formal export syntax. We use heuristics:
        - If ``__all__`` is defined, only those names are exported.
        - Otherwise, all public (non-underscore-prefixed) top-level definitions.
        """
        dunder_all = self._find_dunder_all(root, source)
        if dunder_all is not None:
            return dunder_all

        results: list[ExportInfo] = []
        for node in root.children:
            try:
                results.extend(self._exports_from_node(node, source))
            except Exception:  # noqa: BLE001
                continue
        return results

    def _find_dunder_all(
        self, root: Node, source: bytes
    ) -> list[ExportInfo] | None:
        """Look for ``__all__ = [...]`` and extract its string entries."""
        for node in root.children:
            if node.type != "expression_statement":
                continue
            assign = self._find_child(node, "assignment")
            if assign is None:
                continue
            left = assign.children[0] if assign.children else None
            if left is None:
                continue
            if self._node_text(left, source) != "__all__":
                continue

            # Found __all__, extract string values from the list
            list_node = self._find_child(assign, "list")
            if list_node is None:
                continue

            results: list[ExportInfo] = []
            line = node.start_point[0] + 1
            for item in list_node.children:
                if item.type == "string":
                    # Strip quotes from string literal
                    text = self._node_text(item, source)
                    name = text.strip("\"'")
                    if name:
                        results.append(ExportInfo(name=name, line=line))
            return results

        return None

    def _exports_from_node(
        self, node: Node, source: bytes
    ) -> list[ExportInfo]:
        """Get export entries from a single top-level node."""
        if node.type == "function_definition":
            name = self._def_name(node, source)
            if name and not name.startswith("_"):
                return [
                    ExportInfo(
                        name=name,
                        kind="function",
                        line=node.start_point[0] + 1,
                    )
                ]

        elif node.type == "class_definition":
            name = self._def_name(node, source)
            if name and not name.startswith("_"):
                return [
                    ExportInfo(
                        name=name,
                        kind="class",
                        line=node.start_point[0] + 1,
                    )
                ]

        elif node.type == "decorated_definition":
            inner = self._unwrap_decorated(node)
            if inner is not None:
                return self._exports_from_node(inner, source)

        elif node.type == "expression_statement":
            assign = self._find_child(node, "assignment")
            if assign is not None:
                names = self._assignment_targets(assign, source)
                return [
                    ExportInfo(
                        name=n,
                        kind="variable",
                        line=node.start_point[0] + 1,
                    )
                    for n in names
                    if not n.startswith("_")
                ]

        return []

    # -- Definitions -----------------------------------------------------------

    def extract_definitions(
        self, root: Node, source: bytes
    ) -> list[DefinitionInfo]:
        """Extract function, class, and method definitions."""
        results: list[DefinitionInfo] = []

        for node in root.children:
            try:
                results.extend(
                    self._definitions_from_node(node, source, is_method=False)
                )
            except Exception:  # noqa: BLE001
                continue

        return results

    def _definitions_from_node(
        self,
        node: Node,
        source: bytes,
        *,
        is_method: bool,
        decorators: list[str] | None = None,
    ) -> list[DefinitionInfo]:
        """Recursively extract definitions from a node."""
        results: list[DefinitionInfo] = []

        if node.type == "decorated_definition":
            collected_decorators = self._collect_decorators(node, source)
            inner = self._unwrap_decorated(node)
            if inner is not None:
                results.extend(
                    self._definitions_from_node(
                        inner,
                        source,
                        is_method=is_method,
                        decorators=collected_decorators,
                    )
                )
            return results

        if node.type == "function_definition":
            name = self._def_name(node, source)
            if not name:
                return results

            is_async = self._is_async_function(node, source)
            params = self._extract_parameters(node, source, skip_self=is_method)
            kind = "method" if is_method else "function"

            results.append(
                DefinitionInfo(
                    name=name,
                    kind=kind,
                    line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    decorators=decorators or [],
                    is_async=is_async,
                    parameters=params,
                )
            )

        elif node.type == "class_definition":
            name = self._def_name(node, source)
            if not name:
                return results

            results.append(
                DefinitionInfo(
                    name=name,
                    kind="class",
                    line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    decorators=decorators or [],
                )
            )

            # Walk class body for methods
            body = self._find_child(node, "block")
            if body is not None:
                for child in body.children:
                    try:
                        results.extend(
                            self._definitions_from_node(
                                child, source, is_method=True
                            )
                        )
                    except Exception:  # noqa: BLE001
                        continue

        return results

    # -- Naming Samples --------------------------------------------------------

    def extract_naming_samples(
        self, root: Node, source: bytes
    ) -> list[NamingInfo]:
        """Collect naming samples for convention detection."""
        samples: list[NamingInfo] = []
        max_samples = 100

        for node in root.children:
            if len(samples) >= max_samples:
                break
            try:
                samples.extend(
                    self._naming_from_node(node, source, max_samples - len(samples))
                )
            except Exception:  # noqa: BLE001
                continue

        return samples[:max_samples]

    def _naming_from_node(
        self, node: Node, source: bytes, remaining: int
    ) -> list[NamingInfo]:
        """Collect naming samples from a single top-level node."""
        if remaining <= 0:
            return []

        results: list[NamingInfo] = []

        if node.type == "function_definition":
            name = self._def_name(node, source)
            if name:
                results.append(NamingInfo(name=name, kind="function"))
                # Collect parameter names
                results.extend(self._param_naming(node, source))

        elif node.type == "class_definition":
            name = self._def_name(node, source)
            if name:
                results.append(NamingInfo(name=name, kind="class"))
            # Walk class body for method names and their parameters
            body = self._find_child(node, "block")
            if body is not None:
                for child in body.children:
                    if len(results) >= remaining:
                        break
                    inner = child
                    if child.type == "decorated_definition":
                        inner = self._unwrap_decorated(child)
                        if inner is None:
                            continue
                    if inner.type == "function_definition":
                        mname = self._def_name(inner, source)
                        if mname:
                            results.append(NamingInfo(name=mname, kind="function"))
                            results.extend(self._param_naming(inner, source))

        elif node.type == "decorated_definition":
            inner = self._unwrap_decorated(node)
            if inner is not None:
                results.extend(self._naming_from_node(inner, source, remaining))

        elif node.type == "expression_statement":
            assign = self._find_child(node, "assignment")
            if assign is not None:
                names = self._assignment_targets(assign, source)
                for n in names:
                    results.append(NamingInfo(name=n, kind="variable"))

        return results

    def _param_naming(
        self, func_node: Node, source: bytes
    ) -> list[NamingInfo]:
        """Extract parameter names from a function for naming samples."""
        params = self._extract_parameters(func_node, source, skip_self=True)
        return [NamingInfo(name=p, kind="parameter") for p in params]

    # -- Shared Helpers --------------------------------------------------------

    @staticmethod
    def _unwrap_decorated(node: Node) -> Node | None:
        """Return the inner function/class from a decorated_definition."""
        for child in node.children:
            if child.type in ("function_definition", "class_definition"):
                return child
        return None

    def _collect_decorators(
        self, node: Node, source: bytes
    ) -> list[str]:
        """Collect decorator names from a decorated_definition."""
        decorators: list[str] = []
        for child in node.children:
            if child.type == "decorator":
                text = self._clean_decorator_text(self._node_text(child, source))
                if text:
                    decorators.append(text)
        return decorators

    def _def_name(self, node: Node, source: bytes) -> str:
        """Get the name identifier from a function or class definition."""
        name_node = self._find_child(node, "identifier")
        return self._node_text(name_node, source) if name_node else ""

    def _is_async_function(self, node: Node, source: bytes) -> bool:
        """Check if a function definition is async."""
        text = self._node_text(node, source)
        return text.startswith("async ")

    def _extract_parameters(
        self, func_node: Node, source: bytes, *, skip_self: bool
    ) -> list[str]:
        """Extract parameter names from a function definition's parameters node."""
        params_node = self._find_child(func_node, "parameters")
        if params_node is None:
            return []

        skip_names = {"self", "cls"} if skip_self else set()
        names: list[str] = []

        for child in params_node.children:
            name = self._param_name(child, source)
            if name and name not in skip_names:
                names.append(name)

        return names

    def _param_name(self, node: Node, source: bytes) -> str:
        """Extract the parameter name from various parameter node types."""
        if node.type == "identifier":
            return self._node_text(node, source)

        if node.type in (
            "typed_parameter",
            "default_parameter",
            "typed_default_parameter",
        ):
            ident = self._find_child(node, "identifier")
            if ident is not None:
                return self._node_text(ident, source)
            # typed_default_parameter may have a typed_parameter child
            typed = self._find_child(node, "typed_parameter")
            if typed is not None:
                ident = self._find_child(typed, "identifier")
                if ident is not None:
                    return self._node_text(ident, source)

        if node.type == "list_splat_pattern":
            ident = self._find_child(node, "identifier")
            if ident is not None:
                return "*" + self._node_text(ident, source)

        if node.type == "dictionary_splat_pattern":
            ident = self._find_child(node, "identifier")
            if ident is not None:
                return "**" + self._node_text(ident, source)

        return ""

    def _assignment_targets(
        self, assign: Node, source: bytes
    ) -> list[str]:
        """Extract target variable names from an assignment node."""
        if not assign.children:
            return []
        left = assign.children[0]
        if left.type == "identifier":
            return [self._node_text(left, source)]
        if left.type == "pattern_list":
            return [
                self._node_text(c, source)
                for c in left.children
                if c.type == "identifier"
            ]
        return []
