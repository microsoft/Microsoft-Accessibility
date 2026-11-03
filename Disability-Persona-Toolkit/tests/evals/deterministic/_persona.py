"""Shared helpers for deterministic persona eval modules.

These helpers encode the default convention for persona-level deterministic
checks: stable hidden-answer-key tasks backed by registries in
``tests/evals/answer_keys``. Most tasks are closed-set recall, but the same
shape also supports stable scenario prompts that expect a bounded set of
persona-specific behaviors. Behavior answer keys should be more alias-rich than
recall keys because supported models may express the same blind-navigation or
recovery behavior with slightly different wording while still being correct.
"""

from __future__ import annotations

from inspect_ai import Task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._scorers import answer_key_scorer
from tests.evals.answer_keys import load_answer_key_from_file


_STANDARD_SECTION_SLUGS = {
    "at_categories",
    "assistive_technologies",
    "persona_types",
    "exploration_strategies",
    "user_variants",
    "baseline_strategies",
}


def _validate_section_slug(section_slug: str) -> None:
    if section_slug in _STANDARD_SECTION_SLUGS:
        return
    if section_slug.startswith("behavior_"):
        return
    raise ValueError(
        "Deterministic section slugs must be either a standard recall slug "
        "or a behavior slug prefixed with 'behavior_'."
    )


def persona_deterministic_solver(persona_prompt: str) -> list:
    return [
        system_message(persona_prompt),
        generate(**_providers.generation_config()),
    ]


def build_persona_deterministic_task(
    *,
    persona_slug: str,
    section_slug: str,
    prompt: str,
    persona_prompt: str,
    task_name_suffix: str = "_deterministic",
):
    _validate_section_slug(section_slug)
    task_name = f"{persona_slug}_{section_slug}{task_name_suffix}"
    answer_key_name = f"{persona_slug}.{section_slug}"

    def factory() -> Task:
        return Task(
            name=task_name,
            dataset=[
                Sample(
                    input=prompt,
                    metadata={
                        "answer_key": load_answer_key_from_file(answer_key_name)
                    },
                )
            ],
            solver=persona_deterministic_solver(persona_prompt),
            scorer=answer_key_scorer(),
        )

    return factory
