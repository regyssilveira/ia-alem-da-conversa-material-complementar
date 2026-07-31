from __future__ import annotations

import json
import os
import time
import urllib.request
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ModelRequest:
    task: str
    prompt: str
    max_output_tokens: int = 200


@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None


class ModelAdapter(Protocol):
    name: str

    def generate(self, request: ModelRequest) -> ModelResponse: ...


class ReplayAdapter:
    """Adaptador offline: devolve respostas versionadas pelo identificador da tarefa."""

    def __init__(self, responses: dict[str, str], name: str = "replay-v1") -> None:
        self.name = name
        self._responses = dict(responses)

    def generate(self, request: ModelRequest) -> ModelResponse:
        started = time.perf_counter()
        text = self._responses.get(request.task, "")
        return ModelResponse(
            text=text,
            model=self.name,
            latency_ms=(time.perf_counter() - started) * 1000,
        )


class OpenAICompatibleAdapter:
    """Cliente HTTP opcional para endpoints compatíveis com `chat/completions`."""

    def __init__(
        self,
        *,
        base_url: str,
        model: str,
        api_key: str,
        timeout_seconds: float = 30,
    ) -> None:
        self.name = model
        self._url = base_url.rstrip("/") + "/chat/completions"
        self._api_key = api_key
        self._timeout = timeout_seconds

    @classmethod
    def from_environment(cls) -> "OpenAICompatibleAdapter":
        required = ("MODEL_BASE_URL", "MODEL_NAME", "MODEL_API_KEY")
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise ValueError("Variáveis ausentes: " + ", ".join(missing))
        return cls(
            base_url=os.environ["MODEL_BASE_URL"],
            model=os.environ["MODEL_NAME"],
            api_key=os.environ["MODEL_API_KEY"],
        )

    def generate(self, request: ModelRequest) -> ModelResponse:
        body = json.dumps(
            {
                "model": self.name,
                "messages": [{"role": "user", "content": request.prompt}],
                "max_tokens": request.max_output_tokens,
                "temperature": 0,
            }
        ).encode("utf-8")
        http_request = urllib.request.Request(
            self._url,
            data=body,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        started = time.perf_counter()
        with urllib.request.urlopen(http_request, timeout=self._timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        latency_ms = (time.perf_counter() - started) * 1000
        usage = payload.get("usage", {})
        return ModelResponse(
            text=payload["choices"][0]["message"]["content"],
            model=str(payload.get("model", self.name)),
            latency_ms=latency_ms,
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
        )


class TaskRouter:
    def __init__(
        self,
        default: ModelAdapter,
        specialized: dict[str, ModelAdapter] | None = None,
    ) -> None:
        self._default = default
        self._specialized = specialized or {}

    def generate(self, request: ModelRequest) -> ModelResponse:
        adapter = self._specialized.get(request.task, self._default)
        return adapter.generate(request)
