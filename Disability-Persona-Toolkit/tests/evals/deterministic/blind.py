"""Deterministic eval: hidden answer-key grading for the blind persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable blind-persona knowledge that should reliably be
triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies, the
disability-specific user variants, and bounded navigation behavior for common
tasks such as finding a button, reaching main content, navigating a complex
page efficiently, interacting with a form, or recovering from form errors.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/blind.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/blind.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("blind")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="blind",
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
        persona_slug="blind",
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
        persona_slug="blind",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this blind "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="blind",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "blind persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_navigation_button() -> Task:
    return build_persona_deterministic_task(
        persona_slug="blind",
        section_slug="behavior_navigation_button",
        task_name_suffix="",
        prompt=(
            "A blind user needs to find a button somewhere on the page. "
            "List the likely ways they would check for it first across common "
            "screen reader interaction patterns. Use a short bullet list and "
            "keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_navigation_main_content() -> Task:
    return build_persona_deterministic_task(
        persona_slug="blind",
        section_slug="behavior_navigation_main_content",
        task_name_suffix="",
        prompt=(
            "A blind user lands on a busy page and wants to get oriented and "
            "reach the main content quickly. List the likely things they would "
            "try first, including at least one approach that would still work "
            "for a less experienced screen reader user. Use a short bullet "
            "list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_navigation_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="blind",
        section_slug="behavior_navigation_complex_page",
        task_name_suffix="",
        prompt=(
            "A blind desktop screen reader user lands on a complex web page "
            "with a global navigation bar, a site search field, a promotional "
            "banner, a filter sidebar, a long results area, a comparison table, "
            "and a newsletter signup form near the end of the page. They want "
            "to get oriented quickly, skip repeated page chrome, jump to the "
            "main results, inspect the comparison table, complete the signup "
            "form, and confirm whether submission succeeded. List the likely "
            "assistive-technology actions and exploration strategies they would "
            "use to complete this efficiently. Use a short bullet list and keep "
            "each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_interaction_form() -> Task:
    return build_persona_deterministic_task(
        persona_slug="blind",
        section_slug="behavior_interaction_form",
        task_name_suffix="",
        prompt=(
            "A blind user needs to complete a form they have not seen before. "
            "List the likely things they would do to understand the form, move "
            "through it, and tell what happened after submission. Use a short "
            "bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_recovery_form_errors() -> Task:
    return build_persona_deterministic_task(
        persona_slug="blind",
        section_slug="behavior_recovery_form_errors",
        task_name_suffix="",
        prompt=(
            "A blind user submits a form and something goes wrong. List the "
            "likely things they would check to understand the problem, get back "
            "to the right place, and confirm they have recovered successfully. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()