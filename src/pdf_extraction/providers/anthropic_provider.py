"""Anthropic Claude provider — uses native PDF document blocks."""

from __future__ import annotations

import base64
from pathlib import Path

from .base import Provider


class AnthropicProvider(Provider):
    name = "anthropic"
    env_var = "ANTHROPIC_API_KEY"
    install_cmd = "pip install anthropic"
    aliases = {
        "opus":   "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
        "haiku":  "claude-haiku-4-5-20251001",
    }

    def _make_client(self):
        self.require_sdk("anthropic")
        from anthropic import Anthropic
        return Anthropic()

    def extract(self, pdf_path: Path, prompt: str, model: str, max_tokens: int) -> str:
        pdf_b64 = base64.standard_b64encode(pdf_path.read_bytes()).decode("ascii")
        response = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        return response.content[0].text
