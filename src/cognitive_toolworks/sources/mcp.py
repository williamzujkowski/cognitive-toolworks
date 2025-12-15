"""
MCP Server Introspection Module.

Extracts tool definitions, resources, and capabilities from MCP servers.
Supports both stdio and SSE transport methods.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from cognitive_toolworks.models import MCPAnalysis, MCPToolDefinition

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class MCPConfig:
    """Configuration for connecting to an MCP server."""

    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    transport: str = "stdio"  # stdio or sse

    @classmethod
    def from_json(cls, path: Path) -> MCPConfig:
        """Load config from a JSON file."""
        data = json.loads(path.read_text())

        # Handle both direct config and mcpServers wrapper format
        if "mcpServers" in data:
            # Claude Desktop style: {"mcpServers": {"name": {...}}}
            servers = data["mcpServers"]
            if not servers:
                raise ValueError("No MCP servers defined in config")
            # Take the first server
            name = next(iter(servers))
            server_config = servers[name]
        else:
            server_config = data

        return cls(
            command=server_config.get("command", ""),
            args=server_config.get("args", []),
            env=server_config.get("env", {}),
            transport=server_config.get("transport", "stdio"),
        )


class MCPIntrospector:
    """
    Introspects MCP servers to extract tool and resource definitions.

    Communicates with MCP servers via JSON-RPC over stdio to discover
    available tools, their schemas, and server capabilities.
    """

    def __init__(self, config: MCPConfig) -> None:
        self.config = config
        self._process: subprocess.Popen[bytes] | None = None
        self._request_id = 0

    async def introspect(self) -> MCPAnalysis:
        """
        Perform full introspection of the MCP server.

        Returns:
            MCPAnalysis containing tools, resources, and capabilities.
        """
        try:
            await self._start_server()

            # Initialize connection
            await self._initialize()

            # Get tools
            tools = await self._list_tools()

            # Get resources
            resources = await self._list_resources()

            # Get capabilities from init response
            capabilities = await self._get_capabilities()

            return MCPAnalysis(
                server_name=self._extract_server_name(),
                tools=tools,
                resources=resources,
                capabilities=capabilities,
            )
        finally:
            await self._stop_server()

    async def _start_server(self) -> None:
        """Start the MCP server process."""
        env = {**dict(subprocess.os.environ), **self.config.env}

        self._process = subprocess.Popen(
            [self.config.command, *self.config.args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

    async def _stop_server(self) -> None:
        """Stop the MCP server process."""
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None

    async def _send_request(
        self, method: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Send a JSON-RPC request and wait for response."""
        if not self._process or not self._process.stdin or not self._process.stdout:
            raise RuntimeError("MCP server not running")

        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
        }
        if params:
            request["params"] = params

        # Send request
        request_bytes = json.dumps(request).encode() + b"\n"
        self._process.stdin.write(request_bytes)
        self._process.stdin.flush()

        # Read response (simple line-based for now)
        response_line = self._process.stdout.readline()
        if not response_line:
            raise RuntimeError("No response from MCP server")

        response = json.loads(response_line.decode())

        if "error" in response:
            raise RuntimeError(f"MCP error: {response['error']}")

        return response.get("result", {})

    async def _initialize(self) -> dict[str, Any]:
        """Initialize the MCP connection."""
        return await self._send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "cognitive-toolworks",
                    "version": "2.0.0",
                },
            },
        )

    async def _list_tools(self) -> list[MCPToolDefinition]:
        """List all available tools."""
        result = await self._send_request("tools/list")
        tools = []

        for tool_data in result.get("tools", []):
            tool = MCPToolDefinition(
                name=tool_data.get("name", ""),
                description=tool_data.get("description", ""),
                input_schema=tool_data.get("inputSchema", {}),
                required_params=tool_data.get("inputSchema", {}).get("required", []),
            )
            tools.append(tool)

        return tools

    async def _list_resources(self) -> list[dict[str, Any]]:
        """List all available resources."""
        try:
            result = await self._send_request("resources/list")
            return result.get("resources", [])
        except RuntimeError:
            # Resources may not be supported
            return []

    async def _get_capabilities(self) -> list[str]:
        """Extract capabilities from server."""
        capabilities = []

        # Check for tool support
        try:
            await self._send_request("tools/list")
            capabilities.append("tools")
        except RuntimeError:
            pass

        # Check for resource support
        try:
            await self._send_request("resources/list")
            capabilities.append("resources")
        except RuntimeError:
            pass

        # Check for prompt support
        try:
            await self._send_request("prompts/list")
            capabilities.append("prompts")
        except RuntimeError:
            pass

        return capabilities

    def _extract_server_name(self) -> str:
        """Extract server name from command or config."""
        # Try to get a meaningful name from the command
        cmd = self.config.command
        if "/" in cmd:
            cmd = cmd.split("/")[-1]
        if cmd.endswith(".js"):
            cmd = cmd[:-3]
        if cmd.startswith("@"):
            # npm package like @modelcontextprotocol/server-github
            parts = cmd.split("/")
            if len(parts) > 1:
                cmd = parts[-1]
        return cmd


async def introspect_mcp_server(config_path: Path) -> MCPAnalysis:
    """
    Convenience function to introspect an MCP server from config file.

    Args:
        config_path: Path to MCP config JSON file.

    Returns:
        MCPAnalysis with tools, resources, and capabilities.
    """
    config = MCPConfig.from_json(config_path)
    introspector = MCPIntrospector(config)
    return await introspector.introspect()


def introspect_mcp_server_sync(config_path: Path) -> MCPAnalysis:
    """Synchronous wrapper for introspect_mcp_server."""
    return asyncio.run(introspect_mcp_server(config_path))
