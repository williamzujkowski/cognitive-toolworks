"""Tests for script analysis module."""

import tempfile
from pathlib import Path

from cognitive_toolworks.sources.scripts import (
    ScriptAnalyzer,
    ScriptLanguage,
    analyze_script,
)


class TestScriptLanguage:
    """Tests for ScriptLanguage enum."""

    def test_from_extension_python(self) -> None:
        """Test Python extension detection."""
        assert ScriptLanguage.from_extension(".py") == ScriptLanguage.PYTHON

    def test_from_extension_typescript(self) -> None:
        """Test TypeScript extension detection."""
        assert ScriptLanguage.from_extension(".ts") == ScriptLanguage.TYPESCRIPT
        assert ScriptLanguage.from_extension(".tsx") == ScriptLanguage.TYPESCRIPT

    def test_from_extension_javascript(self) -> None:
        """Test JavaScript extension detection."""
        assert ScriptLanguage.from_extension(".js") == ScriptLanguage.JAVASCRIPT
        assert ScriptLanguage.from_extension(".jsx") == ScriptLanguage.JAVASCRIPT
        assert ScriptLanguage.from_extension(".mjs") == ScriptLanguage.JAVASCRIPT

    def test_from_extension_bash(self) -> None:
        """Test Bash extension detection."""
        assert ScriptLanguage.from_extension(".sh") == ScriptLanguage.BASH
        assert ScriptLanguage.from_extension(".bash") == ScriptLanguage.BASH

    def test_from_extension_unknown(self) -> None:
        """Test unknown extension."""
        assert ScriptLanguage.from_extension(".xyz") == ScriptLanguage.UNKNOWN


class TestPythonAnalysis:
    """Tests for Python script analysis."""

    def test_analyze_simple_function(self) -> None:
        """Test analyzing a simple Python function."""
        content = '''"""Module docstring."""

def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"
'''
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert result.language == ScriptLanguage.PYTHON
            assert "Module docstring" in result.description
            assert len(result.functions) == 1
            assert result.functions[0].name == "hello"
            assert result.functions[0].return_type == "str"
            assert len(result.functions[0].parameters) == 1
            assert result.functions[0].parameters[0]["name"] == "name"
        finally:
            path.unlink()

    def test_analyze_async_function(self) -> None:
        """Test analyzing an async function."""
        content = '''
async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    pass
'''
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert len(result.functions) == 1
            assert result.functions[0].name == "fetch_data"
            assert result.functions[0].is_async is True
        finally:
            path.unlink()

    def test_analyze_class(self) -> None:
        """Test analyzing a Python class."""
        content = '''
class MyClass:
    """A test class."""

    def __init__(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        """Get the value."""
        return self.value
'''
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert len(result.classes) == 1
            assert result.classes[0].name == "MyClass"
            assert "A test class" in result.classes[0].description
            assert len(result.classes[0].methods) == 2  # __init__ and get_value
        finally:
            path.unlink()

    def test_analyze_imports(self) -> None:
        """Test extracting imports."""
        content = """
import os
import json
from pathlib import Path
from typing import Any

import httpx
from anthropic import Anthropic
"""
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert "os" in result.imports
            assert "json" in result.imports
            assert "pathlib" in result.imports
            assert "httpx" in result.imports
            assert "anthropic" in result.imports
            # Check dependencies (non-stdlib)
            assert "httpx" in result.dependencies
            assert "anthropic" in result.dependencies
            assert "os" not in result.dependencies
        finally:
            path.unlink()

    def test_analyze_env_vars(self) -> None:
        """Test extracting environment variables."""
        content = """
import os

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SECRET = os.getenv("SECRET_TOKEN", "default")
"""
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert "ANTHROPIC_API_KEY" in result.env_vars
            assert "SECRET_TOKEN" in result.env_vars
        finally:
            path.unlink()

    def test_analyze_typer_cli(self) -> None:
        """Test detecting Typer CLI commands."""
        content = """
import typer

app = typer.Typer()

@app.command("hello")
def hello_cmd():
    pass

@app.command()
def goodbye():
    pass
"""
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert len(result.cli_commands) >= 1
            assert any(cmd["framework"] == "typer" for cmd in result.cli_commands)
        finally:
            path.unlink()


class TestJavaScriptAnalysis:
    """Tests for JavaScript/TypeScript analysis."""

    def test_analyze_js_function(self) -> None:
        """Test analyzing JavaScript functions."""
        content = """
export function hello(name) {
    return `Hello, ${name}!`;
}

export const greet = async (name) => {
    return `Hi, ${name}!`;
};
"""
        with tempfile.NamedTemporaryFile(suffix=".js", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert result.language == ScriptLanguage.JAVASCRIPT
            assert len(result.functions) >= 1
            # Check for exported functions
            assert any(f.name == "hello" for f in result.functions)
        finally:
            path.unlink()

    def test_analyze_ts_class(self) -> None:
        """Test analyzing TypeScript class."""
        content = """
export class MyService extends BaseService {
    async getData() {
        return [];
    }
}
"""
        with tempfile.NamedTemporaryFile(suffix=".ts", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert result.language == ScriptLanguage.TYPESCRIPT
            assert len(result.classes) == 1
            assert result.classes[0].name == "MyService"
            assert "BaseService" in result.classes[0].base_classes
        finally:
            path.unlink()

    def test_analyze_js_imports(self) -> None:
        """Test extracting JavaScript imports."""
        content = """
import { something } from 'some-package';
import path from 'path';
const fs = require('fs');
"""
        with tempfile.NamedTemporaryFile(suffix=".js", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert "some-package" in result.imports
            assert "path" in result.imports
            assert "fs" in result.imports
        finally:
            path.unlink()

    def test_analyze_js_env_vars(self) -> None:
        """Test extracting JavaScript environment variables."""
        content = """
const apiKey = process.env.API_KEY;
const secret = process.env['SECRET_TOKEN'];
"""
        with tempfile.NamedTemporaryFile(suffix=".js", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert "API_KEY" in result.env_vars
            assert "SECRET_TOKEN" in result.env_vars
        finally:
            path.unlink()


class TestBashAnalysis:
    """Tests for Bash script analysis."""

    def test_analyze_bash_functions(self) -> None:
        """Test analyzing Bash functions."""
        content = """#!/bin/bash
# This is a test script
# for doing things

function hello() {
    echo "Hello"
}

goodbye() {
    echo "Goodbye"
}
"""
        with tempfile.NamedTemporaryFile(suffix=".sh", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert result.language == ScriptLanguage.BASH
            assert "test script" in result.description
            assert len(result.functions) == 2
            assert any(f.name == "hello" for f in result.functions)
            assert any(f.name == "goodbye" for f in result.functions)
        finally:
            path.unlink()

    def test_analyze_bash_env_vars(self) -> None:
        """Test extracting Bash environment variables."""
        content = """#!/bin/bash
echo $ANTHROPIC_API_KEY
echo ${DATABASE_URL}
"""
        with tempfile.NamedTemporaryFile(suffix=".sh", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert "ANTHROPIC_API_KEY" in result.env_vars
            assert "DATABASE_URL" in result.env_vars
        finally:
            path.unlink()

    def test_analyze_bash_cli_commands(self) -> None:
        """Test extracting Bash CLI subcommands."""
        content = """#!/bin/bash
case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        do_restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        ;;
esac
"""
        with tempfile.NamedTemporaryFile(suffix=".sh", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert len(result.cli_commands) == 3
            cmd_names = [cmd["name"] for cmd in result.cli_commands]
            assert "start" in cmd_names
            assert "stop" in cmd_names
            assert "restart" in cmd_names
        finally:
            path.unlink()


class TestScriptAnalyzer:
    """Tests for ScriptAnalyzer class."""

    def test_analyzer_to_dict(self) -> None:
        """Test converting analysis to dictionary."""
        content = '''"""Test module."""

def test_func():
    pass
'''
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            analyzer = ScriptAnalyzer()
            result = analyzer.analyze(path)
            data = result.to_dict()

            assert "file_path" in data
            assert "language" in data
            assert "functions" in data
            assert data["language"] == "python"
        finally:
            path.unlink()

    def test_unknown_extension(self) -> None:
        """Test handling unknown file extension."""
        with tempfile.NamedTemporaryFile(suffix=".xyz", mode="w", delete=False) as f:
            f.write("some content")
            f.flush()
            path = Path(f.name)

        try:
            result = analyze_script(path)
            assert result.language == ScriptLanguage.UNKNOWN
        finally:
            path.unlink()
