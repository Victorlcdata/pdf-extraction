"""Anthropic Claude provider — uses native PDF document blocks."""

from __future__ import annotations

import base64
from pathlib import Path

from .base import Provider, ProviderResult


class AnthropicProvider(Provider):
    name = "anthropic"
    env_var = "ANTHROPIC_API_KEY"
    install_cmd = "pip install anthropic"
    aliases = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
        "haiku": "claude-haiku-4-5-20251001",
    }

    def _make_client(self):
        self.require_sdk("anthropic")
        from anthropic import Anthropic

        return Anthropic()

    def extract(self, pdf_path: Path, prompt: str, model: str, max_tokens: int) -> ProviderResult:
        pdf_b64 = base64.standard_b64encode(pdf_path.read_bytes()).decode("ascii")

        # `with_raw_response` lets us inspect rate-limit headers alongside the parsed body.
        raw = self._client.messages.with_raw_response.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
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
                }
            ],
        )
        response = raw.parse()

        rate_limit = _extract_rate_limit(raw.headers)

        return ProviderResult(
            text=response.content[0].text,
            input_tokens=getattr(response.usage, "input_tokens", 0) or 0,
            output_tokens=getattr(response.usage, "output_tokens", 0) or 0,
            rate_limit=rate_limit,
        )


def _extract_rate_limit(headers) -> dict:
    """Pull the per-minute rate-limit info Anthropic returns on every response."""
    out = {}
    pairs = [
        ("anthropic-ratelimit-tokens-remaining", "tokens_remaining"),
        ("anthropic-ratelimit-tokens-limit", "tokens_limit"),
        ("anthropic-ratelimit-requests-remaining", "requests_remaining"),
        ("anthropic-ratelimit-requests-limit", "requests_limit"),
        ("anthropic-ratelimit-tokens-reset", "tokens_reset_at"),
    ]
    for header, key in pairs:
        value = headers.get(header)
        if value is None:
            continue
        if key.endswith("_at"):
            out[key] = value
        else:
            try:
                out[key] = int(value)
            except (TypeError, ValueError):
                out[key] = value
    return out
