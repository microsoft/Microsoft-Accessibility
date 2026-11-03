"""Eval: blind persona (clause 4.2.1).

Five sub-tests verifying the persona file transfers SME knowledge:

- AT recall
- Exploration strategy recall
- User variant recall
- Heuristic lens override application
- Baseline inheritance awareness

Each sub-test is a separate `@task` so it has its own rubric. Run with:

    python -m tests.evals tests/evals/personas/eval_blind.py

Use `--persona_context_mode all` to run the same tasks with all
elaborated personas loaded in background context, while still grading
blind answers.

Add `-T` to limit to one sub-test, e.g. `--task at_recall`.
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_eval_persona_context
from tests.evals._scorers import rubric_scorer

PERSONA_ALIAS = "blind"
PERSONA = load_eval_persona_context(PERSONA_ALIAS)


def _solver():
    return [system_message(PERSONA), generate(**_providers.generation_config())]


@task
def at_recall() -> Task:
    return Task(
        name="blind_at_recall",
        dataset=[
            Sample(
                input=(
                    "Identify the assistive technology category(ies) this persona uses. "
                    "For each, give a one-sentence interaction model and name at least "
                    "one concrete tool, distinguished by platform where relevant."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "covers_screen_readers",
                    "description": (
                        "Mentions screen reader software (e.g., JAWS, NVDA, "
                        "VoiceOver, Narrator, TalkBack) as the primary AT "
                        "category for blind users."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "screen_reader_models_distinct",
                    "description": (
                        "Distinguishes screen readers by platform or interaction "
                        "model (e.g., JAWS/NVDA for desktop, VoiceOver for macOS/"
                        "iOS, TalkBack for Android, Narrator for Windows), showing "
                        "understanding of different contexts."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "covers_braille_display",
                    "description": (
                        "Mentions refreshable braille display as a distinct AT "
                        "category for users who read braille."
                    ),
                },
                {
                    "id": "no_false_categories",
                    "description": (
                        "Does NOT list visual/display-related ATs (magnifiers, zoom, "
                        "brightness, contrast) or mouse/pointer interaction AS ATs "
                        "THIS PERSONA USES. Mentioning them in a negated/contrastive "
                        "context (e.g., 'cannot use a magnifier') is acceptable and "
                        "counts as YES. Mark NO only if the answer presents these as "
                        "available or used by blind users."
                    ),
                    "weight": 2.0,
                },
            ]
        ),
    )


@task
def strategy_recall() -> Task:
    return Task(
        name="blind_strategy_recall",
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
                    "id": "heading_navigation",
                    "description": (
                        "Includes heading-based navigation as a primary strategy "
                        "for scanning page structure via screen reader."
                    ),
                },
                {
                    "id": "landmark_navigation",
                    "description": (
                        "Includes navigation by ARIA landmarks (main, nav, aside, "
                        "region) for orienting within a page."
                    ),
                },
                {
                    "id": "element_list_navigation",
                    "description": (
                        "Includes using the screen reader's elements list (links, "
                        "buttons, headings, form fields) to jump to desired content."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "sequential_reading",
                    "description": (
                        "Includes sequential top-to-bottom reading with the screen "
                        "reader as a fallback or detailed review strategy."
                    ),
                },
                {
                    "id": "keyboard_shortcuts",
                    "description": (
                        "Includes keyboard shortcuts (e.g., JAWS/NVDA find, "
                        "application shortcuts) for efficient navigation."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "excludes_baseline_only",
                    "description": (
                        "Lists strategies that are screen-reader-specific. "
                        "Strategies marked as baseline (form interaction, navigation "
                        "and wayfinding, touch/pointer interaction) may be acknowledged "
                        "but should not dominate; visual/pointer-only strategies "
                        "should NOT appear."
                    ),
                    "weight": 1.5,
                },
            ]
        ),
    )


@task
def variant_recall() -> Task:
    return Task(
        name="blind_variant_recall",
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
                    "id": "desktop_screen_reader_variant",
                    "description": (
                        "Includes a desktop screen reader variant (e.g., JAWS/NVDA "
                        "on Windows, VoiceOver on macOS) as distinct from mobile."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "mobile_screen_reader_variant",
                    "description": (
                        "Includes a mobile screen reader variant (VoiceOver on iOS, "
                        "TalkBack on Android) with touch-based interaction."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "braille_display_variant",
                    "description": (
                        "Includes a braille display user variant, distinguishing "
                        "tactile reading from speech-only users."
                    ),
                },
                {
                    "id": "beginner_variant",
                    "description": (
                        "Includes a beginner/novice screen reader user variant "
                        "with distinct strategies from expert users."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "differentiation_clear",
                    "description": (
                        "Each variant's differentiator is concrete and actionable "
                        "(e.g., specific screen reader, platform, skill level, or "
                        "AT combination), not just renaming the persona."
                    ),
                },
            ]
        ),
    )


@task
def lens_override_h1() -> Task:
    return Task(
        name="blind_lens_override_h1",
        dataset=[
            Sample(
                input=(
                    "How does Heuristic 1 (Visibility of System Status) "
                    "apply specifically to a blind user? Focus on what "
                    "this persona's lens override adds beyond the generic "
                    "accessibility lens — screen reader feedback, audio cues, "
                    "and similar concerns."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "screen_reader_announcement",
                    "description": (
                        "Notes that status updates must be announced to screen "
                        "readers, not just visible on screen. Example: live regions, "
                        "aria-live, or spoken feedback."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "offline_screen_reader",
                    "description": (
                        "Addresses status updates that occur off-screen or in "
                        "floating elements that may be missed by screen reader focus."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "accessibility_tree_accuracy",
                    "description": (
                        "Emphasizes that semantics in the accessibility tree must "
                        "accurately reflect the interface state, not just visual state."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "audio_supplement",
                    "description": (
                        "Mentions audio cues or earcons that provide non-speech "
                        "feedback as a supplement to screen reader output."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "persona_specific",
                    "description": (
                        "The answer is specific to blind/screen reader concerns and "
                        "does not just restate the generic Heuristic 1 lens unchanged."
                    ),
                    "weight": 2.0,
                },
            ]
        ),
    )


@task
def baseline_inheritance() -> Task:
    return Task(
        name="blind_baseline_inheritance",
        dataset=[
            Sample(
                input=(
                    "Which baseline exploration strategies does this persona "
                    "inherit, and which are excluded? For each, justify in "
                    "one sentence."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "identifies_exclusions",
                    "description": (
                        "Correctly identifies that visual scanning is NOT applicable "
                        "to blind users (they cannot visually scan or comprehend layouts visually)."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "inherits_form_nav_reading",
                    "description": (
                        "Correctly identifies that form interaction, navigation and "
                        "wayfinding, and reading and scrolling ARE inherited from baseline "
                        "(blind users still interact with forms, navigate, and read)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "inherits_touch_pointer",
                    "description": (
                        "Correctly identifies that touch/pointer interaction is inherited "
                        "(mobile screen reader users interact via touch)."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "justifications_grounded",
                    "description": (
                        "Justifications explain WHY (e.g., 'visual scanning is excluded "
                        "because blind users cannot see visual cues') rather than just "
                        "restating whether included/excluded."
                    ),
                    "weight": 1.0,
                },
            ]
        ),
    )
