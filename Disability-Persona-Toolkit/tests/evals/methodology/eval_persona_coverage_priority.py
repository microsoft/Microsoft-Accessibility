"""Two scenarios:

- A "trigger" case where the methodology should fire — a proposed
  persona evaluation order for a video-conferencing UI is in a
  generic vision-first order that mis-prioritizes for the UI's
  audio-centric interaction model. The correct response is to
  REORDER, placing Deaf and Hard of hearing at the top.

- A "no-trigger" case where the principle should NOT fire — a
  proposed persona evaluation order for a checkout form already
  matches the KB's task-contextual divergence logic. The correct
  response is to KEEP it.

Run with:

    inspect eval tests/evals/methodology/eval_persona_coverage_priority.py \
        --model copilot/gpt-5-mini
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_methodology
from tests.evals._scorers import rubric_scorer

PERSONA_COVERAGE_PRIORITY = load_methodology("persona-coverage-priority")
SYSTEM = (
    "You are an accessibility evaluation lead planning which personas "
    "to evaluate for a specific UI when full persona coverage is not "
    "practical. Apply the following principle exactly:\n\n"
    f"{PERSONA_COVERAGE_PRIORITY}\n\n"
    "When asked to review a proposed persona evaluation order for a "
    "specific UI, decide whether to KEEP the proposed order or "
    "REORDER it. If REORDER, give the corrected priority order and "
    "justify it by reference to the principle. Be precise about "
    "task-contextual interaction-model divergence from baseline, "
    "barrier frequency for the UI type, and coverage breadth. Do not "
    "defend a static or generic ordering when the UI context warrants "
    "a different priority."
)


@task
def persona_coverage_priority_triggers() -> Task:
    """The principle SHOULD fire — the proposed order is a generic
    vision-first default that mis-prioritizes for an audio-centric UI."""
    return Task(
        name="persona_coverage_priority_triggers",
        dataset=[
            Sample(
                input=(
                    "Proposed persona evaluation plan to review:\n\n"
                    "  UI under evaluation: A real-time video meeting "
                    "web application. Core functionality includes live "
                    "audio/video calls, screen sharing, in-meeting "
                    "chat, reactions, hand-raise, mute/camera toggles, "
                    "and a participants panel with per-participant "
                    "actions revealed on hover.\n"
                    "  Constraint: Time only allows evaluating four of "
                    "the seven personas listed.\n"
                    "  Proposed order (evaluate top-down until time "
                    "runs out):\n"
                    "    1. Blind (screen reader)\n"
                    "    2. Low vision\n"
                    "    3. Colorblind\n"
                    "    4. Keyboard-only\n"
                    "    5. Deaf\n"
                    "    6. Hard of hearing\n"
                    "    7. Voice access\n"
                    "  Rationale given by the plan author: 'We always "
                    "start with vision personas because screen reader "
                    "issues are the most common accessibility "
                    "findings.'\n\n"
                    "Should this order be KEPT or REORDERED? Apply the "
                    "persona-coverage-priority principle. If REORDER, "
                    "give the corrected order and explain."
                ),
            )
        ],
        solver=[
            system_message(SYSTEM),
            generate(**_providers.generation_config()),
        ],
        scorer=rubric_scorer(
            [
                {
                    "id": "decides_reorder",
                    "description": (
                        "Concludes the proposed order should be "
                        "REORDERED — NOT kept as-is and NOT defended "
                        "as an acceptable static ordering."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "prioritizes_deaf_and_hoh",
                    "description": (
                        "Places Deaf AND Hard of hearing at or near "
                        "the top of the revised order (within the "
                        "first three positions), recognizing that "
                        "audio is the core communication channel of a "
                        "video meeting."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "cites_task_contextual_divergence",
                    "description": (
                        "Explicitly justifies the reorder in terms of "
                        "task-contextual interaction-model divergence "
                        "from the baseline user (or equivalent "
                        "paraphrase from the principle), not just "
                        "'audio matters' or 'deaf users need "
                        "captions'."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "demotes_low_divergence_personas",
                    "description": (
                        "Moves Colorblind (and ideally the broader "
                        "vision tier where divergence on the core "
                        "meeting function is low) lower in the "
                        "revised order than at least one audio or "
                        "motor persona."
                    ),
                },
                {
                    "id": "no_static_ordering",
                    "description": (
                        "Does NOT endorse the plan author's rationale "
                        "that vision personas should always come "
                        "first, and does NOT defend any fixed / "
                        "alphabetical / by-clause-number ordering "
                        "scheme."
                    ),
                },
            ]
        ),
    )


@task
def persona_coverage_priority_does_not_trigger() -> Task:
    """The principle should NOT fire — the proposed order already
    matches the KB's task-contextual divergence logic for this UI."""
    return Task(
        name="persona_coverage_priority_does_not_trigger",
        dataset=[
            Sample(
                input=(
                    "Proposed persona evaluation plan to review:\n\n"
                    "  UI under evaluation: A multi-step checkout "
                    "form. Each step has labeled text inputs, "
                    "required-field markers, and inline validation. "
                    "Validation errors are shown with a red warning "
                    "icon AND a descriptive text message next to the "
                    "field (the color is never the sole signal). The "
                    "final step is a 'Place order' submit button.\n"
                    "  Constraint: Time only allows evaluating four "
                    "personas.\n"
                    "  Proposed order (evaluate top-down):\n"
                    "    1. Keyboard-only\n"
                    "    2. Voice access\n"
                    "    3. Low vision\n"
                    "    4. Colorblind\n"
                    "  Rationale given by the plan author: 'Form "
                    "interaction is heavily Tab-driven and "
                    "label-driven, so keyboard-only and voice access "
                    "have the highest divergence here. Magnification "
                    "affects label/field spatial association so low "
                    "vision is moderate. Colorblind divergence is low "
                    "for this form because every validation message "
                    "pairs the color with an icon and text.'\n\n"
                    "Should this order be KEPT or REORDERED? Apply "
                    "the persona-coverage-priority principle."
                ),
            )
        ],
        solver=[
            system_message(SYSTEM),
            generate(**_providers.generation_config()),
        ],
        scorer=rubric_scorer(
            [
                {
                    "id": "decides_keep",
                    "description": (
                        "Concludes the proposed order should be KEPT "
                        "— the existing prioritization already matches "
                        "task-contextual divergence for this UI."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "justifies_keyboard_and_voice_top",
                    "description": (
                        "Explains why Keyboard-only and Voice access "
                        "are correctly at the top for this UI — high "
                        "task-contextual divergence on form "
                        "interaction (Tab order, focus, label-based "
                        "targeting)."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "justifies_colorblind_low",
                    "description": (
                        "Explains why Colorblind is correctly "
                        "low-priority for this specific form — "
                        "validation pairs color with an icon and "
                        "descriptive text, so color is not the sole "
                        "signal and divergence is low."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "principle_understood",
                    "description": (
                        "Demonstrates understanding that the principle "
                        "is about matching priority to UI-specific "
                        "divergence, NOT about always reshuffling a "
                        "presented order or always promoting "
                        "screen-reader / vision personas to the top."
                    ),
                },
                {
                    "id": "no_invented_reorder",
                    "description": (
                        "Does NOT fabricate a reorder when the "
                        "proposed order is already aligned with the "
                        "KB's logic — e.g. does not arbitrarily swap "
                        "Low vision above Voice access, or promote "
                        "Colorblind."
                    ),
                },
            ]
        ),
    )
