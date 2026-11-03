"""Deterministic eval: hidden answer-key grading for the voice-access persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable voice-access persona knowledge that should reliably
be triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies,
disability-specific user variants, inherited baseline strategies, and bounded
behavior for label-based activation, fallback targeting, and dictation,
including scenario tasks for complex pages and rich interaction interfaces.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/voice_access.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/voice_access.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("voice-access")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
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
        persona_slug="voice_access",
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
        persona_slug="voice_access",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this voice-access "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "voice-access persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this voice-access persona, then list excluded baseline strategies "
            "in a separate section. Only report exclusions that are explicitly present in "
            "the persona file's baseline inheritance metadata or inline baseline content. "
            "Do not infer additional exclusions from the disability description. Follow "
            "the persona file literally: if a baseline strategy appears inline in the "
            "persona, treat it as applicable even if it seems surprising; if a baseline "
            "strategy is named in `baseline_excludes`, list it under excluded baseline "
            "strategies. In this persona, `mouse-pointer-interaction` is the explicit "
            "baseline exclusion, while `Touch / pointer interaction` still appears inline "
            "and must remain in the applicable list. Use a short bullet list and keep each "
            "bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_activate_visible_control() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
        section_slug="behavior_activate_visible_control",
        task_name_suffix="",
        prompt=(
            "A voice-access user can see the control they want and wants the "
            "fastest way to activate it without using their hands. List the "
            "likely things they would check first to tell whether natural "
            "voice commands will work. Use a short bullet list and keep each "
            "bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_fallback_targeting_unlabeled_control() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
        section_slug="behavior_fallback_targeting_unlabeled_control",
        task_name_suffix="",
        prompt=(
            "A voice-access user finds a control they can see but cannot "
            "activate by saying its obvious name. List the likely things they "
            "would try next to reach it and tell whether the interface is "
            "still workable. Use a short bullet list and keep each bullet to "
            "one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_dictation_text_input() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
        section_slug="behavior_dictation_text_input",
        task_name_suffix="",
        prompt=(
            "A voice-access user reaches a text field and needs to enter a "
            "sentence by dictation, then continue through the form. List the "
            "likely things they would check first to see whether text entry "
            "and editing will work smoothly. Use a short bullet list and keep "
            "each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
        section_slug="behavior_review_complex_page",
        task_name_suffix="",
        prompt=(
            "A voice-access user is reviewing a complex web page with a "
            "sticky header, search box, filter sidebar, long results area, "
            "comparison table, newsletter signup form, and occasional promo "
            "modal. They can see the page clearly but must operate it "
            "entirely by voice. List the likely things they would check first "
            "to tell whether the page is efficient and workable without any "
            "hand input. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_interaction_heavy_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="voice_access",
        section_slug="behavior_review_interaction_heavy_page",
        task_name_suffix="",
        prompt=(
            "A voice-access user is reviewing a rich interaction interface "
            "with a left navigation pane, toolbar, icon-only buttons, custom "
            "dropdowns, command palette, date picker, modal dialogs, and text "
            "fields that support dictation. List the likely things they would "
            "check first to verify the interface remains efficient by voice, "
            "and that fallback methods are available when natural commands "
            "fail. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()