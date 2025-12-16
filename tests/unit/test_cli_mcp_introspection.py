"""
Unit tests for CLI MCP introspection functionality.

Tests the _introspect_source function with MCP sources.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from cognitive_toolworks.cli import SourceType, _introspect_source
from cognitive_toolworks.models import MCPAnalysis, MCPToolDefinition


@pytest.fixture
def sample_mcp_config(tmp_path: Path) -> Path:
    """Create a sample MCP config file."""
    config_data = {
        "mcpServers": {
            "test-server": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                "transport": "stdio",
            }
        }
    }

    config_file = tmp_path / "mcp_config.json"
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture
def sample_mcp_analysis() -> MCPAnalysis:
    """Sample MCPAnalysis for mocking."""
    return MCPAnalysis(
        server_name="server-filesystem",
        tools=[
            MCPToolDefinition(
                name="read_file",
                description="Read a file from the filesystem",
                input_schema={
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
                required_params=["path"],
            ),
            MCPToolDefinition(
                name="write_file",
                description="Write content to a file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["path", "content"],
                },
                required_params=["path", "content"],
            ),
        ],
        resources=[{"uri": "file:///example", "name": "example"}],
        capabilities=["tools", "resources"],
    )


class TestCLIMCPIntrospection:
    """Test CLI MCP introspection functionality."""

    def test_introspect_mcp_success(
        self, sample_mcp_config: Path, sample_mcp_analysis: MCPAnalysis
    ) -> None:
        """Test successful MCP introspection via CLI."""
        with patch("cognitive_toolworks.sources.mcp.MCPIntrospector") as mock_introspector:
            # Setup mock with async coroutine
            mock_instance = MagicMock()

            async def mock_introspect() -> MCPAnalysis:
                return sample_mcp_analysis

            mock_instance.introspect = mock_introspect
            mock_introspector.return_value = mock_instance

            # Call introspect
            result = _introspect_source(SourceType.MCP, sample_mcp_config)

            # Verify result structure
            assert result["source_type"] == "mcp"
            assert result["server_name"] == "server-filesystem"
            assert len(result["tools"]) == 2
            assert result["tools"][0]["name"] == "read_file"
            assert result["tools"][1]["name"] == "write_file"
            assert len(result["resources"]) == 1
            assert "tools" in result["capabilities"]

    def test_introspect_mcp_config_not_found(self, tmp_path: Path) -> None:
        """Test MCP introspection with missing config file."""
        non_existent = tmp_path / "does_not_exist.json"

        with pytest.raises(typer.Exit) as exc_info:
            _introspect_source(SourceType.MCP, non_existent)

        assert exc_info.value.exit_code == 1

    def test_introspect_mcp_invalid_json(self, tmp_path: Path) -> None:
        """Test MCP introspection with invalid JSON."""
        invalid_json = tmp_path / "invalid.json"
        invalid_json.write_text("{not valid json")

        with pytest.raises(typer.Exit) as exc_info:
            _introspect_source(SourceType.MCP, invalid_json)

        assert exc_info.value.exit_code == 1

    def test_introspect_mcp_invalid_config_format(self, tmp_path: Path) -> None:
        """Test MCP introspection with invalid config format."""
        invalid_config = tmp_path / "invalid_config.json"
        invalid_config.write_text(json.dumps({"mcpServers": {}}))

        with pytest.raises(typer.Exit) as exc_info:
            _introspect_source(SourceType.MCP, invalid_config)

        assert exc_info.value.exit_code == 1

    def test_introspect_mcp_server_error(self, sample_mcp_config: Path) -> None:
        """Test MCP introspection with server runtime error."""
        with patch("cognitive_toolworks.sources.mcp.MCPIntrospector") as mock_introspector:
            mock_instance = MagicMock()

            # Simulate async function that raises RuntimeError
            async def mock_introspect() -> None:
                raise RuntimeError("Server failed to start")

            mock_instance.introspect = mock_introspect
            mock_introspector.return_value = mock_instance

            with pytest.raises(typer.Exit) as exc_info:
                _introspect_source(SourceType.MCP, sample_mcp_config)

            assert exc_info.value.exit_code == 1

    def test_introspect_mcp_server_timeout(self, sample_mcp_config: Path) -> None:
        """Test MCP introspection with server timeout."""
        import subprocess

        with patch("cognitive_toolworks.sources.mcp.MCPIntrospector") as mock_introspector:
            mock_instance = MagicMock()

            async def mock_introspect() -> None:
                raise subprocess.TimeoutExpired("test", 5)

            mock_instance.introspect = mock_introspect
            mock_introspector.return_value = mock_instance

            with pytest.raises(typer.Exit) as exc_info:
                _introspect_source(SourceType.MCP, sample_mcp_config)

            assert exc_info.value.exit_code == 1

    def test_introspect_mcp_unknown_error(self, sample_mcp_config: Path) -> None:
        """Test MCP introspection with unexpected error."""
        with patch("cognitive_toolworks.sources.mcp.MCPIntrospector") as mock_introspector:
            mock_instance = MagicMock()

            async def mock_introspect() -> None:
                raise Exception("Unexpected error")

            mock_instance.introspect = mock_introspect
            mock_introspector.return_value = mock_instance

            with pytest.raises(typer.Exit) as exc_info:
                _introspect_source(SourceType.MCP, sample_mcp_config)

            assert exc_info.value.exit_code == 1

    def test_introspect_mcp_converts_to_dict(
        self, sample_mcp_config: Path, sample_mcp_analysis: MCPAnalysis
    ) -> None:
        """Test that MCP introspection properly converts MCPAnalysis to dict."""
        with patch("cognitive_toolworks.sources.mcp.MCPIntrospector") as mock_introspector:
            mock_instance = MagicMock()

            async def mock_introspect() -> MCPAnalysis:
                return sample_mcp_analysis

            mock_instance.introspect = mock_introspect
            mock_introspector.return_value = mock_instance

            result = _introspect_source(SourceType.MCP, sample_mcp_config)

            # Verify all expected dict keys are present
            assert "source_type" in result
            assert "server_name" in result
            assert "tools" in result
            assert "resources" in result
            assert "capabilities" in result

            # Verify tools are properly converted to dicts
            assert isinstance(result["tools"], list)
            for tool in result["tools"]:
                assert isinstance(tool, dict)
                assert "name" in tool
                assert "description" in tool
                assert "input_schema" in tool
