"""
Multi-provider LLM client.

Supports Anthropic Claude API with structured output parsing,
retry logic, and rate limiting.
"""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import httpx


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"


@dataclass
class LLMConfig:
    """Configuration for LLM client."""

    provider: LLMProvider = LLMProvider.ANTHROPIC
    api_key: str | None = None
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: float = 120.0
    max_retries: int = 3
    retry_delay: float = 1.0

    def __post_init__(self) -> None:
        # Auto-detect API key from environment
        if not self.api_key:
            if self.provider == LLMProvider.ANTHROPIC:
                self.api_key = os.environ.get("ANTHROPIC_API_KEY")
            elif self.provider == LLMProvider.OPENAI:
                self.api_key = os.environ.get("OPENAI_API_KEY")


@dataclass
class LLMResponse:
    """Response from LLM API."""

    content: str
    model: str
    tokens_used: int
    stop_reason: str
    raw_response: dict[str, Any] = field(default_factory=dict)

    @property
    def as_json(self) -> dict[str, Any]:
        """Parse response content as JSON."""
        # Try to extract JSON from markdown code blocks
        content = self.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return json.loads(content.strip())


class LLMClient:
    """
    Multi-provider LLM client with retry logic and structured output.

    Example:
        client = LLMClient()
        response = await client.generate("Analyze this code...")
        data = response.as_json
    """

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig()
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> LLMClient:
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        json_output: bool = False,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Generate a response from the LLM.

        Args:
            prompt: The user prompt.
            system: Optional system prompt.
            json_output: If True, request JSON-formatted response.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            LLMResponse with content and metadata.
        """
        if self.config.provider == LLMProvider.ANTHROPIC:
            return await self._generate_anthropic(prompt, system, json_output, **kwargs)
        elif self.config.provider == LLMProvider.OPENAI:
            return await self._generate_openai(prompt, system, json_output, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    async def _generate_anthropic(
        self,
        prompt: str,
        system: str | None,
        _json_output: bool,
        **kwargs: Any,
    ) -> LLMResponse:
        """Generate using Anthropic Claude API."""
        if not self.config.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)

        headers = {
            "x-api-key": self.config.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        messages = [{"role": "user", "content": prompt}]

        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.config.model),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "messages": messages,
        }

        if system:
            payload["system"] = system

        # Retry logic
        last_error: Exception | None = None
        for attempt in range(self.config.max_retries):
            try:
                response = await self._client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                )

                if response.status_code == 429:
                    # Rate limited
                    retry_after = float(
                        response.headers.get("retry-after", self.config.retry_delay * 2)
                    )
                    await asyncio.sleep(retry_after)
                    continue

                response.raise_for_status()
                data = response.json()

                content = ""
                for block in data.get("content", []):
                    if block.get("type") == "text":
                        content += block.get("text", "")

                return LLMResponse(
                    content=content,
                    model=data.get("model", self.config.model),
                    tokens_used=data.get("usage", {}).get("output_tokens", 0),
                    stop_reason=data.get("stop_reason", ""),
                    raw_response=data,
                )

            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code >= 500:
                    await asyncio.sleep(self.config.retry_delay * (attempt + 1))
                    continue
                raise

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                last_error = e
                await asyncio.sleep(self.config.retry_delay * (attempt + 1))
                continue

        raise RuntimeError(f"Failed after {self.config.max_retries} retries: {last_error}")

    async def _generate_openai(
        self,
        prompt: str,
        system: str | None,
        _json_output: bool,
        **kwargs: Any,
    ) -> LLMResponse:
        """Generate using OpenAI API."""
        if not self.config.api_key:
            raise ValueError("OPENAI_API_KEY not set")

        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": kwargs.get("model", "gpt-4"),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "messages": messages,
        }

        if _json_output:
            payload["response_format"] = {"type": "json_object"}

        response = await self._client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]

        return LLMResponse(
            content=content,
            model=data.get("model", "gpt-4"),
            tokens_used=data.get("usage", {}).get("completion_tokens", 0),
            stop_reason=data["choices"][0].get("finish_reason", ""),
            raw_response=data,
        )

    async def analyze(
        self,
        content: str,
        analysis_type: str = "semantic",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Analyze content and return structured result.

        Args:
            content: The content to analyze.
            analysis_type: Type of analysis (semantic, security, etc.)
            **kwargs: Additional parameters.

        Returns:
            Structured analysis result.
        """
        from cognitive_toolworks.llm.prompts import get_prompt

        system = get_prompt(f"{analysis_type}_analysis_system")
        prompt = get_prompt(f"{analysis_type}_analysis").format(content=content)

        response = await self.generate(prompt, system=system, json_output=True, **kwargs)
        return response.as_json


def get_client(config: LLMConfig | None = None) -> LLMClient:
    """Get a configured LLM client."""
    return LLMClient(config)
