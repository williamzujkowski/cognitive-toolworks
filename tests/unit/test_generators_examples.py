"""Tests for example generator module."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from cognitive_toolworks.generators.examples import (
    Example,
    ExampleComplexity,
    ExampleGenerationConfig,
    ExampleGenerator,
    ExampleSet,
    create_example,
)
from cognitive_toolworks.models import SemanticAnalysis, SkillContent, SkillMetadata


class TestExample:
    """Tests for Example dataclass."""

    def test_create_example_basic(self) -> None:
        """Test creating a basic example."""
        example = Example(
            title="Basic Example",
            description="A simple test",
            code="echo 'Hello World'",
            language="bash",
        )
        assert example.title == "Basic Example"
        assert example.language == "bash"
        assert example.complexity == ExampleComplexity.SIMPLE

    def test_example_to_dict(self) -> None:
        """Test converting example to dictionary."""
        example = Example(
            title="Test",
            description="Desc",
            code="code",
            language="python",
            user_intent="Run test",
            expected_output="Success",
            complexity=ExampleComplexity.INTERMEDIATE,
            tags=["test", "example"],
        )
        data = example.to_dict()

        assert data["title"] == "Test"
        assert data["complexity"] == "intermediate"
        assert "test" in data["tags"]

    def test_example_from_dict(self) -> None:
        """Test creating example from dictionary."""
        data = {
            "title": "From Dict",
            "description": "Created from dict",
            "code": "print('hello')",
            "language": "python",
            "complexity": "advanced",
        }
        example = Example.from_dict(data)

        assert example.title == "From Dict"
        assert example.complexity == ExampleComplexity.ADVANCED
        assert example.language == "python"

    def test_example_from_dict_defaults(self) -> None:
        """Test example from dict uses defaults."""
        data = {"code": "test"}
        example = Example.from_dict(data)

        assert example.title == "Untitled Example"
        assert example.language == "bash"
        assert example.complexity == ExampleComplexity.SIMPLE

    def test_example_is_valid(self) -> None:
        """Test example validation."""
        valid = Example(title="Test", description="", code="echo test")
        assert valid.is_valid() is True

        invalid_no_title = Example(title="", description="", code="echo test")
        assert invalid_no_title.is_valid() is False

        invalid_no_code = Example(title="Test", description="", code="")
        assert invalid_no_code.is_valid() is False

    def test_example_token_estimate(self) -> None:
        """Test token estimation."""
        example = Example(
            title="Test Title",  # 10 chars
            description="A description",  # 13 chars
            code="echo 'hello'",  # 12 chars
            user_intent="Run command",  # 11 chars
            expected_output="hello",  # 5 chars
        )
        # Total: 51 chars, estimate = 51 // 4 = 12
        assert example.token_estimate() == 12


class TestExampleComplexity:
    """Tests for ExampleComplexity enum."""

    def test_complexity_values(self) -> None:
        """Test complexity enum values."""
        assert ExampleComplexity.SIMPLE.value == "simple"
        assert ExampleComplexity.INTERMEDIATE.value == "intermediate"
        assert ExampleComplexity.ADVANCED.value == "advanced"
        assert ExampleComplexity.EDGE_CASE.value == "edge_case"


class TestExampleSet:
    """Tests for ExampleSet dataclass."""

    def test_create_empty_set(self) -> None:
        """Test creating empty example set."""
        example_set = ExampleSet()
        assert len(example_set.examples) == 0
        assert example_set.total_tokens == 0

    def test_add_example(self) -> None:
        """Test adding example to set."""
        example_set = ExampleSet(skill_name="test-skill")
        example = Example(title="Test", description="", code="test")

        example_set.add_example(example)

        assert len(example_set.examples) == 1
        assert example_set.total_tokens > 0

    def test_filter_by_complexity(self) -> None:
        """Test filtering examples by complexity."""
        example_set = ExampleSet()
        example_set.add_example(
            Example(
                title="Simple",
                description="",
                code="simple",
                complexity=ExampleComplexity.SIMPLE,
            )
        )
        example_set.add_example(
            Example(
                title="Advanced",
                description="",
                code="advanced",
                complexity=ExampleComplexity.ADVANCED,
            )
        )
        example_set.add_example(
            Example(
                title="Simple2",
                description="",
                code="simple2",
                complexity=ExampleComplexity.SIMPLE,
            )
        )

        simple = example_set.filter_by_complexity(ExampleComplexity.SIMPLE)
        assert len(simple) == 2

        advanced = example_set.filter_by_complexity(ExampleComplexity.ADVANCED)
        assert len(advanced) == 1

    def test_validate_all(self) -> None:
        """Test validating all examples in set."""
        example_set = ExampleSet()
        example_set.add_example(
            Example(
                title="Valid",
                description="Has description",
                code="echo 'valid code here'",
            )
        )
        example_set.add_example(Example(title="", description="", code=""))  # Invalid

        is_valid, issues = example_set.validate_all()

        assert is_valid is False
        assert len(issues) > 0

    def test_to_dict(self) -> None:
        """Test converting set to dictionary."""
        example_set = ExampleSet(skill_name="test")
        example_set.add_example(Example(title="Ex1", description="", code="code"))

        data = example_set.to_dict()

        assert data["skill_name"] == "test"
        assert len(data["examples"]) == 1


class TestExampleGenerationConfig:
    """Tests for ExampleGenerationConfig."""

    def test_default_config(self) -> None:
        """Test default configuration values."""
        config = ExampleGenerationConfig()

        assert config.num_examples == 3
        assert config.include_simple is True
        assert config.include_intermediate is True
        assert config.include_advanced is False
        assert config.include_edge_case is True
        assert config.max_tokens_per_example == 200
        assert config.default_language == "bash"

    def test_custom_config(self) -> None:
        """Test custom configuration."""
        config = ExampleGenerationConfig(
            num_examples=5,
            include_advanced=True,
            default_language="python",
        )

        assert config.num_examples == 5
        assert config.include_advanced is True
        assert config.default_language == "python"


class TestExampleGenerator:
    """Tests for ExampleGenerator class."""

    def test_init_default(self) -> None:
        """Test default initialization."""
        generator = ExampleGenerator()
        assert generator.config.num_examples == 3

    def test_init_custom_config(self) -> None:
        """Test initialization with custom config."""
        config = ExampleGenerationConfig(num_examples=5)
        generator = ExampleGenerator(config=config)
        assert generator.config.num_examples == 5

    def test_validate_examples_list(self) -> None:
        """Test validating a list of examples."""
        generator = ExampleGenerator()

        valid_examples = [
            Example(title="Ex1", description="Desc", code="echo 'valid code'"),
            Example(title="Ex2", description="Desc", code="echo 'also valid'"),
        ]
        is_valid, issues = generator.validate_examples(valid_examples)
        assert is_valid is True
        assert len(issues) == 0

        invalid_examples = [
            Example(title="", description="", code=""),
        ]
        is_valid, issues = generator.validate_examples(invalid_examples)
        assert is_valid is False
        assert len(issues) > 0

    def test_format_for_skill_md(self) -> None:
        """Test formatting examples for SKILL.md."""
        generator = ExampleGenerator()

        examples = [
            Example(
                title="Example One",
                description="First example",
                code="echo 'hello'",
                language="bash",
                expected_output="hello",
            ),
        ]

        markdown = generator.format_for_skill_md(examples)

        assert "## Examples" in markdown
        assert "### Example One" in markdown
        assert "```bash" in markdown
        assert "echo 'hello'" in markdown
        assert "**Expected output:**" in markdown

    def test_format_for_skill_md_empty(self) -> None:
        """Test formatting empty examples."""
        generator = ExampleGenerator()
        markdown = generator.format_for_skill_md([])
        assert markdown == ""

    def test_format_for_skill_md_example_set(self) -> None:
        """Test formatting ExampleSet."""
        generator = ExampleGenerator()

        example_set = ExampleSet()
        example_set.add_example(
            Example(
                title="Test",
                description="Test desc",
                code="test code",
                language="python",
            )
        )

        markdown = generator.format_for_skill_md(example_set)

        assert "## Examples" in markdown
        assert "### Test" in markdown
        assert "```python" in markdown

    @pytest.mark.asyncio
    async def test_generate_from_semantic(self) -> None:
        """Test generating examples from semantic analysis."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.as_json = [
            {
                "title": "Generated Example",
                "description": "LLM generated this",
                "code": "echo 'generated'",
                "language": "bash",
            }
        ]
        mock_llm.generate = AsyncMock(return_value=mock_response)
        mock_llm.__aenter__ = AsyncMock(return_value=mock_llm)
        mock_llm.__aexit__ = AsyncMock(return_value=None)

        generator = ExampleGenerator(llm_client=mock_llm)

        semantic = SemanticAnalysis(
            purpose="Test purpose",
            tool_categories={"cat1": ["tool1"]},
            workflows=[{"name": "workflow1", "steps": ["step1"]}],
            error_scenarios=[],
            security_considerations=[],
            recommended_use_cases=[],
        )

        result = await generator.generate_from_semantic(semantic)

        assert isinstance(result, ExampleSet)
        assert len(result.examples) == 1
        assert result.examples[0].title == "Generated Example"

    @pytest.mark.asyncio
    async def test_generate_from_skill(self) -> None:
        """Test generating examples from skill content."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.as_json = [
            {
                "title": "Skill Example",
                "description": "For existing skill",
                "code": "skill-cmd --test",
                "language": "bash",
                "complexity": "intermediate",
            }
        ]
        mock_llm.generate = AsyncMock(return_value=mock_response)
        mock_llm.__aenter__ = AsyncMock(return_value=mock_llm)
        mock_llm.__aexit__ = AsyncMock(return_value=None)

        generator = ExampleGenerator(llm_client=mock_llm)

        skill = SkillContent(
            metadata=SkillMetadata(name="test-skill", description="Test skill"),
            overview="A test skill",
            when_to_use=["When testing"],
            quick_reference="",
            instructions="Run tests",
            examples=[],
            guidelines=[],
        )

        result = await generator.generate_from_skill(skill)

        assert isinstance(result, ExampleSet)
        assert result.skill_name == "test-skill"
        assert len(result.examples) == 1

    @pytest.mark.asyncio
    async def test_enhance_example(self) -> None:
        """Test enhancing an existing example."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.as_json = {
            "title": "Enhanced Example",
            "description": "Now with detailed explanation",
            "code": "echo 'hello'",
            "language": "bash",
            "expected_output": "hello",
        }
        mock_llm.generate = AsyncMock(return_value=mock_response)
        mock_llm.__aenter__ = AsyncMock(return_value=mock_llm)
        mock_llm.__aexit__ = AsyncMock(return_value=None)

        generator = ExampleGenerator(llm_client=mock_llm)

        original = Example(
            title="Basic",
            description="Short",
            code="echo 'hello'",
            language="bash",
        )

        enhanced = await generator.enhance_example(original)

        assert enhanced.expected_output == "hello"
        assert len(enhanced.description) > len(original.description)

    @pytest.mark.asyncio
    async def test_enhance_example_no_changes_needed(self) -> None:
        """Test that enhance returns unchanged if no enhancements needed."""
        generator = ExampleGenerator()

        complete_example = Example(
            title="Complete",
            description="This is a sufficiently detailed description for the example",
            code="echo 'hello'",
            language="bash",
            expected_output="hello",
        )

        # When no enhancements needed, should return same object
        result = await generator.enhance_example(
            complete_example,
            add_output=True,  # Already has output
            add_explanation=True,  # Description is long enough
        )

        assert result is complete_example


class TestCreateExampleHelper:
    """Tests for create_example helper function."""

    def test_create_example_minimal(self) -> None:
        """Test creating example with minimal args."""
        example = create_example("Test", "echo test")

        assert example.title == "Test"
        assert example.code == "echo test"
        assert example.language == "bash"
        assert example.description == ""

    def test_create_example_full(self) -> None:
        """Test creating example with all args."""
        example = create_example(
            title="Full Example",
            code="python script.py",
            description="Runs a Python script",
            language="bash",
            user_intent="Execute Python code",
            expected_output="Script output",
            complexity=ExampleComplexity.INTERMEDIATE,
            tags=["python", "script"],
        )

        assert example.title == "Full Example"
        assert example.complexity == ExampleComplexity.INTERMEDIATE
        assert "python" in example.tags


class TestExampleGeneratorParseExamples:
    """Tests for _parse_examples method."""

    def test_parse_list_of_dicts(self) -> None:
        """Test parsing list of dictionaries."""
        generator = ExampleGenerator()

        data = [
            {"title": "Ex1", "code": "code1"},
            {"title": "Ex2", "code": "code2"},
        ]

        examples = generator._parse_examples(data)

        assert len(examples) == 2
        assert examples[0].title == "Ex1"
        assert examples[1].title == "Ex2"

    def test_parse_single_dict(self) -> None:
        """Test parsing single dictionary."""
        generator = ExampleGenerator()

        data = {"title": "Single", "code": "single code"}

        examples = generator._parse_examples(data)

        assert len(examples) == 1
        assert examples[0].title == "Single"

    def test_parse_assigns_complexity(self) -> None:
        """Test that complexity is assigned based on index."""
        generator = ExampleGenerator()

        data = [
            {"title": "Ex1", "code": "c1"},
            {"title": "Ex2", "code": "c2"},
            {"title": "Ex3", "code": "c3"},
            {"title": "Ex4", "code": "c4"},
        ]

        examples = generator._parse_examples(data)

        assert examples[0].complexity == ExampleComplexity.SIMPLE
        assert examples[1].complexity == ExampleComplexity.INTERMEDIATE
        assert examples[2].complexity == ExampleComplexity.ADVANCED
        assert examples[3].complexity == ExampleComplexity.EDGE_CASE
