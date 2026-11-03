"""Eval: color-blind persona (clause 4.2.3).

Five sub-tests verifying the persona file transfers SME knowledge:

- AT recall
- Exploration strategy recall
- User variant recall
- Heuristic lens override application
- Baseline inheritance awareness

Each sub-test is a separate `@task` so it has its own rubric. Run with:

    python -m tests.evals tests/evals/personas/eval_color_blind.py

Use `--persona_context_mode all` to run the same tasks with all
elaborated personas loaded in background context, while still grading
color-blind answers.

Add `-T` to limit to one sub-test, e.g. `--task at_recall`.
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_eval_persona_context
from tests.evals._scorers import rubric_scorer

PERSONA_ALIAS = "color-blind"
PERSONA = load_eval_persona_context(PERSONA_ALIAS)


def _solver():
    return [system_message(PERSONA), generate(**_providers.generation_config())]


@task
def at_recall() -> Task:
    return Task(
        name="color_blind_at_recall",
        dataset=[
            Sample(
                input=(
                    "Identify the assistive technology category(ies) this persona uses. "
                    "For each, give a one-sentence interaction model and name at least "
                    "two concrete tools or filter modes, distinguished by platform or "
                    "deficiency type where relevant. Make each tool's interaction model "
                    "distinct (not just a list of names)."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "covers_colour_filters",
                    "description": (
                        "Mentions colour filter or colour correction tools "
                        "(e.g., Windows Colour Filters, macOS Colour Filters, "
                        "third-party applications) as the primary AT category."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "filter_types_distinct",
                    "description": (
                        "Distinguishes between filter types (e.g., grayscale, "
                        "protanopia/red-blind, deuteranopia/green-blind, "
                        "tritanopia/blue-yellow blind) or platforms (Windows, "
                        "macOS, browser plugins). Naming at least two platforms "
                        "or two filter modes is sufficient to satisfy this criterion."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "filter_interaction_model",
                    "description": (
                        "Explains that colour filters operate by transforming "
                        "colours at the OS or browser level, shifting the palette "
                        "to make distinctions perceivable."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "interaction_models_clear",
                    "description": (
                        "Interactions models are distinct and meaningful (not just "
                        "a list of filter names), highlighting how the filters "
                        "affect the user's visual experience."
                    ),
                    "weight": 1.5,
                },
            ]
        ),
    )


@task
def strategy_recall() -> Task:
    return Task(
        name="color_blind_strategy_recall",
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
                    "id": "scanning_non_colour_cues",
                    "description": (
                        "Includes scanning for non-colour cues: shape, pattern, "
                        "icons, text labels, borders, or positioning that convey "
                        "information independent of colour."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "seeking_explicit_labels",
                    "description": (
                        "Includes seeking explicit text labels and legends that "
                        "unambiguously identify meaning without relying on colour "
                        "coding alone."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "affordance_identification",
                    "description": (
                        "Includes identifying interactive elements by shape and "
                        "affordance (button style, link styling, etc.) rather than "
                        "colour alone."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "state_interpretation_without_colour",
                    "description": (
                        "Includes interpreting state changes and feedback using "
                        "alternative cues (underlines, icons, text, borders) when "
                        "colour-only feedback is unavailable."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "excludes_baseline_only",
                    "description": (
                        "Lists strategies specific to colour-blindness. Baseline "
                        "visual/pointer/reading strategies may be referenced but "
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
        name="color_blind_variant_recall",
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
                    "id": "achromatopsia_variant",
                    "description": (
                        "Includes an achromatopsia (complete colour blindness / "
                        "monochromacy) variant where NO colour information is "
                        "perceivable."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "protanopia_deuteranopia_variant",
                    "description": (
                        "Includes a red-blind (protanopia) or green-blind "
                        "(deuteranopia) variant; notes how red/green distinctions "
                        "are affected."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "tritanopia_variant",
                    "description": (
                        "Includes a blue-yellow blind (tritanopia) variant, "
                        "distinguishing it from red-green colour blindness."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "differentiation_clear",
                    "description": (
                        "Each variant's differentiator is concrete (specific colour "
                        "blindness type) and distinguishes which colours/contrasts "
                        "are affected, not just variant names."
                    ),
                    "weight": 1.5,
                },
            ]
        ),
    )


@task
def lens_override_h1() -> Task:
    return Task(
        name="color_blind_lens_override_h1",
        dataset=[
            Sample(
                input=(
                    "How does Heuristic 1 (Visibility of System Status) "
                    "apply specifically to a colour-blind user? Focus on what "
                    "this persona's lens override adds beyond the generic "
                    "accessibility lens — colour independence, non-colour cues, "
                    "and similar concerns."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "colour_independence",
                    "description": (
                        "Notes that status indicators must not rely solely on "
                        "colour to convey meaning; alternative cues (icons, labels, "
                        "patterns, borders) are essential."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "contrast_sufficiency",
                    "description": (
                        "Ideally addresses that status elements should have sufficient "
                        "luminance contrast even when colour cues are ineffective, but "
                        "this may be partially addressed or implied through discussion of "
                        "non-colour alternatives."
                    ),
                    "weight": 1.0,
                },
                {
                    "id": "text_and_labels",
                    "description": (
                        "Emphasizes that text labels or explicit descriptions "
                        "unambiguously convey status (e.g., 'error: invalid email')."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "filter_robustness",
                    "description": (
                        "Ideally considers how status signals appear under colour filters, "
                        "but awareness of OS colour filters is optional; primary focus is on "
                        "non-colour alternatives and contrast."
                    ),
                    "weight": 0.5,
                },
                {
                    "id": "persona_specific",
                    "description": (
                        "The answer is specific to colour-blindness concerns and "
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
        name="color_blind_baseline_inheritance",
        dataset=[
            Sample(
                input=(
                    "The universal baseline defines six exploration strategies: "
                    "Visual scanning and layout comprehension, Mouse / pointer "
                    "interaction, Reading and scrolling, Form interaction, "
                    "Navigation and wayfinding, Touch / pointer interaction. "
                    "For each, state whether THIS persona inherits it using the "
                    "binary labels Inherited or Excluded — do not introduce any "
                    "third state. In one sentence, justify why a colour-blind user "
                    "can (or cannot) still use it; if the strategy is inherited "
                    "but has colour-related friction, mention that in the "
                    "justification rather than changing the label. Do not "
                    "introduce strategies outside this list."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "all_strategies_apply",
                    "description": (
                        "States that colour-blind users inherit ALL baseline "
                        "strategies: visual scanning, mouse/pointer interaction, "
                        "reading and scrolling, form interaction, navigation and "
                        "wayfinding, touch/pointer interaction."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "no_false_exclusions",
                    "description": (
                        "Does NOT incorrectly exclude visual scanning or pointer "
                        "interaction (colour-blind users CAN see and interact "
                        "normally; they just perceive colours differently)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "justifications_grounded",
                    "description": (
                        "Justifications reference how colour-blind users STILL "
                        "use these strategies (e.g., 'visual scanning still applies; "
                        "they scan using non-colour cues'), not generic descriptions."
                    ),
                    "weight": 1.0,
                },
            ]
        ),
    )
