"""Deterministic eval: hidden answer-key grading for the cognitive-language persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable cognitive-language persona knowledge that should reliably
be triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies, the
disability-specific user variants, inherited baseline strategies, and bounded
behavior for reading dense text and completing form text inputs.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/cognitive_language.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/cognitive_language.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("cognitive-language")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_language",
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
        persona_slug="cognitive_language",
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
        persona_slug="cognitive_language",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this cognitive-language "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_language",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "cognitive-language persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_language",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this cognitive-language persona. Use a short bullet list and "
            "keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_reading_dense_text() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_language",
        section_slug="behavior_reading_dense_text",
        task_name_suffix="",
        prompt=(
            "A cognitive-language user encounters a page with long, dense "
            "paragraphs of technical or bureaucratic text with no icons or "
            "images. List the likely things they would check first to "
            "determine whether they can understand the content. Use a short "
            "bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_form_text_input() -> Task:
    return build_persona_deterministic_task(
        persona_slug="cognitive_language",
        section_slug="behavior_form_text_input",
        task_name_suffix="",
        prompt=(
            "A cognitive-language user needs to fill in a free-text form field "
            "that requires typed input. List the likely things they would "
            "check first to assess whether the form supports their writing "
            "needs. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
