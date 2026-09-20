"""A LlamaIndex LLM that answers through the local Claude Code CLI (Module 2 lab).

The CLI runs on the user's existing Claude subscription, so this project needs
no ANTHROPIC_API_KEY. If a key IS present in the environment, use the official
Anthropic integration instead by passing --api to query.py.
"""

import shutil
import subprocess
from typing import Any

from llama_index.core.llms import (
    CompletionResponse,
    CompletionResponseGen,
    CustomLLM,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback

CLI_TIMEOUT_SECONDS = 300


class ClaudeCLI(CustomLLM):
    """Sends one prompt to `claude -p` and returns the text it prints."""

    model: str = "claude-opus-5"
    context_window: int = 200000
    num_output: int = 4096

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        binary = shutil.which("claude")
        if binary is None:
            raise RuntimeError(
                "The claude CLI is not on PATH. Install Claude Code, or run "
                "query.py --api with ANTHROPIC_API_KEY set."
            )
        result = subprocess.run(
            [binary, "-p", "--model", self.model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=CLI_TIMEOUT_SECONDS,
        )
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI failed: {result.stderr.strip()}")
        return CompletionResponse(text=result.stdout.strip())

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        # The CLI returns one block, so stream it as a single chunk.
        response = self.complete(prompt, **kwargs)
        yield response
