"""Eval: cognitive-memory persona (clause 4.2.10).

Five sub-tests verifying the persona file transfers SME knowledge:

- AT recall
- Exploration strategy recall
- User variant recall
- Heuristic lens override application (Heuristic 6 — Recognition over Recall)
- Baseline inheritance awareness

Each sub-test is a separate `@task` so it has its own rubric. Run with:

    python -m tests.evals tests/evals/personas/eval_cognitive_memory.py

Use `--persona_context_mode all` to run the same tasks with all
elaborated personas loaded in background context, while still grading
cognitive-memory answers.
"""

# NOTE: This eval grades responses against the cognitive-memory persona, which
# adapts W3C COGA material. See personas/cognitive-sources.LICENSE.md for attribution.

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_eval_persona_context
from tests.evals._scorers import rubric_scorer

PERSONA_ALIAS = "cognitive-memory"
PERSONA = load_eval_persona_context(PERSONA_ALIAS)


def _solver():
    return [system_message(PERSONA), generate(**_providers.generation_config())]


@task
def at_recall() -> Task:
    return Task(
        name="cognitive_memory_at_recall",
        dataset=[
            Sample(
                input=(
                    "Identify the assistive technologies and support tools this "
                    "persona uses. For each, give a one-sentence interaction model "
                    "and name a concrete example."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "covers_reminder_calendar",
                    "description": (
                        "Mentions reminder / calendar / notification tools used to "
                        "offload dates, deadlines, and steps out of memory."
                    ),
                },
                {
                    "id": "covers_password_manager",
                    "description": (
                        "Mentions password managers that store / auto-fill "
                        "credentials so the user need not recall or transcribe them."
                    ),
                },
                {
                    "id": "covers_simplification_focus",
                    "description": (
                        "Mentions reading / de-clutter / focus or distraction-"
                        "removing extensions used to reduce clutter and sustain "
                        "attention."
                    ),
                },
                {
                    "id": "covers_form_autofill",
                    "description": (
                        "Mentions form autofill / autocomplete that re-enters "
                        "routine information to avoid recall and re-typing."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "covers_read_aloud_or_personalization",
                    "description": (
                        "Mentions text-to-speech / read-aloud OR personalization / "
                        "simplification semantics as a support."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "reframes_as_mainstream_reliance",
                    "description": (
                        "Frames support as a mix of mainstream features, browser "
                        "extensions, and reliance on built-in platform aids (Back, "
                        "undo, autosave) rather than a single dedicated AT."
                    ),
                    "weight": 1.5,
                },
            ]
        ),
    )


@task
def strategy_recall() -> Task:
    return Task(
        name="cognitive_memory_strategy_recall",
        dataset=[
            Sample(
                input=(
                    "List the persona-specific exploration strategies this user "
                    "employs (NOT the universal baseline strategies). For each, "
                    "briefly describe what the user does."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "orientation_reorientation",
                    "description": (
                        "Includes orientation / re-orientation — using headings, "
                        "breadcrumbs, and step indicators to recover context after "
                        "losing focus."
                    ),
                },
                {
                    "id": "chunked_task_progression",
                    "description": (
                        "Includes working through a task one step at a time, "
                        "relying on each step carrying forward needed information."
                    ),
                },
                {
                    "id": "recognition_over_recall",
                    "description": (
                        "Includes relying on recognition — familiar conventional "
                        "patterns and visible labels — rather than recalling paths "
                        "or shortcuts."
                    ),
                },
                {
                    "id": "distraction_management",
                    "description": (
                        "Includes managing distractions — pausing or blocking "
                        "moving content, notifications, and clutter to hold focus."
                    ),
                },
                {
                    "id": "offloading_external_aids",
                    "description": (
                        "Includes offloading information to external aids "
                        "(reminders, autofill, password managers, notes)."
                    ),
                },
                {
                    "id": "feedback_confirmed_action",
                    "description": (
                        "Includes confirming each action succeeded via explicit "
                        "feedback before proceeding."
                    ),
                },
                {
                    "id": "excludes_baseline_only",
                    "description": (
                        "Focuses on persona-specific strategies; baseline "
                        "strategies (visual scanning, mouse / pointer, reading and "
                        "scrolling, form interaction, navigation and wayfinding, "
                        "touch / pointer) may be acknowledged as inherited but "
                        "should not dominate."
                    ),
                    "weight": 0.5,
                },
            ]
        ),
    )


@task
def variant_recall() -> Task:
    return Task(
        name="cognitive_memory_variant_recall",
        dataset=[
            Sample(
                input=(
                    "List the user variants defined for this persona (disability-"
                    "specific, NOT the New/Expert baseline variants). For each, "
                    "describe what differentiates them in one sentence."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "working_memory_variant",
                    "description": (
                        "Includes a working-memory-limited variant whose barrier is "
                        "carrying / transcribing information across steps."
                    ),
                },
                {
                    "id": "attention_distraction_variant",
                    "description": (
                        "Includes an attention- and distraction-sensitive variant "
                        "derailed by interruptions and moving content."
                    ),
                },
                {
                    "id": "executive_function_variant",
                    "description": (
                        "Includes an executive-function / processing-speed variant "
                        "needing planning support, clear steps, and more time."
                    ),
                },
                {
                    "id": "progressive_decline_variant",
                    "description": (
                        "Includes a progressive-memory-decline variant that cannot "
                        "learn new patterns and depends on familiar, unchanging "
                        "designs."
                    ),
                },
                {
                    "id": "differentiation_clear",
                    "description": (
                        "Each variant's differentiator is concrete and actionable, "
                        "not just renaming the persona."
                    ),
                },
            ]
        ),
    )


@task
def lens_override_h6() -> Task:
    return Task(
        name="cognitive_memory_lens_override_h6",
        dataset=[
            Sample(
                input=(
                    "How does Heuristic 6 (Recognition Rather than Recall) apply "
                    "specifically to a user with limited memory, attention, and "
                    "executive function? Focus on what this persona's lens override "
                    "adds beyond the generic accessibility lens."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "info_at_point_of_use",
                    "description": (
                        "States that everything needed to act must be visible at "
                        "the point of use, so the user never has to hold "
                        "information in mind."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "no_recall_across_steps",
                    "description": (
                        "Notes the user should not have to remember codes, prior "
                        "choices, menu locations, or shortcuts; carry data forward."
                    ),
                },
                {
                    "id": "labels_persist",
                    "description": (
                        "Notes that labels and instructions must not vanish when a "
                        "field gains focus."
                    ),
                },
                {
                    "id": "persona_specific",
                    "description": (
                        "The answer is specific to memory / attention / executive "
                        "function concerns and does not just restate the generic "
                        "Heuristic 6 lens unchanged."
                    ),
                    "weight": 2.0,
                },
            ]
        ),
    )


@task
def baseline_inheritance() -> Task:
    return Task(
        name="cognitive_memory_baseline_inheritance",
        dataset=[
            Sample(
                input=(
                    "The universal baseline defines six exploration strategies: "
                    "Visual scanning and layout comprehension, Mouse / pointer "
                    "interaction, Reading and scrolling, Form interaction, "
                    "Navigation and wayfinding, Touch / pointer interaction. For "
                    "each, state whether THIS persona inherits it and justify in "
                    "one sentence why a user with limited memory, attention, and "
                    "executive function can still use it. Do not introduce "
                    "strategies outside this list."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "all_strategies_apply",
                    "description": (
                        "States that this persona has NO baseline exclusions — all "
                        "six baseline strategies apply (the user's senses and motor "
                        "control are unaffected)."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "no_false_exclusions",
                    "description": (
                        "Does NOT incorrectly claim any baseline strategy is "
                        "excluded for this persona."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "justifications_grounded",
                    "description": (
                        "Justifications reference how a memory- / attention-limited "
                        "user still uses each strategy (e.g. needing consistent "
                        "navigation, feedback, and reduced clutter), not generic "
                        "descriptions of the strategies themselves."
                    ),
                },
            ]
        ),
    )
