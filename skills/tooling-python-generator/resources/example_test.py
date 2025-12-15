"""Example pytest test file.

Demonstrates: fixtures, parametrize, type hints, assertions
"""

import pytest
from my_library import TextAnalyzer


@pytest.fixture
def analyzer() -> TextAnalyzer:
    """Create a TextAnalyzer instance."""
    return TextAnalyzer()


def test_analyze_valid_text(analyzer: TextAnalyzer) -> None:
    """Test analyzing valid text returns correct metrics."""
    result = analyzer.analyze("Hello world test")

    assert result.length == 16
    assert result.word_count == 3
    assert result.analyzed_at is not None


@pytest.mark.parametrize("text", ["", "   ", "\t\n"])
def test_analyze_empty_text_raises_error(analyzer: TextAnalyzer, text: str) -> None:
    """Test that empty text raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        analyzer.analyze(text)


def test_history_is_immutable(analyzer: TextAnalyzer) -> None:
    """Test that history returns immutable tuple."""
    analyzer.analyze("test")
    history = analyzer.get_history()

    assert isinstance(history, tuple)
    assert len(history) == 1
