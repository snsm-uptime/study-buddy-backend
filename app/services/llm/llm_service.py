import json
from string import Template
import re
from enum import Enum
from pathlib import Path
from typing import Any, Literal

import ollama
from returns.future import FutureResult, future_safe
from returns.result import Failure, Result, Success
from tqdm import tqdm

from app.config import get_settings
from app.schemas.prompt_outputs.concept_extraction import ConceptExtractionResponse

settings = get_settings()


class PromptTemplate(str, Enum):
    CONCEPT_EXTRACTOR = "concept_extractor"

    @property
    def path(self) -> Path:
        return Path("app", "dependencies", "prompts", f"{self.value}.md")

    @property
    def template(self) -> str:
        with open(self.path, "r", encoding="utf-8") as file:
            return file.read().strip()


class LLMService:
    def __init__(self, model: str = settings.ollama_model) -> None:
        self.model = model
        self.pull_model()

    def _get_prompt(self, prompt_template: PromptTemplate, **kwargs) -> str:
        """
        Formats the prompt template with the provided input variables.
        """
        template = prompt_template.template
        if not template:
            raise ValueError(f"Prompt template {prompt_template.value} is empty.")
        n_template = Template(template).substitute(**kwargs)
        return n_template

    @future_safe
    async def query(
        self, prompt_template: PromptTemplate, input_vars: dict[str, Any]
    ) -> ConceptExtractionResponse:
        # prompt = self._get_prompt(template, input_vars)
        schema = ConceptExtractionResponse.model_json_schema()
        messages = [
            {"role": "system", "content": prompt_template.template},
            {"role": "user", "content": str(input_vars)},
        ]
        try:
            response = ollama.chat(
                format=schema,
                messages=messages,
                model=self.model,
            )
            content = response["message"]["content"]
            return ConceptExtractionResponse.model_validate(json.loads(content))
        except Exception as e:
            raise ValueError(f"Failed to parse JSON from LLM: {e}")

    def pull_model(self):
        current_digest, bars = "", {}
        for progress in ollama.pull(self.model, stream=True):
            digest = progress.get("digest", "")
            if digest != current_digest and current_digest in bars:
                bars[current_digest].close()

            if not digest:
                print(progress.get("status"))
                continue

            if digest not in bars and (total := progress.get("total")):
                bars[digest] = tqdm(
                    total=total,
                    desc=f"pulling {digest[7:19]}",
                    unit="B",
                    unit_scale=True,
                )

            if completed := progress.get("completed"):
                bars[digest].update(completed - bars[digest].n)

            current_digest = digest
