"""Deterministic eval: hidden answer-key grading for the hard-of-hearing persona.

This task uses a deterministic scorer backed by a hidden answer key in
`Sample.metadata["answer_key"]`. The key is not sent to the model; only the prompt and
system context are.

These checks cover stable, factual persona content that should reliably be
triggered by the persona prompt, including assistive-technology categories,
named assistive technologies, persona-specific exploration strategies,
disability-specific user variants, inherited baseline strategies, and
bounded behaviors for audio clarity, captions as supplement, and unreliable
audio cues, including scenario tasks for complex pages and communication-heavy
interfaces.

Run with:

    python -m tests.evals \
        copilot/gpt-5-mini \
        deterministic/hard_of_hearing.py

    python -m tests.evals \
        copilot/claude-sonnet-4.5 \
        deterministic/hard_of_hearing.py
"""

from __future__ import annotations

from inspect_ai import Task, task

from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("hard-of-hearing")


@task
def at_categories() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
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
        persona_slug="hard_of_hearing",
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
        persona_slug="hard_of_hearing",
        section_slug="exploration_strategies",
        task_name_suffix="",
        prompt=(
            "List the persona-specific exploration strategies this hard-of-hearing "
            "evaluator must consider. Exclude inherited universal baseline "
            "strategies. Use a short bullet list and keep each bullet to one "
            "line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def user_variants() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
        section_slug="user_variants",
        task_name_suffix="",
        prompt=(
            "List the disability-specific user variants defined for this "
            "hard-of-hearing persona. Exclude the New/Expert baseline variants. "
            "Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def baseline_strategies() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
        section_slug="baseline_strategies",
        task_name_suffix="",
        prompt=(
            "List the inherited universal baseline exploration strategies that still "
            "apply to this hard-of-hearing persona, then list excluded baseline "
            "strategies in a separate section. Only report exclusions that are explicitly "
            "present in the persona file's baseline inheritance metadata or inline "
            "baseline content. If there are no excluded baseline strategies, write 'None' "
            "under the excluded section. Do not infer exclusions from the disability "
            "description. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_media_audio_clarity() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
        section_slug="behavior_media_audio_clarity",
        task_name_suffix="",
        prompt=(
            "A hard-of-hearing user starts media with spoken content and wants "
            "to decide whether the audio will be usable in their current "
            "listening conditions. List the likely things they would check "
            "first. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_captions_as_supplement() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
        section_slug="behavior_captions_as_supplement",
        task_name_suffix="",
        prompt=(
            "A hard-of-hearing user can hear some of a video or call but keeps "
            "missing words. List the likely things they would check first to "
            "use captions as a supplement rather than as the only channel. Use "
            "a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_audio_alert_redundancy() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
        section_slug="behavior_audio_alert_redundancy",
        task_name_suffix="",
        prompt=(
            "A hard-of-hearing user is interacting with a page where important "
            "feedback may be signaled by sound. List the likely things they "
            "would check first to make sure they will not miss important "
            "events. Use a short bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_complex_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
        section_slug="behavior_review_complex_page",
        task_name_suffix="",
        prompt=(
            "A hard-of-hearing user is reviewing a complex web page that "
            "includes a hero video with music under speech, a webinar signup "
            "panel, notification toasts with sounds, an onboarding clip, a "
            "support area with a phone number, and a form whose success or "
            "error feedback may include audio. List the likely things they "
            "would check first to determine whether the page remains usable "
            "when audio is only partly reliable. Use a short bullet list and "
            "keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()


@task
def behavior_review_communication_heavy_page() -> Task:
    return build_persona_deterministic_task(
        persona_slug="hard_of_hearing",
        section_slug="behavior_review_communication_heavy_page",
        task_name_suffix="",
        prompt=(
            "A hard-of-hearing user is reviewing a communication-heavy "
            "interface for meetings, live announcements, and support. The "
            "page includes a meeting preview, call volume and noise "
            "suppression controls, live caption controls, participant join "
            "alerts, and phone-first support pathways. List the likely cues "
            "and checks they would use first to verify the experience works "
            "when audio is available but not fully reliable. Use a short "
            "bullet list and keep each bullet to one line."
        ),
        persona_prompt=PERSONA,
    )()