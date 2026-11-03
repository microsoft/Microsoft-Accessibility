"""Deterministic eval: hidden answer-key grading for the low-vision persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable low-vision persona knowledge that should reliably be
triggered by the persona prompt, including both assistive-technology categories
and named assistive technologies, the distinct low-vision user types the
evaluator must consider, the persona-specific exploration strategies, the
disability-specific user variants, and bounded behavior for zoomed reading,
magnified orientation, and forced-colours visibility, including scenario tasks
for complex pages and chart-heavy analytics views.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/low_vision.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/low_vision.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("low-vision")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
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
        persona_slug="low_vision",
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
def persona_types() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="persona_types",
        task_name_suffix="",
        prompt=(
            "When evaluating an interface with this persona, list the distinct "
            "low-vision user types the evaluator must consider. Use a short "
            "bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def exploration_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this low-vision "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "low-vision persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_zoomed_reading_reflow() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="behavior_zoomed_reading_reflow",
        task_name_suffix="",
        prompt=(
            "A low-vision user increases text size or browser zoom because the "
            "default page is hard to read. List the likely things they would "
            "check first to tell whether the page still works comfortably. Use "
            "a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_magnified_viewport_orientation() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="behavior_magnified_viewport_orientation",
        task_name_suffix="",
        prompt=(
            "A low-vision user is using a screen magnifier and can see only a "
            "small part of the interface at once. List the likely things they "
            "would check first to stay oriented and avoid losing content while "
            "moving around. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_high_contrast_visibility() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="behavior_high_contrast_visibility",
        task_name_suffix="",
        prompt=(
            "A low-vision user turns on a high-contrast or forced-colours theme "
            "before using the page. List the likely things they would check "
            "first to confirm the interface is still understandable and usable. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="behavior_review_complex_page",
        task_name_suffix="",
        prompt=(
            "A low-vision user is reviewing a complex web page with a sticky "
            "header, filter sidebar, long results list, comparison table, "
            "newsletter signup form, autocomplete suggestions, and toast "
            "messages. They may use browser zoom, a screen magnifier, or a "
            "high-contrast theme. List the likely things they would check "
            "first to tell whether the page remains readable, oriented, and "
            "usable. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_chart_heavy_analytics_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="low_vision",
        section_slug="behavior_review_chart_heavy_analytics_page",
        task_name_suffix="",
        prompt=(
            "A low-vision user is reviewing a chart-heavy analytics page "
            "with multiple line and bar charts, a heatmap, legends, hover "
            "tooltips, summary cards, and filter controls. They may use 200% "
            "zoom, high magnification, or forced-colours mode. List the likely "
            "things they would check first to tell whether the charts and "
            "supporting controls remain readable and understandable. Use a "
            "short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
