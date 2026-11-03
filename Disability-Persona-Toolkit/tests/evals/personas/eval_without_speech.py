"""Eval: without-speech persona (clause 4.2.6).

Five sub-tests verifying the persona file transfers SME knowledge:

- AT recall
- Exploration strategy recall
- User variant recall
- Heuristic lens override application
- Baseline inheritance awareness

Each sub-test is a separate `@task` so it has its own rubric. Run with:

    python -m tests.evals tests/evals/personas/eval_without_speech.py

Use `--persona_context_mode all` to run the same tasks with all
elaborated personas loaded in background context, while still grading
without-speech answers.

Add `-T` to limit to one sub-test, e.g. `--task at_recall`.
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_eval_persona_context
from tests.evals._scorers import rubric_scorer

PERSONA_ALIAS = "without-speech"
PERSONA = load_eval_persona_context(PERSONA_ALIAS)


def _solver():
    return [system_message(PERSONA), generate(**_providers.generation_config())]


@task
def at_recall() -> Task:
    return Task(
        name="without_speech_at_recall",
        dataset=[
            Sample(
                input=(
                    "Identify the assistive technology category(ies) this persona uses. "
                    "For each, give a one-sentence interaction model. If the persona "
                    "uses only one category, name at least one concrete example tool "
                    "within it."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "covers_keyboard_mouse_touch",
                    "description": (
                        "Mentions standard input methods (keyboard, mouse, touch) as "
                        "the primary AT for users without speech — no voice features."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "clarifies_no_voice_input",
                    "description": (
                        "Clarifies that this persona specifically cannot or does not "
                        "use voice input (distinct from other personas that use voice)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "no_false_categories",
                    "description": (
                        "Does NOT list voice input, voice control, or dictation AS ATs "
                        "THIS PERSONA USES. Mentioning them in a negated/contrastive "
                        "context (e.g., 'cannot use voice input') is REQUIRED by the "
                        "clarifies_no_voice_input criterion and counts as YES here. "
                        "Mark NO only if the answer presents voice features as "
                        "available or used by this persona."
                    ),
                    "weight": 2.0,
                },
            ]
        ),
    )


@task
def strategy_recall() -> Task:
    return Task(
        name="without_speech_strategy_recall",
        dataset=[
            Sample(
                input=(
                    "List the persona-specific exploration strategies this "
                    "user employs (NOT the universal baseline strategies). "
                    "For each, briefly describe what the user does."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "seeking_text_alternatives",
                    "description": (
                        "Includes seeking text alternatives or workarounds for "
                        "voice-only features (e.g., finding email instead of phone)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "avoiding_voice_gates",
                    "description": (
                        "Includes avoiding voice-gated workflows or features that "
                        "require voice input and have no keyboard/text alternative."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "no_voice_strategies_listed",
                    "description": (
                        "Does NOT list voice input, dictation, voice commands, or "
                        "other voice-based strategies as strategies THIS PERSONA "
                        "USES. Mentioning them in a negated/contrastive context "
                        "(e.g., 'avoids voice-gated workflows', 'cannot use "
                        "dictation') is REQUIRED and counts as YES. Mark NO only "
                        "if the answer presents voice strategies as available or "
                        "used by this persona."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "excludes_baseline_only",
                    "description": (
                        "Lists strategies specific to non-voice input. Baseline "
                        "visual/pointer/reading strategies may be acknowledged but should "
                        "not dominate."
                    ),
                    "weight": 0.5,
                },
            ]
        ),
    )


@task
def variant_recall() -> Task:
    return Task(
        name="without_speech_variant_recall",
        dataset=[
            Sample(
                input=(
                    "List the user variants defined for this persona "
                    "(disability-specific, NOT the New/Expert baseline "
                    "variants). For each, describe what differentiates them "
                    "from the others in one sentence."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "cannot_use_voice_variant",
                    "description": (
                        "Includes a variant of users who cannot produce voice input "
                        "at all (medically unable, laryngectomy, etc.)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "differentiation_clear",
                    "description": (
                        "Variant differentiators are concrete (medical inability, "
                        "environmental constraint, preference) and actionable."
                    ),
                    "weight": 1.0,
                },
            ]
        ),
    )


@task
def lens_override_h1() -> Task:
    return Task(
        name="without_speech_lens_override_h1",
        dataset=[
            Sample(
                input=(
                    "How does Heuristic 1 (Visibility of System Status) "
                    "apply specifically to a user without speech? Focus on what "
                    "this persona's lens override adds beyond the generic "
                    "accessibility lens — voice-free feedback and text input."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "no_voice_status_dependency",
                    "description": (
                        "Notes that status feedback must NOT require voice output or "
                        "rely only on voice as the status channel."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "text_status_required",
                    "description": (
                        "Emphasizes that status must be available as text (e.g., "
                        "visible on-screen messages, notifications, or in accessibility "
                        "tree) so non-voice users receive it."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "acknowledges_non_response",
                    "description": (
                        "Notes that after a voice attempt fails or no voice input is "
                        "given, the system must visibly acknowledge the non-response "
                        "and offer an alternative path rather than silently waiting, "
                        "timing out, or looping prompts like 'please try again'."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "equal_prominence_text_path",
                    "description": (
                        "States that when voice input is offered, the system must "
                        "clearly show that text input is also accepted — making the "
                        "non-voice path equally visible/prominent rather than a "
                        "hidden fallback."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "persona_specific",
                    "description": (
                        "The answer is specific to non-voice concerns and does not just "
                        "restate the generic Heuristic 1 lens unchanged."
                    ),
                    "weight": 2.0,
                },
            ]
        ),
    )


@task
def baseline_inheritance() -> Task:
    return Task(
        name="without_speech_baseline_inheritance",
        dataset=[
            Sample(
                input=(
                    "The universal baseline defines six exploration strategies: "
                    "Visual scanning and layout comprehension, Mouse / pointer "
                    "interaction, Reading and scrolling, Form interaction, "
                    "Navigation and wayfinding, Touch / pointer interaction. "
                    "For each, state whether THIS persona inherits it and "
                    "justify in one sentence why a user without speech can "
                    "(or cannot) still use it. Do not introduce strategies "
                    "outside this list."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "all_strategies_apply",
                    "description": (
                        "States that users without speech inherit ALL baseline strategies: "
                        "visual scanning, mouse/pointer interaction, reading and scrolling, "
                        "form interaction, navigation and wayfinding, touch/pointer "
                        "interaction."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "no_false_exclusions",
                    "description": (
                        "Does NOT incorrectly exclude visual, pointer, or reading "
                        "strategies (non-voice users CAN see, interact, and read normally)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "justifications_grounded",
                    "description": (
                        "Justifications reference how non-voice users STILL use these "
                        "strategies, not generic descriptions."
                    ),
                    "weight": 1.0,
                },
            ]
        ),
    )
