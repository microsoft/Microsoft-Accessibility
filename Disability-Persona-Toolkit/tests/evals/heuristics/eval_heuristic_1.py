"""Pilot eval: Heuristic 1 (Visibility of System Status) and severity scale.

Two tasks:

- `heuristic_1_lens_low_vision` — given the heuristics index + the H1
  per-heuristic file + low-vision persona, produce the persona-specific
  lens for Heuristic 1 and identify a likely violation. Loads only the
  index + H1 (~5 KB) instead of the full 15 KB aggregate to demonstrate
  the focused-loading pattern.

- `severity_assignment` — given severity.md, assign 0–4 severity to two
  scenarios with known baseline ratings.

Run with:

    inspect eval tests/evals/heuristics/eval_heuristic_1.py \
        --model copilot/gpt-5-mini
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import (
    load_heuristic,
    load_heuristic_index,
    load_persona_by_alias,
    load_required_persona_safeguards,
    load_severity,
)
from tests.evals._scorers import rubric_scorer

# Focused load: index (supplementary concerns + Nielsen menu) + just H1.
HEURISTIC_INDEX = load_heuristic_index()
HEURISTIC_1 = load_heuristic(1)
LOW_VISION = load_persona_by_alias("low-vision")
SEVERITY = load_severity()
REQUIRED_PERSONA_SAFEGUARDS = load_required_persona_safeguards()


@task
def heuristic_1_lens_low_vision() -> Task:
    system = (
        f"{REQUIRED_PERSONA_SAFEGUARDS}\n\n"
        f"# Heuristics index\n\n{HEURISTIC_INDEX}\n\n"
        f"# Heuristic 1 detail\n\n{HEURISTIC_1}\n\n"
        f"# Persona reference\n\n{LOW_VISION}"
    )
    return Task(
        name="heuristic_1_lens_low_vision",
        dataset=[
            Sample(
                input=(
                    "Apply Heuristic 1 (Visibility of System Status) to a "
                    "low-vision user. Then describe one concrete UI pattern "
                    "that would VIOLATE this heuristic for that persona, "
                    "explaining why it would fail."
                ),
            )
        ],
        solver=[
            system_message(system),
            generate(**_providers.generation_config()),
        ],
        scorer=rubric_scorer(
            [
                {
                    "id": "states_generic_lens",
                    "description": (
                        "States the generic accessibility lens for "
                        "Heuristic 1 — that AT users need system state "
                        "surfaced through the channel they rely on, not "
                        "only visual feedback."
                    ),
                    "weight": 0.75,
                },
                {
                    "id": "applies_persona_lens",
                    "description": (
                        "Applies the low-vision lens override: feedback "
                        "must be perceivable WITHIN the magnified viewport "
                        "and survive forced-colours mode (not rely solely "
                        "on stripped colour cues)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "concrete_violation",
                    "description": (
                        "Describes a concrete violating UI pattern that "
                        "would specifically fail for a low-vision user "
                        "(e.g. 'success toast appears top-right while "
                        "user's magnified viewport is on a button bottom-"
                        "left')."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "violation_grounded_in_persona",
                    "description": (
                        "Explains why the violation harms the persona "
                        "specifically — referencing magnifier viewport "
                        "size, panning cost, or forced-colours stripping."
                    ),
                },
                {
                    "id": "no_unrelated_personas",
                    "description": (
                        "Does NOT centre the answer on personas this "
                        "question is not about (blind, keyboard-only) "
                        "except as brief contrast."
                    ),
                    "weight": 1.5,
                },
            ]
        ),
    )


@task
def severity_assignment() -> Task:
    system = f"# Severity reference\n\n{SEVERITY}"

    return Task(
        name="severity_assignment",
        dataset=[
            Sample(
                input=(
                    "Persona: keyboard-only user.\n"
                    "Issue: A modal dialog cannot be closed using any "
                    "keyboard input (no Escape, no focusable close button, "
                    "focus is trapped inside). The user encounters this on "
                    "every save action in the primary workflow.\n\n"
                    "Assign a severity (0–4) using the severity scale in "
                    "your reference. Then justify the rating using the "
                    "frequency / impact / persistence / learnability "
                    "dimensions."
                ),
                metadata={"expected_severity": 0, "label": "keyboard_trap_modal"},
            ),
            Sample(
                input=(
                    "Persona: low-vision user (browser zoom 200%).\n"
                    "Issue: A footer copyright notice has 3.5:1 contrast "
                    "instead of the AA-recommended 4.5:1. The user sees "
                    "this once per page visit; the content is non-essential "
                    "and is also available in the site's About page at "
                    "AAA contrast.\n\n"
                    "Assign a severity (0–4) and justify using the "
                    "frequency / impact / persistence / learnability "
                    "dimensions."
                ),
                metadata={
                    "expected_severity_range": [3, 4],
                    "label": "low_contrast_footer",
                },
            ),
        ],
        solver=[
            system_message(system),
            generate(**_providers.generation_config()),
        ],
        scorer=rubric_scorer(
            [
                {
                    "id": "rating_within_expected",
                    "description": (
                        "The numeric severity matches the expected rating "
                        "in the sample metadata. For sample "
                        "'keyboard_trap_modal' the expected severity is 0 "
                        "(Critical); for 'low_contrast_footer' a rating of "
                        "3 or 4 (Low or Trivial) is acceptable. A different "
                        "rating fails this criterion regardless of "
                        "justification quality."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "uses_all_four_dimensions",
                    "description": (
                        "Justification explicitly addresses all four "
                        "dimensions: frequency, impact, persistence, AND "
                        "learnability."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "justification_grounded",
                    "description": (
                        "Justifications cite concrete details from the "
                        "scenario (e.g. 'every save action' for frequency, "
                        "'no Escape, focus trapped' for impact) rather "
                        "than generic descriptions."
                    ),
                    "weight": 1.25,
                },
                {
                    "id": "mitigation_consideration",
                    "description": (
                        "For the footer scenario, the answer considers the "
                        "available mitigation (AAA-contrast version on the "
                        "About page) per the severity scale's "
                        "mitigation-aware guidance."
                    ),
                },
            ]
        ),
    )
