"""Pilot consistency check: baseline propagation for low-vision persona.

Deterministic — no LLM. Run via pytest:

    pytest tests/evals/consistency/test_baseline_propagation.py

Verifies that every baseline section the persona claims to inherit
(via `*(from baseline)*` markers) actually contains the corresponding
content from `personas/_baseline.md`.

This is a stricter check than `tests/validate_structure.py`: it
compares the persona's inherited body text against the canonical
baseline body, not just the presence of the marker.
"""

from __future__ import annotations

import re

import pytest

from tests.evals._context import extract_section, load_baseline, load_persona_by_alias

PERSONA_ALIAS = "low-vision"


def _split_h3_sections(body: str) -> dict[str, str]:
    """Split a body string by H3 headings, returning {heading: content}.

    Heading names are stripped of trailing markers like *(from baseline)*.
    """
    sections: dict[str, str] = {}
    pattern = re.compile(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", re.MULTILINE | re.DOTALL)
    for match in pattern.finditer(body):
        heading = match.group(1).strip()
        heading = re.sub(r"\s*\*\(from baseline\)\*\s*$", "", heading).strip()
        sections[heading] = match.group(2).strip()
    return sections


def _baseline_strategies() -> dict[str, str]:
    body = extract_section(load_baseline(), "Exploration Strategies", level=2)
    return _split_h3_sections(body)


def _persona_inherited_strategies(alias: str) -> dict[str, str]:
    persona = load_persona_by_alias(alias)
    body = extract_section(persona, "Exploration Strategies", level=2)
    sections: dict[str, str] = {}
    pattern = re.compile(
        r"^### ([^\n]+?)\s*\*\(from baseline\)\*\s*\n(.*?)(?=^### |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for match in pattern.finditer(body):
        sections[match.group(1).strip()] = match.group(2).strip()
    return sections


def _normalise(text: str) -> str:
    """Collapse whitespace differences for tolerant equality checks."""
    return re.sub(r"\s+", " ", text).strip()


@pytest.mark.parametrize(
    "alias",
    [PERSONA_ALIAS],
)
def test_persona_has_baseline_markers(alias: str) -> None:
    inherited = _persona_inherited_strategies(alias)
    assert inherited, (
        f"Persona '{alias}' has no '*(from baseline)*' strategy markers; "
        "either the persona is missing inherited content or the marker "
        "format has drifted."
    )


@pytest.mark.parametrize(
    "alias",
    [PERSONA_ALIAS],
)
def test_inherited_strategies_exist_in_baseline(alias: str) -> None:
    baseline = _baseline_strategies()
    inherited = _persona_inherited_strategies(alias)
    unknown = sorted(set(inherited) - set(baseline))
    assert not unknown, (
        f"Persona '{alias}' claims to inherit baseline strategies that "
        f"are not defined in _baseline.md: {unknown}"
    )


@pytest.mark.parametrize(
    "alias",
    [PERSONA_ALIAS],
)
def test_inherited_content_matches_baseline(alias: str) -> None:
    baseline = _baseline_strategies()
    inherited = _persona_inherited_strategies(alias)
    drift: list[str] = []
    for heading, content in inherited.items():
        baseline_content = baseline.get(heading, "")
        if _normalise(content) != _normalise(baseline_content):
            drift.append(heading)
    assert not drift, (
        f"Persona '{alias}' has baseline-marked strategies whose content "
        f"has drifted from _baseline.md: {drift}. Update the persona to "
        "match the baseline or remove the *(from baseline)* marker."
    )


def test_low_vision_has_no_baseline_exclusions() -> None:
    """The baseline file's Exclusions table lists no exclusions for
    low-vision. Verify the persona honours that — every baseline
    exploration strategy appears in the persona's Exploration
    Strategies section, even if not all are marked as inherited."""
    baseline = _baseline_strategies()
    persona = load_persona_by_alias(PERSONA_ALIAS)
    body = extract_section(persona, "Exploration Strategies", level=2)
    persona_strategies = _split_h3_sections(body)
    missing = sorted(set(baseline) - set(persona_strategies))
    assert not missing, (
        "Low-vision persona is missing baseline exploration strategies "
        f"despite having no exclusions: {missing}"
    )
