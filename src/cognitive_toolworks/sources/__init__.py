"""
Source adapters for extracting information from various input formats.

This module provides adapters for:
- MCP servers (mcp.py)
- OpenAPI specifications (openapi.py)
- README files (readme.py)
- Scripts (scripts.py)
- Documentation (docs.py)
"""

from cognitive_toolworks.sources.mcp import MCPIntrospector

__all__ = ["MCPIntrospector"]
