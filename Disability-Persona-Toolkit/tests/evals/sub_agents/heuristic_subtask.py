"""Per-heuristic sub-agent task factory.

Builds a single inspect-ai ``Task`` for one Nielsen heuristic with a
focused system prompt (index + that heuristic + the persona). The
orchestrator dispatches one of these per heuristic in scope.

Each sub-task asks the same question ("walk through the artifact for
heuristic <N> from the persona's perspective"); the model's job is to
ground its answer in the focused KB it has been given. The split
layout guarantees the model only ever sees the heuristic it owns plus
the supplementary concerns from the index.
"""

from __future__ import annotations

from inspect_ai import Task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from .. import _providers
from .._scorers import rubric_scorer
from ._loaders import build_focused_system


def build_heuristic_subtask(
    *,
    heuristic_number: int,
    persona_alias: str,
    artifact_description: str,
) -> Task:
    """Create a per-heuristic evaluation sub-task.

    Args:
        heuristic_number: 1..10. Selects which heuristic file the
            sub-agent will see.
        persona_alias: Persona alias (e.g. ``"low-vision"``) the
            sub-agent evaluates from.
        artifact_description: Plain-text description of the UI
            artifact under evaluation. Kept short — the sub-agent is
            not expected to reason about the artifact in detail, only
            to apply the heuristic lens to it.
    """
    system = build_focused_system(
        heuristic_number=heuristic_number,
        persona_alias=persona_alias,
    )

    user_prompt = (
        f"Artifact under evaluation:\n\n{artifact_description}\n\n"
        f"Apply Heuristic {heuristic_number} to this artifact from the "
        f"perspective of the {persona_alias!r} persona. If the heuristic "
        f"raises a concern for this persona, describe the concern, its "
        f"severity (0-4), and what would mitigate it. If not, say so "
        f"explicitly. Use ONLY the heuristic you have been given; do not "
        f"speculate about other heuristics."
    )

    return Task(
        name=f"heuristic_{heuristic_number}_{persona_alias}_subtask",
        dataset=[Sample(input=user_prompt)],
        solver=[
            system_message(system),
            generate(**_providers.generation_config()),
        ],
        scorer=rubric_scorer(
            [
                {
                    "id": "applies_correct_heuristic",
                    "description": (
                        f"The answer applies Heuristic {heuristic_number} "
                        f"specifically — not a different heuristic. The "
                        f"sub-agent contract is that it owns this one "
                        f"heuristic only."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "applies_persona_lens",
                    "description": (
                        f"The answer applies the {persona_alias!r} "
                        f"persona's lens (referring to that persona's "
                        f"assistive technology, exploration strategy, or "
                        f"variant), not a generic accessibility lens."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "stays_in_scope",
                    "description": (
                        "The answer does NOT pull in other Nielsen "
                        "heuristics by number or name. If the model wants "
                        "to reference a different heuristic it should say "
                        "'this would also concern the orchestrator' "
                        "rather than improvising."
                    ),
                },
                {
                    "id": "grounded_in_artifact",
                    "description": (
                        "The answer cites specifics from the artifact "
                        "description rather than improvising details that "
                        "were not provided."
                    ),
                },
            ]
        ),
    )
