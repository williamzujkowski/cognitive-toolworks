"""Tests for data models."""

from cognitive_toolworks.models import (
    AgentsConfig,
    AnalysisReport,
    MCPAnalysis,
    MCPToolDefinition,
    Platform,
    SemanticAnalysis,
    SkillContent,
    SkillMetadata,
    SourceType,
)


class TestPlatformEnum:
    """Tests for Platform enum."""

    def test_values(self) -> None:
        """Test enum values."""
        assert Platform.ANTHROPIC.value == "anthropic"
        assert Platform.OPENAI.value == "openai"
        assert Platform.UNIVERSAL.value == "universal"

    def test_str(self) -> None:
        """Test string conversion."""
        assert str(Platform.ANTHROPIC) == "anthropic"


class TestSourceTypeEnum:
    """Tests for SourceType enum."""

    def test_values(self) -> None:
        """Test enum values."""
        assert SourceType.MCP_SERVER.value == "mcp"
        assert SourceType.OPENAPI.value == "openapi"
        assert SourceType.README.value == "readme"


class TestSkillMetadata:
    """Tests for SkillMetadata dataclass."""

    def test_basic_creation(self) -> None:
        """Test basic metadata creation."""
        meta = SkillMetadata(
            name="test-skill",
            description="A test skill for testing",
        )
        assert meta.name == "test-skill"
        assert meta.description == "A test skill for testing"
        assert meta.version == "1.0.0"

    def test_validate_anthropic_valid(self) -> None:
        """Test validation passes for valid metadata."""
        meta = SkillMetadata(
            name="my-valid-skill",
            description="A valid skill description under 200 chars",
        )
        issues = meta.validate_anthropic()
        assert len(issues) == 0

    def test_validate_anthropic_name_too_long(self) -> None:
        """Test validation catches long names."""
        meta = SkillMetadata(
            name="a" * 100,
            description="Valid description",
        )
        issues = meta.validate_anthropic()
        assert any("64 chars" in issue for issue in issues)

    def test_validate_anthropic_name_uppercase(self) -> None:
        """Test validation catches uppercase names."""
        meta = SkillMetadata(
            name="MySkill",
            description="Valid description",
        )
        issues = meta.validate_anthropic()
        assert any("lowercase" in issue for issue in issues)

    def test_validate_anthropic_description_too_long(self) -> None:
        """Test validation catches long descriptions."""
        meta = SkillMetadata(
            name="valid-name",
            description="a" * 250,
        )
        issues = meta.validate_anthropic()
        assert any("200 chars" in issue for issue in issues)

    def test_validate_anthropic_description_xml_tags(self) -> None:
        """Test validation catches XML tags in description."""
        meta = SkillMetadata(
            name="valid-name",
            description="Description with <tag>XML</tag>",
        )
        issues = meta.validate_anthropic()
        assert any("XML" in issue for issue in issues)

    def test_validate_openai_valid(self) -> None:
        """Test OpenAI validation passes for valid metadata."""
        meta = SkillMetadata(
            name="my-valid-skill",
            description="A valid skill description",
        )
        issues = meta.validate_openai()
        assert len(issues) == 0

    def test_validate_openai_longer_description(self) -> None:
        """Test OpenAI allows longer descriptions."""
        meta = SkillMetadata(
            name="valid-name",
            description="a" * 500,  # Too long for Anthropic, OK for OpenAI
        )
        issues = meta.validate_openai()
        assert len(issues) == 0

    def test_to_yaml(self) -> None:
        """Test YAML frontmatter generation."""
        meta = SkillMetadata(
            name="test-skill",
            description="Test description",
            allowed_tools=["Bash", "Read"],
        )
        yaml = meta.to_yaml()
        assert "---" in yaml
        assert "name: test-skill" in yaml
        assert "allowed-tools: Bash, Read" in yaml


class TestSkillContent:
    """Tests for SkillContent dataclass."""

    def test_basic_creation(self) -> None:
        """Test basic skill content creation."""
        meta = SkillMetadata(name="test", description="Test")
        skill = SkillContent(
            metadata=meta,
            overview="Test overview",
            when_to_use=["When testing"],
            quick_reference="Quick ref",
            instructions="Do the thing",
            examples=[],
            guidelines=["Be good"],
        )
        assert skill.metadata.name == "test"
        assert skill.overview == "Test overview"

    def test_to_markdown(self) -> None:
        """Test markdown generation."""
        meta = SkillMetadata(name="test-skill", description="Test")
        skill = SkillContent(
            metadata=meta,
            overview="Test overview",
            when_to_use=["When testing", "When developing"],
            quick_reference="```bash\ntest\n```",
            instructions="Run the test",
            examples=[{"title": "Basic Test", "code": "test cmd", "language": "bash"}],
            guidelines=["Be thorough"],
        )
        md = skill.to_markdown()

        assert "---" in md
        assert "name: test-skill" in md
        assert "# Test Skill" in md
        assert "## When to Use" in md
        assert "- When testing" in md
        assert "## Quick Reference" in md
        assert "## Instructions" in md
        assert "## Examples" in md
        assert "### Example 1: Basic Test" in md


class TestAgentsConfig:
    """Tests for AgentsConfig dataclass."""

    def test_basic_creation(self) -> None:
        """Test basic agents config creation."""
        config = AgentsConfig(
            project_overview="Test project",
            dev_environment={"setup": "npm install"},
            testing_instructions={"commands": ["npm test"]},
            pr_instructions={"checklist": ["Tests pass"]},
            coding_conventions={"style": "prettier"},
        )
        assert config.project_overview == "Test project"

    def test_to_markdown(self) -> None:
        """Test AGENTS.md generation."""
        config = AgentsConfig(
            project_overview="Test project overview",
            dev_environment={
                "setup": "npm install",
                "directories": {"src": "Source code"},
            },
            testing_instructions={"commands": ["npm test"]},
            pr_instructions={"title_format": "feat: description"},
            coding_conventions={"style": "prettier"},
        )
        md = config.to_markdown()

        assert "# AGENTS.md" in md
        assert "Test project overview" in md
        assert "npm install" in md
        assert "npm test" in md


class TestAnalysisReport:
    """Tests for AnalysisReport dataclass."""

    def test_basic_creation(self) -> None:
        """Test basic report creation."""
        report = AnalysisReport(
            total_tokens=1000,
            level1_tokens=50,
            level2_tokens=900,
            level3_tokens=50,
            token_efficiency=0.85,
            progressive_disclosure_score=0.9,
            coverage_score=0.8,
            security_issues=[],
            security_score=1.0,
            anthropic_compatible=True,
            anthropic_issues=[],
            openai_compatible=True,
            openai_issues=[],
            recommendations=[],
        )
        assert report.total_tokens == 1000
        assert report.passed is True

    def test_passed_with_security_issues(self) -> None:
        """Test passed is False with security issues."""
        report = AnalysisReport(
            total_tokens=1000,
            level1_tokens=50,
            level2_tokens=900,
            level3_tokens=50,
            token_efficiency=0.85,
            progressive_disclosure_score=0.9,
            coverage_score=0.8,
            security_issues=["Hardcoded credential found"],
            security_score=0.5,
            anthropic_compatible=True,
            anthropic_issues=[],
            openai_compatible=True,
            openai_issues=[],
            recommendations=[],
        )
        assert report.passed is False

    def test_to_dict(self) -> None:
        """Test dictionary conversion."""
        report = AnalysisReport(
            total_tokens=1000,
            level1_tokens=50,
            level2_tokens=900,
            level3_tokens=50,
            token_efficiency=0.85,
            progressive_disclosure_score=0.9,
            coverage_score=0.8,
            security_issues=[],
            security_score=1.0,
            anthropic_compatible=True,
            anthropic_issues=[],
            openai_compatible=True,
            openai_issues=[],
            recommendations=["Add more examples"],
        )
        d = report.to_dict()

        assert d["tokens"]["total"] == 1000
        assert d["scores"]["token_efficiency"] == 0.85
        assert d["compatibility"]["anthropic"]["compatible"] is True


class TestMCPToolDefinition:
    """Tests for MCPToolDefinition dataclass."""

    def test_basic_creation(self) -> None:
        """Test basic tool definition."""
        tool = MCPToolDefinition(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object"},
            required_params=["param1"],
        )
        assert tool.name == "test_tool"
        assert tool.required_params == ["param1"]

    def test_to_dict(self) -> None:
        """Test dictionary conversion."""
        tool = MCPToolDefinition(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object", "properties": {}},
        )
        d = tool.to_dict()
        assert d["name"] == "test_tool"
        assert d["input_schema"]["type"] == "object"


class TestMCPAnalysis:
    """Tests for MCPAnalysis dataclass."""

    def test_basic_creation(self) -> None:
        """Test basic analysis creation."""
        tool = MCPToolDefinition(
            name="tool1",
            description="Tool 1",
            input_schema={},
        )
        analysis = MCPAnalysis(
            server_name="test-server",
            tools=[tool],
            resources=[],
            capabilities=["tools"],
        )
        assert analysis.server_name == "test-server"
        assert len(analysis.tools) == 1


class TestSemanticAnalysis:
    """Tests for SemanticAnalysis dataclass."""

    def test_basic_creation(self) -> None:
        """Test basic semantic analysis creation."""
        analysis = SemanticAnalysis(
            purpose="Test purpose",
            tool_categories={"crud": ["create", "read"]},
            workflows=[{"name": "basic", "steps": ["step1"]}],
            error_scenarios=["Network error"],
            security_considerations=["Auth required"],
            recommended_use_cases=["Testing"],
        )
        assert analysis.purpose == "Test purpose"
        assert len(analysis.tool_categories) == 1

    def test_to_dict(self) -> None:
        """Test dictionary conversion."""
        analysis = SemanticAnalysis(
            purpose="Test",
            tool_categories={},
            workflows=[],
            error_scenarios=[],
            security_considerations=[],
            recommended_use_cases=[],
        )
        d = analysis.to_dict()
        assert d["purpose"] == "Test"
