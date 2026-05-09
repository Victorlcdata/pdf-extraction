"""Abstract LLM provider interface."""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from pathlib import Path


class Provider(ABC):
    """Common interface for any LLM that can read a PDF and return text."""

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
    def extract(self, pdf_path: Path, prompt: str, model: str, max_tokens: int) -> str:
        """Send PDF + prompt to the model and return the raw text response."""

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
