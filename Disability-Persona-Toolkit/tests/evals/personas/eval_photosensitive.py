"""Eval: photosensitive persona (clause 4.2.9) — STUB.

One sub-test verifying the model handles stub persona content appropriately:

- Stub acknowledgement (refuses fabrication, defers to limitations)

Stub personas have minimal elaboration and should NOT be treated as if they have
detailed AT categories, exploration strategies, or variant definitions. Run with:

    python -m tests.evals tests/evals/personas/eval_photosensitive.py

Use `--persona_context_mode all` to load the same stub task with all
elaborated personas in background context, while still grading the
target photosensitive stub response.
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_eval_persona_context
from tests.evals._scorers import rubric_scorer

PERSONA_ALIAS = "photosensitive"
PERSONA = load_eval_persona_context(PERSONA_ALIAS)


def _solver():
    return [system_message(PERSONA), generate(**_providers.generation_config())]


@task
def stub_acknowledgement() -> Task:
    return Task(
        name="photosensitive_stub_acknowledgement",
        dataset=[
            Sample(
                input=(
                    "List the assistive technologies, exploration strategies, "
                    "and user variants for this persona."
                ),
            )
        ],
        solver=_solver(),
        scorer=rubric_scorer([
                {
                    "id": "declines_fabrication",
                    "description": (
                        "Does not fabricate or invent detailed assistive technologies, "
                        "exploration strategies, or user variants beyond what the stub "
                        "persona file contains."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "stays_within_clause_scope",
                    "description": (
                        "Stays within the high-level scope of clause 4.2.9 (photosensitive "
                        "seizure triggers) without over-elaborating into invented "
                        "categories."
                    ),
                    "weight": 1.0,
                },
            ])
    )
