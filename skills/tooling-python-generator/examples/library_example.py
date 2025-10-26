"""Python Library Example: text analyzer with type hints.

Demonstrates: dataclasses, type hints, protocol, modern Python features
"""

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class AnalysisResult:
    """Immutable analysis result."""

    length: int
    word_count: int
    analyzed_at: datetime


class TextAnalyzer:
    """Analyzes text and tracks history."""

    def __init__(self) -> None:
        self._history: list[str] = []

    def analyze(self, text: str) -> AnalysisResult:
        """Analyze text and return metrics."""
        if not text or not text.strip():
            msg = "Text cannot be empty"
            raise ValueError(msg)

        self._history.append(text)
        word_count = len(text.split())
        return AnalysisResult(len(text), word_count, datetime.now(tz=UTC))

    def get_history(self) -> tuple[str, ...]:
        """Return immutable history."""
        return tuple(self._history)
