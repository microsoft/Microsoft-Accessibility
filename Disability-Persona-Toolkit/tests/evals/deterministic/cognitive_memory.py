"""Deterministic eval: hidden answer-key grading for the cognitive-memory persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable cognitive-memory persona knowledge that should reliably
be triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies, the
disability-specific user variants, inherited baseline strategies, and bounded
behavior for multi-step forms and distraction/interruption handling.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/cognitive_memory.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/cognitive_memory.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("cognitive-memory")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_memory",
        section_slug="at_categories",
        task_name_suffix="",
        prompt=(
            "Name the assistive technology categories described in this "
            "persona. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def assistive_technologies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_memory",
        section_slug="assistive_technologies",
        task_name_suffix="",
        prompt=(
            "List the named assistive technologies described in this "
            "persona's Assistive Technologies section. Use the specific "
            "technology names from the persona, not just broad categories. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def exploration_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_memory",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this cognitive-memory "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_memory",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "cognitive-memory persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_memory",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this cognitive-memory persona. Use a short bullet list and keep "
            "each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_multi_step_form() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_memory",
        section_slug="behavior_multi_step_form",
        task_name_suffix="",
        prompt=(
            "A cognitive-memory user is filling out a multi-step online form. "
            "List the likely things they would check first to assess whether "
            "the form is safe and usable without relying on recall from "
            "previous steps. Use a short bullet list and keep each bullet to "
            "one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_distraction_interruption() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_memory",
        section_slug="behavior_distraction_interruption",
        task_name_suffix="",
        prompt=(
            "A cognitive-memory user is working through a task when autoplaying "
            "content and notification popups appear on the page. List the "
            "likely things they would check first to determine if they can "
            "stay on track without losing their place. Use a short bullet "
            "list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
