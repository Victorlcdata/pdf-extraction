"""Abstract LLM provider interface."""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProviderResult:
    """Wraps the model's response together with per-request usage metrics."""

    text: str
    """The raw text output from the model (expected to be JSON)."""

    input_tokens: int = 0
    """Tokens consumed by the prompt + PDF (provider-reported)."""

    output_tokens: int = 0
    """Tokens generated in the response (provider-reported)."""

    rate_limit: dict = field(default_factory=dict)
    """Rate-limit info from response headers, when the SDK exposes it.

    Typical keys when present:
      tokens_remaining, tokens_limit  — current-minute window
      requests_remaining, requests_limit — current-minute window
    Account-level credit balance is NOT included — providers don't expose it.
    """

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class Provider(ABC):
    """Common interface for any LLM that can read a PDF and return text + usage."""

    name: str
    """Short identifier matching the --provider CLI flag (e.g. 'anthropic')."""

    aliases: dict[str, str]
    """Friendly name → underlying model id (e.g. 'sonnet' → 'claude-sonnet-4-6')."""

    env_var: str
    """Environment variable holding the API key."""

    install_cmd: str
    """Pip command to install this provider's SDK, shown in error messages."""

    def __init__(self):
        self._client = self._make_client()

    def _make_client(self):
        """Subclasses construct their SDK client here. Should call sys.exit on missing SDK."""
        raise NotImplementedError

    @abstractmethod
    def extract(self, pdf_path: Path, prompt: str, model: str, max_tokens: int) -> ProviderResult:
        """Send PDF + prompt to the model and return text + usage metrics."""

    def resolve_model(self, model: str) -> str:
        """Translate a friendly alias to the underlying model id; pass through if not aliased."""
        return self.aliases.get(model, model)

    @classmethod
    def require_sdk(cls, import_target: str) -> None:
        """Helper: subclasses call this at the top of __init__ to fail fast if SDK is missing."""
        try:
            __import__(import_target)
        except ImportError:
            sys.exit(f"ERROR: '{cls.install_cmd}' first")
