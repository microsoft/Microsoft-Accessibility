"""Pilot eval: low-vision persona (clause 4.2.2).

Five sub-tests verifying the persona file transfers SME knowledge:

- AT recall
- Exploration strategy recall
- User variant recall
- Heuristic lens override application
- Baseline inheritance awareness

Each sub-test is a separate `@task` so it has its own rubric. Run with:

    python -m tests.evals tests/evals/personas/eval_low_vision.py

Use `--persona_context_mode all` to run the same tasks with all
elaborated personas loaded in background context, while still grading
low-vision answers.

Add `-T` to limit to one sub-test, e.g. `--task at_recall`.
"""

from __future__ import annotations

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessageUser, ContentImage, ContentText
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_eval_persona_context
from tests.evals._scorers import rubric_scorer

PERSONA_ALIAS = "low-vision"
PERSONA = load_eval_persona_context(PERSONA_ALIAS)
COMBOBOX_IMAGE = (
    Path(__file__).resolve().parents[2]
    / "fixtures"
    / "images"
    / "combobox.png"
)


def _solver():
    return [system_message(PERSONA), generate(**_providers.generation_config())]


def _combobox_image_prompt() -> list[ChatMessageUser]:
    return [
        ChatMessageUser(
            content=[
                ContentText(
                    text=(
                        "You are evaluating the attached synthetic service-selection screenshot from a low-vision "
                        "persona perspective (EN 301 549 FPS 4.2.2).\n\n"
                        "Task:\n"
                        "1) Give an accessibility evaluation based only on visible evidence "
                        "in the screenshot.\n"
                        "2) Call out likely low-vision risks and likely strengths.\n"
                        "3) Separate confirmed observations from items that still require "
                        "interaction/tree checks.\n"
                        "4) Provide concrete remediation suggestions for the highest-impact "
                        "issues.\n"
                        "\nKeep the response concise but specific to what is visible."
                    )
                ),
                ContentImage(image=str(COMBOBOX_IMAGE), detail="low"),
            ]
        )
    ]


@task
def at_recall() -> Task:
    return Task(
        name="low_vision_at_recall",
        dataset=[
            Sample(
                input=(
                    "Identify all assistive technology categories this persona uses. "
                    "For each, give a one-sentence interaction model that meaningfully "
                    "distinguishes it from the others, and name at least one concrete "
                    "example tool."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "covers_browser_zoom",
                    "description": (
                        "Mentions browser zoom AND notes that it triggers "
                        "content reflow / responsive breakpoints."
                    ),
                },
                {
                    "id": "covers_screen_magnifier_no_reflow",
                    "description": (
                        "Mentions a screen magnifier (ZoomText, Windows "
                        "Magnifier, or macOS Zoom) AND notes that it does "
                        "NOT trigger reflow — it magnifies the rendered "
                        "layout, requiring panning."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "covers_dpi_scaling",
                    "description": (
                        "Mentions OS-level text size or DPI / display scaling "
                        "as distinct from browser zoom."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "covers_high_contrast",
                    "description": (
                        "Mentions Windows High Contrast Mode or "
                        "forced-colours as a distinct AT category."
                    ),
                },
                {
                    "id": "covers_dual_channel",
                    "description": (
                        "Mentions a combined magnification + screen reader "
                        "configuration (e.g. Fusion / ZoomText + JAWS) as a "
                        "dual-channel AT setup."
                    ),
                    "weight": 0.5,
                },
                {
                    "id": "interaction_models_distinct",
                    "description": (
                        "Each AT entry has an interaction model that "
                        "meaningfully distinguishes it (not just renaming) — "
                        "e.g. reflow vs. panning, OS-wide vs. browser-only."
                    ),
                    "weight": 1.5,
                },
            ]
        ),
    )


@task
def strategy_recall() -> Task:
    return Task(
        name="low_vision_strategy_recall",
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
                    "id": "zoomed_reading_reflow",
                    "description": (
                        "Includes 'Zoomed reading and text reflow' (or "
                        "equivalent) — increasing browser zoom and relying "
                        "on reflow."
                    ),
                },
                {
                    "id": "magnified_viewport_panning",
                    "description": (
                        "Includes magnified-viewport panning — moving a "
                        "small magnified viewport across the rendered "
                        "layout."
                    ),
                },
                {
                    "id": "focus_cursor_tracking",
                    "description": (
                        "Includes focus / cursor tracking as a strategy — "
                        "the magnifier following keyboard focus or pointer."
                    ),
                },
                {
                    "id": "high_contrast_scanning",
                    "description": (
                        "Includes scanning under high contrast / forced-"
                        "colours as a strategy."
                    ),
                },
                {
                    "id": "dual_channel_reading",
                    "description": (
                        "Includes dual-channel reading (magnification + "
                        "speech) as a strategy."
                    ),
                },
                {
                    "id": "excludes_baseline_only",
                    "description": (
                        "Lists strategies that are persona-specific. Strategies "
                        "marked as baseline (visual scanning, mouse / pointer "
                        "interaction, reading and scrolling, form interaction, "
                        "navigation and wayfinding, touch / pointer "
                        "interaction) may be acknowledged as inherited but "
                        "should not dominate the list."
                    ),
                    "weight": 0.5,
                },
            ]
        ),
    )


@task
def variant_recall() -> Task:
    return Task(
        name="low_vision_variant_recall",
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
                    "id": "moderate_zoom_variant",
                    "description": (
                        "Includes a variant covering increased text size / "
                        "moderate browser zoom (relies on reflow, no "
                        "magnifier)."
                    ),
                },
                {
                    "id": "screen_magnifier_variant",
                    "description": (
                        "Includes a screen magnifier variant operating at "
                        "high magnification (e.g. 3×–8×) with a small "
                        "viewport requiring panning."
                    ),
                },
                {
                    "id": "high_contrast_variant",
                    "description": (
                        "Includes a contrast-sensitivity variant relying on "
                        "high contrast / forced-colours themes."
                    ),
                },
                {
                    "id": "dual_channel_variant",
                    "description": (
                        "Includes a dual-channel variant combining "
                        "magnification with a screen reader."
                    ),
                },
                {
                    "id": "differentiation_clear",
                    "description": (
                        "Each variant's differentiator is concrete and "
                        "actionable (e.g. specific zoom level, specific AT "
                        "combination), not just renaming the persona."
                    ),
                },
            ]
        ),
    )


@task
def lens_override_h1() -> Task:
    return Task(
        name="low_vision_lens_override_h1",
        dataset=[
            Sample(
                input=(
                    "How does Heuristic 1 (Visibility of System Status) "
                    "apply specifically to a low-vision user? Focus on what "
                    "this persona's lens override adds beyond the generic "
                    "accessibility lens — magnified viewport, forced-"
                    "colours, off-screen feedback, and similar concerns."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "viewport_locality",
                    "description": (
                        "Notes that status feedback must appear within (or "
                        "be brought into) the magnified viewport — distant "
                        "feedback may never be seen."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "forced_colours_status",
                    "description": (
                        "Notes that status indicators (progress bars, "
                        "spinners) must remain visible in forced-colours / "
                        "high-contrast mode."
                    ),
                },
                {
                    "id": "audio_supplement",
                    "description": (
                        "Suggests an audio / earcon channel that supplements "
                        "visual cues users may miss."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "focus_tracking",
                    "description": (
                        "Mentions magnifier focus tracking — bringing the "
                        "user to feedback near the activated control."
                    ),
                },
                {
                    "id": "persona_specific",
                    "description": (
                        "The answer is specific to low-vision concerns and "
                        "does not just restate the generic Heuristic 1 "
                        "accessibility lens unchanged."
                    ),
                    "weight": 2.0,
                },
            ]
        ),
    )


@task
def baseline_inheritance() -> Task:
    return Task(
        name="low_vision_baseline_inheritance",
        dataset=[
            Sample(
                input=(
                    "The universal baseline defines six exploration strategies: "
                    "Visual scanning and layout comprehension, Mouse / pointer "
                    "interaction, Reading and scrolling, Form interaction, "
                    "Navigation and wayfinding, Touch / pointer interaction. "
                    "For each, state whether THIS persona inherits it and "
                    "justify in one sentence why a low-vision user can "
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
                        "States that the low-vision persona has NO baseline "
                        "exclusions — visual scanning, mouse / pointer "
                        "interaction, reading and scrolling, form "
                        "interaction, navigation and wayfinding, and touch "
                        "/ pointer interaction all apply."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "no_false_exclusions",
                    "description": (
                        "Does NOT incorrectly claim mouse/pointer or visual "
                        "scanning is excluded for low-vision users (those "
                        "are excluded for blind / keyboard-only personas, "
                        "not low-vision)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "justifications_grounded",
                    "description": (
                        "Justifications reference how a low-vision user "
                        "STILL uses these strategies (e.g. visual scanning "
                        "with magnification), not generic descriptions of "
                        "the strategies themselves."
                    ),
                },
            ]
        ),
    )


@task
def image_combobox_review() -> Task:
    return Task(
        name="low_vision_image_combobox_review",
        dataset=[
            Sample(
                input=_combobox_image_prompt(),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "grounded_visual_evidence",
                    "description": (
                        "Grounds the evaluation in visible screenshot details "
                        "(e.g. small combobox trigger text, compact dropdown "
                        "options, layout density, or contrast-dependent cues), "
                        "rather than generic accessibility advice."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "applies_low_vision_lens",
                    "description": (
                        "Applies low-vision specific reasoning such as zoom/reflow "
                        "readability, magnified viewport scanning effort, target "
                        "discernibility, or forced-colours robustness."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "balanced_strengths_and_risks",
                    "description": (
                        "Includes at least one likely strength and at least one "
                        "likely risk in the screenshot, instead of only one-sided "
                        "criticism."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "confidence_gated_claims",
                    "description": (
                        "Distinguishes confirmed visual observations from items that "
                        "cannot be proven from a static screenshot alone (e.g. keyboard "
                        "flow, focus movement, accessibility tree semantics)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "actionable_remediation",
                    "description": (
                        "Provides concrete remediation steps for highest-impact low-vision "
                        "issues (for example larger control text, stronger contrast, clearer "
                        "focus styling, spacing improvements)."
                    ),
                    "weight": 1.5,
                },
            ]
        ),
    )
