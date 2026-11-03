"""Deterministic eval: hidden answer-key grading for the color-blind persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable color-blind-persona knowledge that should reliably
be triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies, the
disability-specific user variants, and bounded behaviors for interpreting state
and identifying interactive affordances without relying on colour alone,
including a complex-page scenario with multiple colour-encoded signals.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/color_blind.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/color_blind.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("color-blind")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="color_blind",
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
        persona_slug="color_blind",
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
        persona_slug="color_blind",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this color-blind "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="color_blind",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "color-blind persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_interpretation_state_feedback() -> Task:
    return build_persona_deterministic_task(
        persona_slug="color_blind",
        section_slug="behavior_interpretation_state_feedback",
        task_name_suffix="",
        prompt=(
            "A color-blind user encounters status and selection changes in an "
            "interface and needs to work out what changed without relying on "
            "colour. List the likely cues they would check first. Use a short "
            "bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_interaction_affordance() -> Task:
    return build_persona_deterministic_task(
        persona_slug="color_blind",
        section_slug="behavior_interaction_affordance",
        task_name_suffix="",
        prompt=(
            "A color-blind user lands on a page and needs to figure out what "
            "is interactive and what is just static content. List the likely "
            "things they would look for first without relying on colour alone. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_navigation_red_button_protanopia() -> Task:
    return build_persona_deterministic_task(
        persona_slug="color_blind",
        section_slug="behavior_navigation_red_button_protanopia",
        task_name_suffix="",
        prompt=(
            "A user with protanopia is told to use the control that another "
            "person describes only as 'the red button'. List the likely cues "
            "they would check first to figure out which control is meant. Use "
            "a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="color_blind",
        section_slug="behavior_review_complex_page",
        task_name_suffix="",
        prompt=(
            "A color-blind user is reviewing a complex web page that includes "
            "a dashboard summary with red, green, and yellow status badges, a "
            "line chart with multiple coloured series and a legend, a filter "
            "panel with selected chips shown mainly by colour, a table where "
            "negative values are red and positive values are green, and a form "
            "whose validation states are shown with coloured borders. List the "
            "likely cues and checks they would use to understand the page "
            "without relying on colour alone. Use a short bullet list and keep "
            "each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_chart_heavy_analytics_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="color_blind",
        section_slug="behavior_review_chart_heavy_analytics_page",
        task_name_suffix="",
        prompt=(
            "A color-blind user is reviewing a chart-heavy analytics page "
            "with multiple line and bar charts, a heatmap, coloured legends, "
            "red and green trend indicators, and hover tooltips that reveal "
            "series details. They need to compare data series, understand "
            "which trends are positive or negative, and tell whether the "
            "charts remain interpretable without relying on colour alone. "
            "List the likely cues and checks they would use first. Use a "
            "short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
