"""Deterministic eval: hidden answer-key grading for the cognitive-numeracy persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable cognitive-numeracy persona knowledge that should reliably
be triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies, the
disability-specific user variants, inherited baseline strategies, and bounded
behavior for pricing comparison and date/time selection.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/cognitive_numeracy.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/cognitive_numeracy.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("cognitive-numeracy")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_numeracy",
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
        persona_slug="cognitive_numeracy",
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
        persona_slug="cognitive_numeracy",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this cognitive-numeracy "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_numeracy",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "cognitive-numeracy persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_numeracy",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this cognitive-numeracy persona. Use a short bullet list and "
            "keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_pricing_comparison() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_numeracy",
        section_slug="behavior_pricing_comparison",
        task_name_suffix="",
        prompt=(
            "A cognitive-numeracy user is reviewing a pricing page with multiple "
            "plans showing amounts in different currencies and units. List the "
            "likely things they would check first to assess whether they can "
            "compare options without doing mental math. Use a short bullet list "
            "and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_date_time_selection() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_numeracy",
        section_slug="behavior_date_time_selection",
        task_name_suffix="",
        prompt=(
            "A cognitive-numeracy user needs to select check-in and check-out "
            "dates on a hotel booking page. List the likely things they would "
            "check first to determine whether they can complete the task "
            "without date arithmetic. Use a short bullet list and keep each "
            "bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
