"""Google Gemini provider — uses Files API for PDF upload."""

from __future__ import annotations

from pathlib import Path

from .base import Provider, ProviderResult


class GoogleProvider(Provider):
    name = "google"
    env_var = "GOOGLE_API_KEY"
    install_cmd = "pip install google-genai"
    aliases = {
        "pro": "gemini-2.5-pro",
        "flash": "gemini-2.5-flash",
    }

    def _make_client(self):
        self.require_sdk("google.genai")
        from google import genai

        return genai.Client()

    def extract(self, pdf_path: Path, prompt: str, model: str, max_tokens: int) -> ProviderResult:
        from google.genai import types

        # Upload the PDF via the Files API (works for any size up to provider limits).
        uploaded = self._client.files.upload(file=str(pdf_path))
        try:
            response = self._client.models.generate_content(
                model=model,
                contents=[uploaded, prompt],
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    response_mime_type="application/json",
                ),
            )

            # Gemini exposes per-call usage via response.usage_metadata. Rate-limit
            # headers aren't surfaced through the python SDK, so we leave that empty.
            usage = getattr(response, "usage_metadata", None)
            input_tokens = getattr(usage, "prompt_token_count", 0) or 0 if usage else 0
            output_tokens = getattr(usage, "candidates_token_count", 0) or 0 if usage else 0

            return ProviderResult(
                text=response.text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                rate_limit={},
            )
        finally:
            # Best-effort cleanup of the uploaded file.
            try:
                self._client.files.delete(name=uploaded.name)
            except Exception:
                pass
