"""OpenAI GPT provider — uses Files API + Responses API."""

from __future__ import annotations

from pathlib import Path

from .base import Provider


class OpenAIProvider(Provider):
    name = "openai"
    env_var = "OPENAI_API_KEY"
    install_cmd = "pip install openai"
    aliases = {
        "gpt5":     "gpt-5",
        "gpt5mini": "gpt-5-mini",
        "gpt4o":    "gpt-4o",
    }

    def _make_client(self):
        self.require_sdk("openai")
        from openai import OpenAI
        return OpenAI()

    def extract(self, pdf_path: Path, prompt: str, model: str, max_tokens: int) -> str:
        # Upload PDF, reference it from the Responses API call, then clean up.
        with open(pdf_path, "rb") as f:
            uploaded = self._client.files.create(file=f, purpose="user_data")
        try:
            response = self._client.responses.create(
                model=model,
                max_output_tokens=max_tokens,
                input=[{
                    "role": "user",
                    "content": [
                        {"type": "input_file", "file_id": uploaded.id},
                        {"type": "input_text", "text": prompt},
                    ],
                }],
            )
            return response.output_text
        finally:
            try:
                self._client.files.delete(uploaded.id)
            except Exception:
                pass
