"""Regression tests for required methodology in persona evaluation prompts."""

from __future__ import annotations

import pytest

from tests.evals import _context
from tests.evals.heuristics.eval_heuristic_1 import REQUIRED_PERSONA_SAFEGUARDS
from tests.evals.heuristics.eval_heuristics_lens import _build_cell_context
from tests.evals.sub_agents.heuristic_subtask import build_heuristic_subtask

REQUIRED_METHODOLOGY = (
    "licensing",
    "responsible-persona-use",
    "persona-interpretation",
)


def _assert_required_methodology(prompt: str) -> None:
    for name in REQUIRED_METHODOLOGY:
        assert f"methodology/{name}.md" in prompt
        assert _context.load_methodology(name) in prompt


@pytest.mark.parametrize("mode", ("single", "all-personas", "medium"))
def test_persona_context_modes_include_required_methodology(mode):
    previous_mode = _context.get_eval_persona_context_mode()
    try:
        _context.set_eval_persona_context_mode(mode)
        prompt = _context.load_eval_persona_context("low-vision")
    finally:
        _context.set_eval_persona_context_mode(previous_mode)

    _assert_required_methodology(prompt)


def test_focused_heuristic_context_includes_required_methodology():
    _assert_required_methodology(_build_cell_context("low-vision", 1))
    _assert_required_methodology(REQUIRED_PERSONA_SAFEGUARDS)


def test_sub_agent_system_prompt_includes_required_methodology():
    task = build_heuristic_subtask(
        heuristic_number=1,
        persona_alias="low-vision",
        artifact_description="A search form with delayed results.",
    )
    system_solver = list(task.solver)[0]
    system_prompt = system_solver.__dict__["__registry_params__"]["template"]

    _assert_required_methodology(system_prompt)
