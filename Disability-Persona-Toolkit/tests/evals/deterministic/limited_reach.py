"""Deterministic eval: hidden answer-key grading for the limited-reach persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable limited-reach persona knowledge that should reliably
be triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies, the
disability-specific user variants, inherited baseline strategies, and bounded
behavior for assessing target sizes and drag alternatives.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/limited_reach.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/limited_reach.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("limited-reach")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="limited_reach",
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
        persona_slug="limited_reach",
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
        persona_slug="limited_reach",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this limited-reach "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="limited_reach",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "limited-reach persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="limited_reach",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this limited-reach persona. Use a short bullet list and keep "
            "each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_target_assessment() -> Task:
    return build_persona_deterministic_task(
        persona_slug="limited_reach",
        section_slug="behavior_target_assessment",
        task_name_suffix="",
        prompt=(
            "A limited-reach user is reviewing a page with many small clickable "
            "elements close together. List the likely things they would check "
            "first to assess whether the targets are safe and reachable for "
            "them. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_drag_alternative() -> Task:
    return build_persona_deterministic_task(
        persona_slug="limited_reach",
        section_slug="behavior_drag_alternative",
        task_name_suffix="",
        prompt=(
            "A limited-reach user encounters a slider or reorder control that "
            "requires dragging. List the likely things they would check first "
            "to determine if there is a usable single-pointer alternative. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
