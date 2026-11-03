"""Smoke test: minimal eval that proves the harness is wired up.

Run with:

    inspect eval tests/evals/smoke.py --model copilot/gpt-5-mini
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_persona_by_alias
from tests.evals._scorers import must_mention


@task
def smoke() -> Task:
    persona = load_persona_by_alias("blind")
    return Task(
        dataset=[
            Sample(
                input=(
                    "Name the primary assistive technology category used by "
                    "this persona. Reply in one short sentence."
                ),
                target="screen reader",
            )
        ],
        solver=[
            system_message(persona),
            generate(**_providers.generation_config()),
        ],
        scorer=must_mention(["screen reader"]),
    )
