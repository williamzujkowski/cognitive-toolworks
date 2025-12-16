"""
Source adapters for extracting information from various input formats.

This module provides adapters for:
- MCP servers (mcp.py)
- OpenAPI specifications (openapi.py)
- README files (readme.py)
- Scripts (scripts.py)
- Documentation (docs.py)
"""

from cognitive_toolworks.sources.docs import DocsParser, parse_docs
from cognitive_toolworks.sources.mcp import MCPIntrospector
from cognitive_toolworks.sources.openapi import OpenAPIIntrospector
from cognitive_toolworks.sources.readme import ReadmeParser
from cognitive_toolworks.sources.scripts import ScriptAnalyzer, analyze_script

__all__ = [
    "DocsParser",
    "MCPIntrospector",
    "OpenAPIIntrospector",
    "ReadmeParser",
    "ScriptAnalyzer",
    "analyze_script",
    "parse_docs",
]
