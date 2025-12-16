"""
OpenAPI Specification Introspection Module.

Extracts endpoint definitions, schemas, and capabilities from OpenAPI specs.
Supports OpenAPI 3.0 and 3.1 in both JSON and YAML formats.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
import yaml

from cognitive_toolworks.models import EndpointDefinition, OpenAPIAnalysis


class OpenAPIIntrospector:
    """
    Introspects OpenAPI specifications to extract API definitions.

    Parses OpenAPI 3.0/3.1 specifications from files or URLs to discover
    endpoints, schemas, authentication methods, and capabilities.
    """

    def __init__(self, spec: dict[str, Any]) -> None:
        """
        Initialize with a parsed OpenAPI specification.

        Args:
            spec: Parsed OpenAPI specification dictionary.
        """
        self.spec = spec
        self._validate_spec()

    @classmethod
    def from_file(cls, path: Path) -> OpenAPIIntrospector:
        """
        Load OpenAPI spec from a file.

        Args:
            path: Path to JSON or YAML file.

        Returns:
            OpenAPIIntrospector instance.

        Raises:
            ValueError: If file format is unsupported or invalid.
        """
        content = path.read_text()

        # Try to parse based on file extension
        if path.suffix in (".yaml", ".yml"):
            spec = yaml.safe_load(content)
        elif path.suffix == ".json":
            spec = json.loads(content)
        else:
            # Try JSON first, then YAML
            try:
                spec = json.loads(content)
            except json.JSONDecodeError:
                spec = yaml.safe_load(content)

        return cls(spec)

    @classmethod
    def from_url(
        cls,
        url: str,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> OpenAPIIntrospector:
        """
        Load OpenAPI spec from a URL.

        Args:
            url: URL to OpenAPI specification.
            headers: Optional authentication or custom headers.
            timeout: Request timeout in seconds (default: 30.0).

        Returns:
            OpenAPIIntrospector instance.

        Raises:
            ValueError: If URL is invalid, cannot be fetched, or content is invalid.
        """
        # Parse URL to validate
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")

        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"URL must use http or https scheme: {url}")

        # Fetch the spec from the URL
        try:
            response = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
            response.raise_for_status()
        except httpx.TimeoutException as e:
            raise ValueError(f"Request timeout after {timeout}s: {url}") from e
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP {e.response.status_code} error fetching {url}") from e
        except httpx.RequestError as e:
            raise ValueError(f"Network error fetching {url}: {e}") from e

        content = response.text
        content_type = response.headers.get("content-type", "").lower()

        # Parse based on Content-Type or attempt both formats
        spec = None

        if "application/json" in content_type or "json" in content_type:
            try:
                spec = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in response from {url}") from e
        elif "yaml" in content_type or "yml" in content_type:
            try:
                spec = yaml.safe_load(content)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML in response from {url}") from e
        else:
            # Try JSON first, then YAML
            try:
                spec = json.loads(content)
            except json.JSONDecodeError:
                try:
                    spec = yaml.safe_load(content)
                except yaml.YAMLError as e:
                    raise ValueError(f"Could not parse response from {url} as JSON or YAML") from e

        if spec is None:
            raise ValueError(f"Failed to parse OpenAPI spec from {url}")

        return cls(spec)

    def _validate_spec(self) -> None:
        """
        Validate that spec is a valid OpenAPI specification.

        Raises:
            ValueError: If spec is invalid.
        """
        if not isinstance(self.spec, dict):
            raise ValueError("OpenAPI spec must be a dictionary")

        if "openapi" not in self.spec:
            raise ValueError("Missing 'openapi' version field")

        version = self.spec["openapi"]
        if not version.startswith("3."):
            raise ValueError(f"Only OpenAPI 3.x supported, got {version}")

        if "info" not in self.spec:
            raise ValueError("Missing 'info' section")

        if "paths" not in self.spec:
            raise ValueError("Missing 'paths' section")

    def introspect(self) -> OpenAPIAnalysis:
        """
        Perform full introspection of the OpenAPI specification.

        Returns:
            OpenAPIAnalysis containing endpoints, schemas, and capabilities.
        """
        return OpenAPIAnalysis(
            api_name=self._extract_api_name(),
            base_url=self._extract_base_url(),
            endpoints=self._extract_endpoints(),
            schemas=self._extract_schemas(),
            authentication=self._extract_authentication(),
            capabilities=self._extract_capabilities(),
        )

    def _extract_api_name(self) -> str:
        """Extract API name from spec info."""
        info = self.spec.get("info", {})
        title = str(info.get("title", "Unknown API"))
        version = str(info.get("version", ""))
        if version:
            return f"{title} v{version}"
        return title

    def _extract_base_url(self) -> str:
        """
        Extract base URL from servers section.

        Returns first server URL or empty string if none defined.
        """
        servers = self.spec.get("servers", [])
        if servers and len(servers) > 0:
            return str(servers[0].get("url", ""))
        return ""

    def _extract_endpoints(self) -> list[EndpointDefinition]:
        """Extract all endpoint definitions from paths."""
        endpoints: list[EndpointDefinition] = []
        paths = self.spec.get("paths", {})

        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue

            # Process each HTTP method
            for method in ["get", "post", "put", "delete", "patch", "options", "head"]:
                if method in path_item:
                    operation = path_item[method]
                    endpoint = self._parse_operation(path, method.upper(), operation)
                    endpoints.append(endpoint)

        return endpoints

    def _parse_operation(
        self, path: str, method: str, operation: dict[str, Any]
    ) -> EndpointDefinition:
        """
        Parse a single operation into an EndpointDefinition.

        Args:
            path: API path (e.g., /users/{id}).
            method: HTTP method (GET, POST, etc.).
            operation: Operation object from spec.

        Returns:
            EndpointDefinition instance.
        """
        return EndpointDefinition(
            path=path,
            method=method,
            summary=operation.get("summary", ""),
            description=operation.get("description", ""),
            parameters=operation.get("parameters", []),
            request_body=operation.get("requestBody"),
            responses=operation.get("responses", {}),
        )

    def _extract_schemas(self) -> dict[str, Any]:
        """
        Extract component schemas from spec.

        Returns:
            Dictionary of schema definitions.
        """
        components = self.spec.get("components", {})
        schemas = components.get("schemas", {})
        return dict(schemas) if schemas else {}

    def _extract_authentication(self) -> dict[str, Any]:
        """
        Extract authentication/security schemes.

        Returns:
            Dictionary of security schemes.
        """
        components = self.spec.get("components", {})
        security_schemes = components.get("securitySchemes", {})

        # Also check for global security requirements
        global_security = self.spec.get("security", [])

        return {
            "schemes": security_schemes,
            "global_requirements": global_security,
        }

    def _extract_capabilities(self) -> list[str]:
        """
        Extract API capabilities based on available features.

        Returns:
            List of capability strings.
        """
        capabilities = []

        # Check for different HTTP methods
        paths = self.spec.get("paths", {})
        methods_used = set()

        for path_item in paths.values():
            if not isinstance(path_item, dict):
                continue
            for method in ["get", "post", "put", "delete", "patch"]:
                if method in path_item:
                    methods_used.add(method.upper())

        if "GET" in methods_used:
            capabilities.append("read")
        if any(m in methods_used for m in ["POST", "PUT", "PATCH"]):
            capabilities.append("write")
        if "DELETE" in methods_used:
            capabilities.append("delete")

        # Check for webhooks (OpenAPI 3.1)
        if "webhooks" in self.spec:
            capabilities.append("webhooks")

        # Check for authentication
        auth = self._extract_authentication()
        if auth.get("schemes") or auth.get("global_requirements"):
            capabilities.append("authentication")

        # Check for schemas
        if self._extract_schemas():
            capabilities.append("schemas")

        return capabilities


def introspect_openapi(path_or_url: str) -> OpenAPIAnalysis:
    """
    Convenience function to introspect an OpenAPI specification.

    Args:
        path_or_url: File path or URL to OpenAPI spec.

    Returns:
        OpenAPIAnalysis with endpoints, schemas, and capabilities.

    Raises:
        ValueError: If path/URL is invalid or spec cannot be parsed.
    """
    # Determine if it's a URL or file path
    if path_or_url.startswith(("http://", "https://")):
        introspector = OpenAPIIntrospector.from_url(path_or_url)
    else:
        introspector = OpenAPIIntrospector.from_file(Path(path_or_url))

    return introspector.introspect()
