"""
Integration tests for MCP introspection → analysis → generation workflow.

Tests the complete flow:
1. MCPIntrospector extracts tool definitions from MCP server
2. TokenAnalyzer analyzes the extracted tools
3. SkillGenerator creates a valid SKILL.md file
"""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from cognitive_toolworks.analyzers.tokens import TokenAnalyzer
from cognitive_toolworks.generators.skill import GenerationConfig, SkillGenerator
from cognitive_toolworks.models import MCPAnalysis, MCPToolDefinition
from cognitive_toolworks.sources.mcp import MCPConfig, MCPIntrospector
from cognitive_toolworks.validators.anthropic import AnthropicValidator


@pytest.fixture
def sample_mcp_response() -> dict[str, Any]:
    """Sample MCP server response for testing."""
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "tools": [
                {
                    "name": "read_file",
                    "description": "Read the complete contents of a file from the file system.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path of the file to read",
                            }
                        },
                        "required": ["path"],
                    },
                },
                {
                    "name": "write_file",
                    "description": "Create a new file or overwrite an existing file.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path"},
                            "content": {"type": "string", "description": "File content"},
                        },
                        "required": ["path", "content"],
                    },
                },
            ]
        },
    }


@pytest.fixture
def sample_mcp_analysis() -> MCPAnalysis:
    """Sample MCPAnalysis for testing."""
    return MCPAnalysis(
        server_name="filesystem",
        tools=[
            MCPToolDefinition(
                name="read_file",
                description="Read the complete contents of a file from the file system.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the file to read",
                        }
                    },
                    "required": ["path"],
                },
            ),
            MCPToolDefinition(
                name="write_file",
                description="Create a new file or overwrite an existing file.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "The file path"},
                        "content": {"type": "string", "description": "File content"},
                    },
                    "required": ["path", "content"],
                },
            ),
        ],
        resources=[],
        capabilities={"tools": True},
    )


@pytest.mark.integration
class TestMCPWorkflow:
    """Integration tests for complete MCP workflow."""

    def test_mcp_config_loading(self, tmp_path: Path) -> None:
        """Test loading MCP configuration from JSON file."""
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

        config = MCPConfig.from_json(config_file)

        assert config.command == "npx"
        assert "-y" in config.args
        assert "@modelcontextprotocol/server-filesystem" in config.args
        assert config.transport == "stdio"

    @pytest.mark.asyncio
    async def test_mcp_introspection_mock(self, sample_mcp_response: dict[str, Any]) -> None:
        """Test MCP introspection with mocked server response."""
        config = MCPConfig(command="test", args=[], transport="stdio")

        with patch("subprocess.Popen") as mock_popen:
            # Setup mock process
            mock_process = MagicMock()
            mock_process.stdin = MagicMock()
            mock_process.stdout = MagicMock()
            mock_process.stderr = MagicMock()

            # Mock responses
            init_response = {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "test-server", "version": "1.0.0"},
                },
            }

            mock_process.stdout.readline.side_effect = [
                json.dumps(init_response).encode() + b"\n",
                json.dumps(sample_mcp_response).encode() + b"\n",
                json.dumps({"jsonrpc": "2.0", "id": 3, "result": {"resources": []}}).encode()
                + b"\n",
                json.dumps({"jsonrpc": "2.0", "id": 4, "result": {}}).encode() + b"\n",
            ]

            mock_popen.return_value = mock_process

            introspector = MCPIntrospector(config)
            analysis = await introspector.introspect()

            assert analysis is not None
            assert len(analysis.tools) == 2
            assert analysis.tools[0].name == "read_file"
            assert analysis.tools[1].name == "write_file"

    def test_token_analysis_of_mcp_tools(self, sample_mcp_analysis: MCPAnalysis) -> None:
        """Test TokenAnalyzer on MCP tool definitions."""
        analyzer = TokenAnalyzer()

        # Convert MCP analysis to skill-like format with frontmatter
        tools_text = f"""---
name: {sample_mcp_analysis.server_name}
description: MCP server tools
---

# {sample_mcp_analysis.server_name}

## Tools

{chr(10).join([f"- {tool.name}: {tool.description}" for tool in sample_mcp_analysis.tools])}
"""

        metrics = analyzer.analyze(tools_text)

        assert metrics.total_tokens > 0
        # Should have both level1 (frontmatter) and level2 (body) tokens
        assert metrics.level1_tokens > 0
        assert metrics.level2_tokens > 0
        # Should be efficient for simple tool descriptions
        assert metrics.efficiency_score > 0.3

    @pytest.mark.asyncio
    async def test_skill_generation_from_mcp_mock(self, sample_mcp_analysis: MCPAnalysis) -> None:
        """Test SkillGenerator with mocked LLM responses."""
        # This test is simplified - it tests the structure without requiring actual LLM calls
        # In a real scenario, you'd either mock the entire LLM or use actual API calls

        # For now, we'll test that the generator can be instantiated and
        # the analysis structure is correct
        from cognitive_toolworks.models import Platform

        config = GenerationConfig(platform=Platform.UNIVERSAL, num_examples=2)

        # Verify the MCP analysis has the expected structure
        assert sample_mcp_analysis.server_name == "filesystem"
        assert len(sample_mcp_analysis.tools) == 2
        assert sample_mcp_analysis.tools[0].name == "read_file"

        # Test that we can create a generator (actual generation requires API key)
        generator = SkillGenerator(config=config)
        assert generator.config.platform == Platform.UNIVERSAL
        assert generator.config.num_examples == 2

    @pytest.mark.asyncio
    async def test_complete_mcp_to_validated_skill_workflow(self, tmp_path: Path) -> None:
        """
        Test complete workflow: MCP analysis → skill file → validation.

        This is the key integration test that verifies the pipeline.
        Uses a manually created skill to test the validation workflow.
        """
        # Step 1: Create a skill file (simulating generated output)
        skill_content = """---
name: filesystem-mcp-tools
slug: filesystem-mcp-tools
description: File system read and write operations via MCP server integration
capabilities:
  - Read file contents
  - Write file contents
inputs:
  path:
    type: string
    required: true
  content:
    type: string
    required: false
outputs:
  result:
    type: string
keywords:
  - filesystem
  - mcp
  - files
version: 1.0.0
owner: test
license: MIT
---

# Filesystem MCP Tools

## Overview

File system operations through MCP.

## When to Use This Skill

Use when managing files via MCP server.

## Instructions

1. Specify path
2. Execute operation

## Examples

### Example 1

```python
read_file("/path/to/file")
```

## Guidelines

Validate paths before operations.
"""

        # Step 2: Write to file
        skill_file = tmp_path / "SKILL.md"
        skill_file.write_text(skill_content)

        # Step 3: Validate the skill
        validator = AnthropicValidator()
        validation_result = validator.validate_file(skill_file)

        # Assertions
        assert validation_result is not None

        # The skill should be valid or have only minor warnings
        if not validation_result.passed:
            # Log issues for debugging
            for issue in validation_result.errors:
                print(f"ERROR: {issue.field}: {issue.message}")

        # Should have no critical errors (warnings are acceptable)
        assert len(validation_result.errors) == 0

    def test_token_budget_compliance(self, sample_mcp_analysis: MCPAnalysis) -> None:
        """Test that MCP analysis fits within token budgets."""
        analyzer = TokenAnalyzer(level1_budget=100, level2_budget=5000)

        # Convert analysis to markdown-like format
        content = f"""---
name: {sample_mcp_analysis.server_name}
tools: {len(sample_mcp_analysis.tools)}
---

# {sample_mcp_analysis.server_name}

## Tools

{chr(10).join([f"- {tool.name}: {tool.description}" for tool in sample_mcp_analysis.tools])}
"""

        metrics = analyzer.analyze(content)

        # Should fit in Level 2 budget for simple MCP servers
        assert metrics.total_tokens < 5000
        assert not metrics.level2_over_budget
