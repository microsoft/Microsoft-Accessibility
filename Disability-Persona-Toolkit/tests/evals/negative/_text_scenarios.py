"""Shared helpers for text-only negative eval scenarios.

These helpers keep scenario-based negative tests lightweight so future
persona cases can swap in any prompt text without reimplementing the same
persona prompt and task wiring.
"""

from __future__ import annotations

from typing import Any

from inspect_ai import Task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_persona_by_alias
from tests.evals._scorers import Criterion, rubric_scorer


def build_negative_text_task(
    *,
    task_name: str,
    persona_alias: str,
    prompt_text: str,
    criteria: list[dict | Criterion] | None = None,
    scorer: Any = None,
) -> Task:
    if (criteria is None) == (scorer is None):
        raise ValueError("Provide exactly one of 'criteria' or 'scorer'")

    persona = load_persona_by_alias(persona_alias)
    system = (
        "You are an accessibility evaluator answering questions about the "
        "Disability Persona Toolkit (DPT) knowledge base. Use only what is in your reference "
        "context. If a request goes beyond that context, say so explicitly "
        "rather than improvising.\n\n"
        "# Persona reference\n\n"
        f"{persona}"
    )

    return Task(
        name=task_name,
        dataset=[
            Sample(
                input=prompt_text,
            )
        ],
        solver=[
            system_message(system),
            generate(**_providers.generation_config()),
        ],
        scorer=scorer if scorer is not None else rubric_scorer(criteria),
    )