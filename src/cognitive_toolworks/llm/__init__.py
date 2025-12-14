"""
LLM integration for Cognitive Toolworks.

Provides multi-provider LLM client and prompt templates for:
- Semantic analysis
- Skill generation
- Example synthesis
- Optimization
"""

from cognitive_toolworks.llm.client import LLMClient
from cognitive_toolworks.llm.prompts import PromptTemplate, get_prompt

__all__ = ["LLMClient", "PromptTemplate", "get_prompt"]
