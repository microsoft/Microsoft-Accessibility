"""Deterministic eval: hidden answer-key grading for the keyboard-only persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable keyboard-only persona knowledge that should reliably
be triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies, the
disability-specific user variants, inherited baseline strategies, and bounded
behavior for reaching a visible action efficiently, operating custom widgets,
and escaping overlays without getting trapped, including scenario tasks for
complex pages and rich interaction interfaces.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/keyboard_only.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/keyboard_only.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("keyboard-only")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
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
        persona_slug="keyboard_only",
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
        persona_slug="keyboard_only",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this keyboard-only "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "keyboard-only persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this keyboard-only persona, and also name any excluded baseline "
            "strategy. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_navigation_primary_action() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
        section_slug="behavior_navigation_primary_action",
        task_name_suffix="",
        prompt=(
            "A keyboard-only user can already see the page and knows which "
            "primary action they want. List the likely things they would "
            "check first to reach it efficiently without a mouse. Use a "
            "short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_interaction_custom_widget() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
        section_slug="behavior_interaction_custom_widget",
        task_name_suffix="",
        prompt=(
            "A keyboard-only user reaches a custom widget such as a menu, "
            "tablist, dropdown, or date picker. List the likely things they "
            "would check first to tell whether it is fully operable without a "
            "mouse. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_escape_overlay() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
        section_slug="behavior_escape_overlay",
        task_name_suffix="",
        prompt=(
            "A keyboard-only user opens a dialog, menu, or other overlay and "
            "wants to continue or back out safely. List the likely things they "
            "would check first so they do not get stuck or lose their place. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
        section_slug="behavior_review_complex_page",
        task_name_suffix="",
        prompt=(
            "A keyboard-only user is reviewing a complex web page with a "
            "sticky header, skip link, filter sidebar, long results area, "
            "comparison table, newsletter signup form, and an occasional "
            "promo modal. They can see the page and know what they want, but "
            "must operate everything without a mouse. List the likely things "
            "they would check first to tell whether the page is efficient and "
            "safe to use by keyboard only. Use a short bullet list and keep "
            "each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_interaction_heavy_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="keyboard_only",
        section_slug="behavior_review_interaction_heavy_page",
        task_name_suffix="",
        prompt=(
            "A keyboard-only user is reviewing a rich interaction interface "
            "with a left navigation pane, toolbar, tablist, custom dropdowns, "
            "date picker, command palette, and modal dialogs. List the likely "
            "things they would check first to verify the interface is fully "
            "operable and does not trap them when using only the keyboard. Use "
            "a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
