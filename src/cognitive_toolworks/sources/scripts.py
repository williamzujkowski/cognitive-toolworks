"""
Script Analysis Module.

Analyzes Python, TypeScript/JavaScript, and Bash scripts to extract
capabilities, functions, and usage patterns for skill generation.
"""

from __future__ import annotations

import ast
import contextlib
import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


class ScriptLanguage(StrEnum):
    """Supported script languages."""

    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    BASH = "bash"
    UNKNOWN = "unknown"

    @classmethod
    def from_extension(cls, ext: str) -> ScriptLanguage:
        """Determine language from file extension."""
        mapping = {
            ".py": cls.PYTHON,
            ".ts": cls.TYPESCRIPT,
            ".tsx": cls.TYPESCRIPT,
            ".js": cls.JAVASCRIPT,
            ".jsx": cls.JAVASCRIPT,
            ".mjs": cls.JAVASCRIPT,
            ".sh": cls.BASH,
            ".bash": cls.BASH,
        }
        return mapping.get(ext.lower(), cls.UNKNOWN)


@dataclass
class FunctionInfo:
    """Information about a function/method in a script."""

    name: str
    description: str
    parameters: list[dict[str, Any]]
    return_type: str | None
    is_async: bool
    is_exported: bool
    line_number: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "return_type": self.return_type,
            "is_async": self.is_async,
            "is_exported": self.is_exported,
            "line_number": self.line_number,
        }


@dataclass
class ClassInfo:
    """Information about a class in a script."""

    name: str
    description: str
    methods: list[FunctionInfo]
    base_classes: list[str]
    line_number: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "methods": [m.to_dict() for m in self.methods],
            "base_classes": self.base_classes,
            "line_number": self.line_number,
        }


@dataclass
class ScriptAnalysis:
    """Analysis result from script parsing."""

    file_path: str
    language: ScriptLanguage
    description: str
    functions: list[FunctionInfo] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    cli_commands: list[dict[str, Any]] = field(default_factory=list)
    env_vars: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file_path": self.file_path,
            "language": self.language.value,
            "description": self.description,
            "functions": [f.to_dict() for f in self.functions],
            "classes": [c.to_dict() for c in self.classes],
            "imports": self.imports,
            "exports": self.exports,
            "cli_commands": self.cli_commands,
            "env_vars": self.env_vars,
            "dependencies": self.dependencies,
        }


class ScriptAnalyzer:
    """
    Analyzes scripts to extract capabilities and structure.

    Supports Python, TypeScript/JavaScript, and Bash scripts.
    """

    def analyze(self, path: Path) -> ScriptAnalysis:
        """
        Analyze a script file.

        Args:
            path: Path to the script file.

        Returns:
            ScriptAnalysis with extracted information.
        """
        content = path.read_text(encoding="utf-8")
        language = ScriptLanguage.from_extension(path.suffix)

        if language == ScriptLanguage.PYTHON:
            return self._analyze_python(path, content)
        elif language in (ScriptLanguage.TYPESCRIPT, ScriptLanguage.JAVASCRIPT):
            return self._analyze_js_ts(path, content, language)
        elif language == ScriptLanguage.BASH:
            return self._analyze_bash(path, content)
        else:
            return ScriptAnalysis(
                file_path=str(path),
                language=language,
                description="Unknown script type",
            )

    def _analyze_python(self, path: Path, content: str) -> ScriptAnalysis:
        """Analyze a Python script."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return ScriptAnalysis(
                file_path=str(path),
                language=ScriptLanguage.PYTHON,
                description="Failed to parse Python file",
            )

        # Extract module docstring
        description = ast.get_docstring(tree) or ""

        # Extract functions
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                func_info = self._extract_python_function(node)
                if not func_info.name.startswith("_") or func_info.name.startswith("__"):
                    functions.append(func_info)

        # Extract classes
        classes = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                class_info = self._extract_python_class(node)
                classes.append(class_info)

        # Extract imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        # Extract environment variables
        env_vars = self._extract_env_vars(content)

        # Extract CLI commands (argparse, click, typer patterns)
        cli_commands = self._extract_python_cli(tree, content)

        return ScriptAnalysis(
            file_path=str(path),
            language=ScriptLanguage.PYTHON,
            description=description[:500] if description else "",
            functions=functions,
            classes=classes,
            imports=imports,
            env_vars=env_vars,
            cli_commands=cli_commands,
            dependencies=self._extract_python_deps(imports),
        )

    def _extract_python_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> FunctionInfo:
        """Extract function information from AST node."""
        docstring = ast.get_docstring(node) or ""

        # Extract parameters
        params = []
        for arg in node.args.args:
            param = {"name": arg.arg}
            if arg.annotation:
                param["type"] = ast.unparse(arg.annotation)
            params.append(param)

        # Extract return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)

        return FunctionInfo(
            name=node.name,
            description=docstring[:200] if docstring else "",
            parameters=params,
            return_type=return_type,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_exported=not node.name.startswith("_"),
            line_number=node.lineno,
        )

    def _extract_python_class(self, node: ast.ClassDef) -> ClassInfo:
        """Extract class information from AST node."""
        docstring = ast.get_docstring(node) or ""

        # Extract base classes
        bases = []
        for base in node.bases:
            with contextlib.suppress(ValueError, AttributeError):
                bases.append(ast.unparse(base))

        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef):
                if not item.name.startswith("_") or item.name in (
                    "__init__",
                    "__call__",
                ):
                    methods.append(self._extract_python_function(item))

        return ClassInfo(
            name=node.name,
            description=docstring[:200] if docstring else "",
            methods=methods,
            base_classes=bases,
            line_number=node.lineno,
        )

    def _extract_python_cli(self, _tree: ast.Module, content: str) -> list[dict[str, Any]]:
        """Extract CLI command definitions."""
        commands = []

        # Check for typer patterns
        if "typer" in content.lower():
            # Look for @app.command() decorators
            for match in re.finditer(r'@\w+\.command\(["\']?(\w+)?["\']?\)', content):
                cmd_name = match.group(1) or "default"
                commands.append({"name": cmd_name, "framework": "typer"})

        # Check for click patterns
        if "click" in content.lower():
            for match in re.finditer(r'@click\.command\(["\']?(\w+)?["\']?\)', content):
                cmd_name = match.group(1) or "default"
                commands.append({"name": cmd_name, "framework": "click"})

        # Check for argparse patterns
        if "argparse" in content.lower():
            for match in re.finditer(r'add_subparsers|add_parser\(["\'](\w+)', content):
                if match.group(1):
                    commands.append({"name": match.group(1), "framework": "argparse"})

        return commands

    def _extract_python_deps(self, imports: list[str]) -> list[str]:
        """Extract third-party dependencies from imports."""
        stdlib = {
            "os",
            "sys",
            "re",
            "json",
            "pathlib",
            "typing",
            "dataclasses",
            "enum",
            "abc",
            "collections",
            "itertools",
            "functools",
            "contextlib",
            "asyncio",
            "subprocess",
            "io",
            "datetime",
            "time",
            "math",
            "random",
            "copy",
            "pickle",
            "hashlib",
            "base64",
            "urllib",
            "http",
            "logging",
            "unittest",
            "tempfile",
            "shutil",
            "glob",
            "fnmatch",
            "stat",
            "argparse",
            "configparser",
            "csv",
            "xml",
            "html",
            "socket",
            "ssl",
            "threading",
            "multiprocessing",
            "queue",
            "concurrent",
            "ast",
            "inspect",
            "traceback",
            "warnings",
            "textwrap",
            "string",
            "struct",
            "codecs",
            "locale",
            "gettext",
            "secrets",
            "uuid",
            "pprint",
        }

        deps = []
        for imp in imports:
            # Get the top-level package name
            top_level = imp.split(".")[0]
            if top_level not in stdlib and top_level not in deps:
                deps.append(top_level)

        return deps

    def _analyze_js_ts(self, path: Path, content: str, language: ScriptLanguage) -> ScriptAnalysis:
        """Analyze a JavaScript/TypeScript file using regex patterns."""
        description = ""

        # Extract file-level JSDoc comment
        jsdoc_match = re.match(r"/\*\*\s*\n(.*?)\*/", content, re.DOTALL)
        if jsdoc_match:
            description = re.sub(r"\s*\*\s*", " ", jsdoc_match.group(1)).strip()

        # Extract functions
        functions = []
        # Match: function name(...) or const name = (...) => or async function
        func_patterns = [
            r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)",
            r"(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
            r"(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?function",
        ]

        for pattern in func_patterns:
            for match in re.finditer(pattern, content):
                name = match.group(1)
                is_exported = "export" in match.group(0)
                is_async = "async" in match.group(0)

                # Get line number
                line_num = content[: match.start()].count("\n") + 1

                functions.append(
                    FunctionInfo(
                        name=name,
                        description="",
                        parameters=[],
                        return_type=None,
                        is_async=is_async,
                        is_exported=is_exported,
                        line_number=line_num,
                    )
                )

        # Extract classes
        classes = []
        class_pattern = r"(?:export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?"
        for match in re.finditer(class_pattern, content):
            name = match.group(1)
            base = match.group(2)
            line_num = content[: match.start()].count("\n") + 1

            classes.append(
                ClassInfo(
                    name=name,
                    description="",
                    methods=[],
                    base_classes=[base] if base else [],
                    line_number=line_num,
                )
            )

        # Extract imports
        imports = []
        import_patterns = [
            r'import\s+.*?from\s+["\']([^"\']+)["\']',
            r'require\(["\']([^"\']+)["\']\)',
        ]
        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                imports.append(match.group(1))

        # Extract exports
        exports = []
        export_pattern = r"export\s+(?:const|let|var|function|class|async\s+function)\s+(\w+)"
        for match in re.finditer(export_pattern, content):
            exports.append(match.group(1))

        # Extract environment variables
        env_vars = self._extract_env_vars(content)

        return ScriptAnalysis(
            file_path=str(path),
            language=language,
            description=description[:500],
            functions=functions,
            classes=classes,
            imports=imports,
            exports=exports,
            env_vars=env_vars,
        )

    def _analyze_bash(self, path: Path, content: str) -> ScriptAnalysis:
        """Analyze a Bash script."""
        description = ""

        # Extract script description from header comments
        lines = content.split("\n")
        desc_lines = []
        for line in lines[1:20]:  # Skip shebang, check first 20 lines
            if line.startswith("#") and not line.startswith("#!"):
                desc_lines.append(line[1:].strip())
            elif line.strip() and not line.startswith("#"):
                break
        description = " ".join(desc_lines)

        # Extract functions
        functions = []
        func_pattern = r"(?:function\s+)?(\w+)\s*\(\s*\)\s*\{"
        for match in re.finditer(func_pattern, content):
            name = match.group(1)
            if name not in ("if", "while", "for", "case"):
                line_num = content[: match.start()].count("\n") + 1
                functions.append(
                    FunctionInfo(
                        name=name,
                        description="",
                        parameters=[],
                        return_type=None,
                        is_async=False,
                        is_exported=True,
                        line_number=line_num,
                    )
                )

        # Extract environment variables
        env_vars = self._extract_env_vars(content)

        # Extract CLI commands (subcommands from case statements)
        cli_commands = []
        case_pattern = r'case\s+["\']?\$\{?1\}?["\']?\s+in(.*?)esac'
        case_match = re.search(case_pattern, content, re.DOTALL)
        if case_match:
            case_content = case_match.group(1)
            cmd_pattern = r"([a-z_-]+)\)"
            for cmd_match in re.finditer(cmd_pattern, case_content):
                cmd = cmd_match.group(1)
                if cmd not in ("*", "-*", "--*"):
                    cli_commands.append({"name": cmd, "framework": "bash"})

        return ScriptAnalysis(
            file_path=str(path),
            language=ScriptLanguage.BASH,
            description=description[:500],
            functions=functions,
            cli_commands=cli_commands,
            env_vars=env_vars,
        )

    def _extract_env_vars(self, content: str) -> list[str]:
        """Extract environment variable references."""
        env_vars = set()

        # Python: os.environ, os.getenv
        patterns = [
            r'os\.environ(?:\.get)?\(["\'](\w+)["\']',
            r'os\.getenv\(["\'](\w+)["\']',
            r'environ\[["\'](\w+)["\']',
            # JavaScript: process.env
            r"process\.env\.(\w+)",
            r'process\.env\[["\'](\w+)["\']',
            # Bash: $VAR, ${VAR}
            r"\$\{?([A-Z][A-Z0-9_]*)\}?",
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                env_vars.add(match.group(1))

        # Filter out common non-env vars
        filtered = {
            v for v in env_vars if v not in ("PATH", "HOME", "USER", "PWD", "SHELL") and len(v) > 2
        }

        return sorted(filtered)


def analyze_script(path: Path) -> ScriptAnalysis:
    """
    Convenience function to analyze a script file.

    Args:
        path: Path to the script file.

    Returns:
        ScriptAnalysis with extracted information.
    """
    analyzer = ScriptAnalyzer()
    return analyzer.analyze(path)
