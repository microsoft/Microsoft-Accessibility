"""Deterministic eval: hidden answer-key grading for the deaf persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable, factual persona content that should reliably be
triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies,
disability-specific user variants, inherited baseline strategies, and
bounded behaviors for video captions, audio cues, and common web-page audio
barriers, including scenario tasks for complex pages and communication-heavy
interfaces.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/deaf.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/deaf.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("deaf")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
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
        persona_slug="deaf",
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
        persona_slug="deaf",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this deaf "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "deaf persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this deaf persona, then list excluded baseline strategies in a "
            "separate section. Only report exclusions that are explicitly present in the "
            "persona file's baseline inheritance metadata or inline baseline content. If "
            "there are no excluded baseline strategies, write 'None' under the excluded "
            "section. Do not infer exclusions from the disability description. Use a short "
            "bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_interaction_video_captions() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
        section_slug="behavior_interaction_video_captions",
        task_name_suffix="",
        prompt=(
            "A deaf user starts a video that appears to include important "
            "spoken information. List the likely things they would check "
            "first to decide whether they can follow it without hearing. Use "
            "a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_feedback_audio_alerts() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
        section_slug="behavior_feedback_audio_alerts",
        task_name_suffix="",
        prompt=(
            "A deaf user performs an action on a web page and wants to know "
            "whether anything happened, even if the page normally uses sound "
            "for feedback. List the likely on-screen cues they would look "
            "for. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_web_page_audio_barriers() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
        section_slug="behavior_review_web_page_audio_barriers",
        task_name_suffix="",
        prompt=(
            "A deaf user is interacting with a typical web page and wants to "
            "spot features that may break because they depend on hearing. "
            "List the likely problem areas they would check first. Use a "
            "short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
        section_slug="behavior_review_complex_page",
        task_name_suffix="",
        prompt=(
            "A deaf user is reviewing a complex web page that includes a "
            "hero video, a live webinar signup panel, notification toasts, "
            "an audio-based onboarding clip, a support section that promotes "
            "calling a phone number, and a form whose success and error "
            "feedback may include sounds. List the likely things they would "
            "check first to determine whether the page remains usable without "
            "hearing. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_communication_heavy_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="deaf",
        section_slug="behavior_review_communication_heavy_page",
        task_name_suffix="",
        prompt=(
            "A deaf user is reviewing a communication-heavy interface for "
            "joining video meetings, receiving live announcements, and "
            "contacting support. The page includes a meeting preview, live "
            "caption controls, participant join alerts, a request-an-"
            "interpreter option, and phone-first support pathways. List the "
            "likely cues and checks they would use first to verify the "
            "experience works without hearing. Use a short bullet list and "
            "keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()
