"""Deterministic eval: hidden answer-key grading for the without-speech persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable without-speech persona knowledge that should
reliably be triggered by the persona prompt, including assistive-technology
categories, named assistive technologies, persona-specific exploration
strategies, disability-specific user variants, inherited baseline strategies,
and bounded behavior for finding non-voice alternatives, avoiding voice-gated
steps, recovering from voice-first prompts, and reviewing scenario-based
voice barriers in complex interfaces.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/without_speech.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/without_speech.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("without-speech")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
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
        persona_slug="without_speech",
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
        persona_slug="without_speech",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this without-speech "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "without-speech persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this without-speech persona, then list excluded baseline "
            "strategies in a separate section. Only report exclusions that are explicitly "
            "present in the persona file's baseline inheritance metadata or inline "
            "baseline content. If there are no excluded baseline strategies, write 'None' "
            "under the excluded section. Do not infer exclusions from the disability "
            "description. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_find_non_voice_alternative() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="behavior_find_non_voice_alternative",
        task_name_suffix="",
        prompt=(
            "A without-speech user encounters a feature that appears to invite "
            "voice input. List the likely things they would check first to tell "
            "whether a practical non-voice alternative exists in the same "
            "context. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_voice_gated_workflow() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="behavior_voice_gated_workflow",
        task_name_suffix="",
        prompt=(
            "A without-speech user is partway through an important workflow and "
            "then hits a voice-based step such as verification, support contact, "
            "or task completion. List the likely things they would check first to "
            "tell whether they are blocked or can continue another way. Use a "
            "short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_recovery_voice_prompt_failure() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="behavior_recovery_voice_prompt_failure",
        task_name_suffix="",
        prompt=(
            "A without-speech user reaches a voice-first prompt such as \"speak "
            "now\" or a failed voice recognition step. List the likely things "
            "they would check first to recover without restarting or abandoning "
            "the task. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_voice_captcha() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="behavior_review_voice_captcha",
        task_name_suffix="",
        prompt=(
            "A without-speech user reaches a CAPTCHA step that highlights a "
            "voice challenge and includes a microphone prompt saying 'speak "
            "the phrase now'. List the likely things they would check first "
            "to tell whether they can complete verification without speaking "
            "or restarting the form. Use a short bullet list and keep each "
            "bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="behavior_review_complex_page",
        task_name_suffix="",
        prompt=(
            "A without-speech user is reviewing a complex web page with a "
            "sticky header, search feature with a microphone icon, filter "
            "sidebar, long results list, account verification prompt, "
            "newsletter signup form, and support section that highlights a "
            "phone option. They can see and hear everything clearly and can "
            "use keyboard, mouse, and touch, but they cannot speak. List the "
            "likely things they would check first to tell whether the page is "
            "fully workable without any voice input. Use a short bullet list "
            "and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_verification_and_support_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="without_speech",
        section_slug="behavior_review_verification_and_support_page",
        task_name_suffix="",
        prompt=(
            "A without-speech user is reviewing a page for account recovery "
            "and support escalation. The interface offers voice biometric "
            "verification, a 'speak now' step after a failed login, a phone "
            "support flow with voice prompts, and a small chat link near the "
            "footer. List the likely things they would check first to verify "
            "they can recover access and get help without speaking or losing "
            "progress. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()