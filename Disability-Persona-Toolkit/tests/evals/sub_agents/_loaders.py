"""Focused-loading helpers for per-heuristic sub-agents.

These wrap ``_context`` loaders so a sub-agent only ever pays for the
required persona safeguards, heuristics index, the one heuristic file
it owns, and its persona, never the full 15 KB heuristic aggregate.
The point of the split layout is realised here.
"""

from __future__ import annotations

from .._context import (
    HEURISTIC_FILES,
    load_heuristic,
    load_heuristic_index,
    load_persona_by_alias,
    load_required_persona_safeguards,
)


def heuristic_count() -> int:
    """Number of Nielsen heuristics available."""
    return len(HEURISTIC_FILES)


def build_focused_system(
    *,
    heuristic_number: int,
    persona_alias: str,
) -> str:
    """Build a system prompt containing only:

    - required licensing, responsible-use, and interpretation safeguards
    - the heuristics index (supplementary concerns + Nielsen menu)
    - the one heuristic file for *heuristic_number*
    - the persona file for *persona_alias*

    This is the contract sub-agents rely on. If a sub-agent asks for
    content outside this scope, it should escalate to the orchestrator,
    not pull more KB inline.
    """
    if not 1 <= heuristic_number <= heuristic_count():
        raise ValueError(
            f"Heuristic number out of range: {heuristic_number}"
        )

    index = load_heuristic_index().rstrip()
    heuristic_body = load_heuristic(heuristic_number).rstrip()
    persona = load_persona_by_alias(persona_alias).rstrip()
    safeguards = load_required_persona_safeguards().rstrip()

    return (
        f"{safeguards}\n\n"
        "# Heuristics index (supplementary concerns + Nielsen menu)\n\n"
        f"{index}\n\n"
        f"# Heuristic {heuristic_number} (focused detail)\n\n"
        f"{heuristic_body}\n\n"
        "# Persona reference\n\n"
        f"{persona}\n"
    )


def focused_payload_bytes(
    *,
    heuristic_number: int,
    persona_alias: str,
) -> int:
    """Return the byte size of the focused system prompt.

    Useful for asserting the focused-loading contract: each sub-agent
    payload should stay well below the size of the full aggregate.
    """
    return len(
        build_focused_system(
            heuristic_number=heuristic_number,
            persona_alias=persona_alias,
        ).encode("utf-8")
    )
