"""LLM provider registry. Each provider lives in its own submodule."""

from .anthropic_provider import AnthropicProvider
from .base import Provider
from .google_provider import GoogleProvider
from .openai_provider import OpenAIProvider

PROVIDERS: dict[str, type[Provider]] = {
    "anthropic": AnthropicProvider,
    "google": GoogleProvider,
    "openai": OpenAIProvider,
}

__all__ = [
    "Provider",
    "AnthropicProvider",
    "GoogleProvider",
    "OpenAIProvider",
    "PROVIDERS",
]
