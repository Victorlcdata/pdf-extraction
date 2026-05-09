"""OpenAI GPT provider — uses Files API + Responses API."""

from __future__ import annotations

from pathlib import Path

from .base import Provider, ProviderResult


class OpenAIProvider(Provider):
    name = "openai"
    env_var = "OPENAI_API_KEY"
    install_cmd = "pip install openai"
    aliases = {
        "gpt5": "gpt-5",
        "gpt5mini": "gpt-5-mini",
        "gpt4o": "gpt-4o",
    }

    def _make_client(self):
        self.require_sdk("openai")
        from openai import OpenAI

        return OpenAI()

    def extract(self, pdf_path: Path, prompt: str, model: str, max_tokens: int) -> ProviderResult:
        # Upload PDF, reference it from the Responses API call, then clean up.
        with open(pdf_path, "rb") as f:
            uploaded = self._client.files.create(file=f, purpose="user_data")
        try:
            # `with_raw_response` exposes the rate-limit headers OpenAI returns.
            raw = self._client.responses.with_raw_response.create(
                model=model,
                max_output_tokens=max_tokens,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_file", "file_id": uploaded.id},
                            {"type": "input_text", "text": prompt},
                        ],
                    }
                ],
            )
            response = raw.parse()

            usage = getattr(response, "usage", None)
            input_tokens = getattr(usage, "input_tokens", 0) or 0 if usage else 0
            output_tokens = getattr(usage, "output_tokens", 0) or 0 if usage else 0

            return ProviderResult(
                text=response.output_text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                rate_limit=_extract_rate_limit(raw.headers),
            )
        finally:
            try:
                self._client.files.delete(uploaded.id)
            except Exception:
                pass


def _extract_rate_limit(headers) -> dict:
    """Pull the per-minute rate-limit info OpenAI returns on every response."""
    out = {}
    pairs = [
        ("x-ratelimit-remaining-tokens", "tokens_remaining"),
        ("x-ratelimit-limit-tokens", "tokens_limit"),
        ("x-ratelimit-remaining-requests", "requests_remaining"),
        ("x-ratelimit-limit-requests", "requests_limit"),
        ("x-ratelimit-reset-tokens", "tokens_reset_in"),
    ]
    for header, key in pairs:
        value = headers.get(header)
        if value is None:
            continue
        if key.endswith("_in"):
            out[key] = value
        else:
            try:
                out[key] = int(value)
            except (TypeError, ValueError):
                out[key] = value
    return out
