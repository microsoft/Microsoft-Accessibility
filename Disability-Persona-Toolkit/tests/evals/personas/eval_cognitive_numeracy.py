"""Eval: cognitive-numeracy persona (clause 4.2.10).

Five sub-tests verifying the persona file transfers SME knowledge:

- AT recall
- Exploration strategy recall
- User variant recall
- Heuristic lens override application (Heuristic 5 — Error Prevention)
- Baseline inheritance awareness

Each sub-test is a separate `@task` so it has its own rubric. Run with:

    python -m tests.evals tests/evals/personas/eval_cognitive_numeracy.py

Use `--persona_context_mode all` to run the same tasks with all
elaborated personas loaded in background context, while still grading
cognitive-numeracy answers.
"""

# NOTE: This eval grades responses against the cognitive-numeracy persona, which
# adapts W3C COGA material. See personas/cognitive-sources.LICENSE.md for attribution.

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_eval_persona_context
from tests.evals._scorers import rubric_scorer

PERSONA_ALIAS = "cognitive-numeracy"
PERSONA = load_eval_persona_context(PERSONA_ALIAS)


def _solver():
    return [system_message(PERSONA), generate(**_providers.generation_config())]


@task
def at_recall() -> Task:
    return Task(
        name="cognitive_numeracy_at_recall",
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
                    "id": "covers_calculator_conversion",
                    "description": (
                        "Mentions calculators and unit / currency conversion tools "
                        "used to offload arithmetic and conversions."
                    ),
                    "weight": 1.25,
                },
                {
                    "id": "covers_tts_numbers",
                    "description": (
                        "Mentions text-to-speech used to hear numbers, ideally "
                        "noting it often misreads long numbers, codes, or symbols."
                    ),
                },
                {
                    "id": "covers_visual_aids",
                    "description": (
                        "Mentions visual aids — color coding, spacing, larger fonts "
                        "— used to pick out the relevant figure and not lose place."
                    ),
                },
                {
                    "id": "covers_personalization_concepts",
                    "description": (
                        "Mentions personalization semantics that substitute or "
                        "augment numbers with non-numeric concepts (cold/warm/hot, "
                        "small/medium/large)."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "covers_locale_units",
                    "description": (
                        "Mentions reliance on platform locale / unit / currency / "
                        "date defaults to avoid conversions."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "reframes_around_offloading_math",
                    "description": (
                        "Frames the tools around offloading calculation and "
                        "reinforcing figures with non-numeric cues, rather than as "
                        "generic assistive technology."
                    ),
                },
            ]
        ),
    )


@task
def strategy_recall() -> Task:
    return Task(
        name="cognitive_numeracy_strategy_recall",
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
                    "id": "concept_over_number",
                    "description": (
                        "Includes reading the concept behind a number (hot, large, "
                        "almost full) rather than the raw figure."
                    ),
                },
                {
                    "id": "offloading_calculation",
                    "description": (
                        "Includes getting the answer from a tool or expecting the "
                        "system to compute it rather than doing mental arithmetic."
                    ),
                },
                {
                    "id": "magnitude_by_proxy",
                    "description": (
                        "Includes judging relative size / time / price via "
                        "non-numeric proxies (images, 'half way', now-markers, "
                        "relative labels)."
                    ),
                },
                {
                    "id": "verification_double_checking",
                    "description": (
                        "Includes re-checking numbers and relying on summaries and "
                        "warnings because the user cannot tell when a value 'looks "
                        "wrong'."
                    ),
                },
                {
                    "id": "format_unit_normalization",
                    "description": (
                        "Includes sticking to familiar units / formats and relying "
                        "on locale defaults to avoid conversions."
                    ),
                },
                {
                    "id": "excludes_baseline_only",
                    "description": (
                        "Focuses on persona-specific strategies; baseline "
                        "strategies may be acknowledged as inherited but should not "
                        "dominate."
                    ),
                    "weight": 0.5,
                },
            ]
        ),
    )


@task
def variant_recall() -> Task:
    return Task(
        name="cognitive_numeracy_variant_recall",
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
                    "id": "number_calculation_variant",
                    "description": (
                        "Includes a number-and-calculation variant who cannot "
                        "reliably read, compare, or calculate with numbers."
                    ),
                },
                {
                    "id": "quantity_magnitude_variant",
                    "description": (
                        "Includes a quantity-and-magnitude variant who cannot judge "
                        "how much / how big / how far / how expensive."
                    ),
                },
                {
                    "id": "time_sequence_variant",
                    "description": (
                        "Includes a time-and-sequence variant who struggles with "
                        "numeric times, dates, durations, and ordering."
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
def lens_override_h5() -> Task:
    return Task(
        name="cognitive_numeracy_lens_override_h5",
        dataset=[
            Sample(
                input=(
                    "How does Heuristic 5 (Error Prevention) apply specifically to "
                    "a user who has difficulty with numbers, quantities, and "
                    "mathematical concepts? Focus on what this persona's lens "
                    "override adds beyond the generic accessibility lens."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer(
            [
                {
                    "id": "computes_for_user",
                    "description": (
                        "States that the system should compute totals, durations, "
                        "and conversions rather than requiring mental arithmetic."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "warns_unusual_values",
                    "description": (
                        "Notes warning on unusual / extreme quantities or totals "
                        "and showing a summary before commitment, since the user "
                        "cannot tell a value is wrong."
                    ),
                },
                {
                    "id": "forgiving_formats_and_defaults",
                    "description": (
                        "Notes accepting number formats, chunking long numbers, "
                        "defaulting to locale units/dates, preventing impossible "
                        "choices, and not requiring recalled PINs/codes/CVV."
                    ),
                },
                {
                    "id": "persona_specific",
                    "description": (
                        "The answer is specific to numeracy concerns and does not "
                        "just restate the generic Heuristic 5 lens unchanged."
                    ),
                    "weight": 2.0,
                },
            ]
        ),
    )


@task
def baseline_inheritance() -> Task:
    return Task(
        name="cognitive_numeracy_baseline_inheritance",
        dataset=[
            Sample(
                input=(
                    "The universal baseline defines six exploration strategies: "
                    "Visual scanning and layout comprehension, Mouse / pointer "
                    "interaction, Reading and scrolling, Form interaction, "
                    "Navigation and wayfinding, Touch / pointer interaction. For "
                    "each, state whether THIS persona inherits it and justify in "
                    "one sentence why a user with limited numeracy can still use "
                    "it. Do not introduce strategies outside this list."
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
                        "six baseline strategies apply (the user's senses, motor "
                        "control, and language are unaffected)."
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
                        "Justifications reference how a user with limited numeracy "
                        "still uses each strategy (the barrier is specific to "
                        "numbers, not to scanning, reading, or navigating), not "
                        "generic descriptions of the strategies themselves."
                    ),
                },
            ]
        ),
    )
