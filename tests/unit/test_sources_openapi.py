"""Tests for OpenAPI introspection module."""

import json
import tempfile
from pathlib import Path

import pytest

from cognitive_toolworks.sources.openapi import (
    OpenAPIIntrospector,
    introspect_openapi,
)


class TestOpenAPIIntrospector:
    """Tests for OpenAPIIntrospector class."""

    @pytest.fixture
    def sample_spec(self) -> dict:
        """Create a minimal OpenAPI spec for testing."""
        return {
            "openapi": "3.0.0",
            "info": {"title": "Test API", "version": "1.0"},
            "paths": {
                "/users": {
                    "get": {
                        "summary": "List users",
                        "description": "Get all users",
                        "responses": {"200": {"description": "Success"}},
                    }
                }
            },
        }

    def test_from_dict(self, sample_spec: dict) -> None:
        """Test creating introspector from dictionary."""
        introspector = OpenAPIIntrospector(sample_spec)
        assert introspector.spec == sample_spec

    def test_validate_spec_missing_openapi(self) -> None:
        """Test validation fails when openapi field is missing."""
        with pytest.raises(ValueError, match="Missing 'openapi' version field"):
            OpenAPIIntrospector({"info": {"title": "Test"}})

    def test_validate_spec_unsupported_version(self) -> None:
        """Test validation fails for unsupported OpenAPI versions."""
        with pytest.raises(ValueError, match="Only OpenAPI 3.x supported"):
            OpenAPIIntrospector({"openapi": "2.0", "info": {}, "paths": {}})

    def test_validate_spec_missing_info(self) -> None:
        """Test validation fails when info section is missing."""
        with pytest.raises(ValueError, match="Missing 'info' section"):
            OpenAPIIntrospector({"openapi": "3.0.0", "paths": {}})

    def test_validate_spec_missing_paths(self) -> None:
        """Test validation fails when paths section is missing."""
        with pytest.raises(ValueError, match="Missing 'paths' section"):
            OpenAPIIntrospector({"openapi": "3.0.0", "info": {"title": "Test"}})

    def test_extract_api_name_with_version(self, sample_spec: dict) -> None:
        """Test extracting API name with version."""
        introspector = OpenAPIIntrospector(sample_spec)
        assert introspector._extract_api_name() == "Test API v1.0"

    def test_extract_api_name_without_version(self) -> None:
        """Test extracting API name without version."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "No Version API"},
            "paths": {},
        }
        introspector = OpenAPIIntrospector(spec)
        assert introspector._extract_api_name() == "No Version API"

    def test_extract_base_url(self) -> None:
        """Test extracting base URL from servers."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test"},
            "servers": [{"url": "https://api.example.com/v1"}],
            "paths": {},
        }
        introspector = OpenAPIIntrospector(spec)
        assert introspector._extract_base_url() == "https://api.example.com/v1"

    def test_extract_base_url_no_servers(self, sample_spec: dict) -> None:
        """Test extracting base URL when no servers defined."""
        introspector = OpenAPIIntrospector(sample_spec)
        assert introspector._extract_base_url() == ""

    def test_extract_endpoints(self, sample_spec: dict) -> None:
        """Test extracting endpoint definitions."""
        introspector = OpenAPIIntrospector(sample_spec)
        endpoints = introspector._extract_endpoints()

        assert len(endpoints) == 1
        endpoint = endpoints[0]
        assert endpoint.path == "/users"
        assert endpoint.method == "GET"
        assert endpoint.summary == "List users"
        assert endpoint.description == "Get all users"

    def test_extract_multiple_methods(self) -> None:
        """Test extracting multiple HTTP methods for same path."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test"},
            "paths": {
                "/users": {
                    "get": {"summary": "List users", "responses": {}},
                    "post": {"summary": "Create user", "responses": {}},
                }
            },
        }
        introspector = OpenAPIIntrospector(spec)
        endpoints = introspector._extract_endpoints()

        assert len(endpoints) == 2
        methods = {e.method for e in endpoints}
        assert methods == {"GET", "POST"}

    def test_extract_parameters(self) -> None:
        """Test extracting endpoint parameters."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test"},
            "paths": {
                "/users": {
                    "get": {
                        "summary": "List users",
                        "parameters": [
                            {
                                "name": "limit",
                                "in": "query",
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {},
                    }
                }
            },
        }
        introspector = OpenAPIIntrospector(spec)
        endpoints = introspector._extract_endpoints()

        assert len(endpoints[0].parameters) == 1
        assert endpoints[0].parameters[0]["name"] == "limit"
        assert endpoints[0].parameters[0]["in"] == "query"

    def test_extract_request_body(self) -> None:
        """Test extracting request body definition."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test"},
            "paths": {
                "/users": {
                    "post": {
                        "summary": "Create user",
                        "requestBody": {
                            "required": True,
                            "content": {"application/json": {"schema": {"type": "object"}}},
                        },
                        "responses": {},
                    }
                }
            },
        }
        introspector = OpenAPIIntrospector(spec)
        endpoints = introspector._extract_endpoints()

        assert endpoints[0].request_body is not None
        assert endpoints[0].request_body["required"] is True

    def test_extract_schemas(self) -> None:
        """Test extracting component schemas."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test"},
            "paths": {},
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                }
            },
        }
        introspector = OpenAPIIntrospector(spec)
        schemas = introspector._extract_schemas()

        assert "User" in schemas
        assert schemas["User"]["type"] == "object"

    def test_extract_schemas_no_components(self, sample_spec: dict) -> None:
        """Test extracting schemas when components section is missing."""
        introspector = OpenAPIIntrospector(sample_spec)
        schemas = introspector._extract_schemas()
        assert schemas == {}

    def test_extract_authentication(self) -> None:
        """Test extracting authentication schemes."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test"},
            "paths": {},
            "components": {
                "securitySchemes": {
                    "ApiKeyAuth": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "X-API-Key",
                    }
                }
            },
            "security": [{"ApiKeyAuth": []}],
        }
        introspector = OpenAPIIntrospector(spec)
        auth = introspector._extract_authentication()

        assert "ApiKeyAuth" in auth["schemes"]
        assert auth["schemes"]["ApiKeyAuth"]["type"] == "apiKey"
        assert len(auth["global_requirements"]) == 1

    def test_extract_capabilities(self) -> None:
        """Test extracting API capabilities."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test"},
            "paths": {
                "/users": {
                    "get": {"summary": "List", "responses": {}},
                    "post": {"summary": "Create", "responses": {}},
                    "delete": {"summary": "Delete", "responses": {}},
                }
            },
            "components": {
                "schemas": {"User": {"type": "object"}},
                "securitySchemes": {"ApiKey": {"type": "apiKey"}},
            },
        }
        introspector = OpenAPIIntrospector(spec)
        capabilities = introspector._extract_capabilities()

        assert "read" in capabilities  # GET
        assert "write" in capabilities  # POST
        assert "delete" in capabilities  # DELETE
        assert "schemas" in capabilities
        assert "authentication" in capabilities

    def test_introspect_full_analysis(self, sample_spec: dict) -> None:
        """Test full introspection returns OpenAPIAnalysis."""
        introspector = OpenAPIIntrospector(sample_spec)
        analysis = introspector.introspect()

        assert analysis.api_name == "Test API v1.0"
        assert len(analysis.endpoints) == 1
        assert isinstance(analysis.schemas, dict)
        assert isinstance(analysis.authentication, dict)
        assert isinstance(analysis.capabilities, list)

    def test_from_file_yaml(self) -> None:
        """Test loading from YAML file."""
        spec_path = Path(__file__).parent.parent / "fixtures" / "openapi" / "sample_api.yaml"
        introspector = OpenAPIIntrospector.from_file(spec_path)

        assert introspector.spec["info"]["title"] == "Sample API"
        analysis = introspector.introspect()
        assert len(analysis.endpoints) > 0

    def test_from_file_json(self) -> None:
        """Test loading from JSON file."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "JSON Test"},
            "paths": {},
        }

        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump(spec, f)
            f.flush()
            path = Path(f.name)

        try:
            introspector = OpenAPIIntrospector.from_file(path)
            assert introspector.spec["info"]["title"] == "JSON Test"
        finally:
            path.unlink()

    def test_from_file_no_extension_json(self) -> None:
        """Test loading from file with no extension (JSON content)."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "No Ext"},
            "paths": {},
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(spec, f)
            f.flush()
            path = Path(f.name)

        try:
            introspector = OpenAPIIntrospector.from_file(path)
            assert introspector.spec["info"]["title"] == "No Ext"
        finally:
            path.unlink()

    def test_from_url_raises_not_implemented(self) -> None:
        """Test that URL loading raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            OpenAPIIntrospector.from_url("https://example.com/openapi.json")

    def test_from_url_invalid_url(self) -> None:
        """Test that invalid URLs raise ValueError."""
        with pytest.raises(ValueError, match="Invalid URL"):
            OpenAPIIntrospector.from_url("not-a-url")


class TestIntrospectOpenAPI:
    """Tests for introspect_openapi convenience function."""

    def test_introspect_from_file(self) -> None:
        """Test introspecting from file path."""
        spec_path = Path(__file__).parent.parent / "fixtures" / "openapi" / "sample_api.yaml"
        analysis = introspect_openapi(str(spec_path))

        assert analysis.api_name == "Sample API v1.0"
        assert analysis.base_url == "https://api.example.com/v1"
        assert (
            len(analysis.endpoints) == 4
        )  # GET /users, POST /users, GET /users/{id}, DELETE /users/{id}

        # Check endpoints
        paths = {e.path for e in analysis.endpoints}
        assert "/users" in paths
        assert "/users/{id}" in paths

        # Check methods
        methods = {(e.path, e.method) for e in analysis.endpoints}
        assert ("/users", "GET") in methods
        assert ("/users", "POST") in methods
        assert ("/users/{id}", "GET") in methods
        assert ("/users/{id}", "DELETE") in methods

        # Check schemas
        assert "User" in analysis.schemas
        assert analysis.schemas["User"]["type"] == "object"

        # Check authentication
        assert "ApiKeyAuth" in analysis.authentication["schemes"]
        assert len(analysis.authentication["global_requirements"]) == 1

        # Check capabilities
        assert "read" in analysis.capabilities
        assert "write" in analysis.capabilities
        assert "delete" in analysis.capabilities
        assert "schemas" in analysis.capabilities
        assert "authentication" in analysis.capabilities

    def test_introspect_url_not_implemented(self) -> None:
        """Test that URL introspection raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            introspect_openapi("https://example.com/openapi.json")


class TestEndpointDefinition:
    """Tests for EndpointDefinition model."""

    def test_to_dict(self) -> None:
        """Test converting endpoint to dictionary."""
        spec_path = Path(__file__).parent.parent / "fixtures" / "openapi" / "sample_api.yaml"
        analysis = introspect_openapi(str(spec_path))
        endpoint = analysis.endpoints[0]

        data = endpoint.to_dict()
        assert "path" in data
        assert "method" in data
        assert "summary" in data
        assert "description" in data
        assert "parameters" in data
        assert "request_body" in data
        assert "responses" in data


class TestOpenAPIAnalysis:
    """Tests for OpenAPIAnalysis model."""

    def test_to_dict(self) -> None:
        """Test converting analysis to dictionary."""
        spec_path = Path(__file__).parent.parent / "fixtures" / "openapi" / "sample_api.yaml"
        analysis = introspect_openapi(str(spec_path))

        data = analysis.to_dict()
        assert "api_name" in data
        assert "base_url" in data
        assert "endpoints" in data
        assert "schemas" in data
        assert "authentication" in data
        assert "capabilities" in data
        assert isinstance(data["endpoints"], list)
        assert len(data["endpoints"]) == 4
