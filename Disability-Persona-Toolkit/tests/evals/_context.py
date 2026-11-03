"""Loaders for repository instruction files used as LLM context.

Each loader returns the file contents as a string, ready to embed in a
system prompt. Loaders never modify or duplicate content — they always
read from the canonical files in personas/, heuristics/, methodology/,
and standards/.

When ``PERSONA_SOURCE=schema``, persona content is loaded from generated
YAML files in ``schemas/`` and rendered as self-contained YAML at load time. The
default (``PERSONA_SOURCE=md``) reads raw markdown from ``personas/``.
"""

from __future__ import annotations

import logging
import os
import re
from functools import lru_cache
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
PERSONAS_DIR = REPO_ROOT / "personas"
SCHEMAS_DIR = REPO_ROOT / "schemas"
HEURISTICS_DIR = REPO_ROOT / "heuristics"
METHODOLOGY_DIR = REPO_ROOT / "methodology"
STANDARDS_DIR = REPO_ROOT / "standards"
_EVAL_PERSONA_CONTEXT_MODE = "single"
_SINGLE_PERSONA_CONTEXT_MODES = {"", "single", "specific", "persona"}
_COMPACT_PERSONA_CONTEXT_MODES = {"all", "multi", "multi-persona", "all-personas", "compact"}
_MEDIUM_PERSONA_CONTEXT_MODES = {"medium", "medium-brief", "medium-briefs"}
_REQUIRED_PERSONA_METHODOLOGY = (
    "licensing",
    "responsible-persona-use",
    "persona-interpretation",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@lru_cache(maxsize=None)
def load_baseline() -> str:
    return _read(PERSONAS_DIR / "_baseline.md")


# ---------------------------------------------------------------------------
# Schema-based persona loading (PERSONA_SOURCE=schema)
# ---------------------------------------------------------------------------

def _get_persona_source() -> str:
    """Return 'schema' or 'md' based on the PERSONA_SOURCE env var."""
    source = os.environ.get("PERSONA_SOURCE", "md").strip().lower()
    if source not in {"md", "schema"}:
        raise ValueError(f"Unsupported PERSONA_SOURCE {source!r}; use 'md' or 'schema'.")
    return source


@lru_cache(maxsize=None)
def _load_persona_schema_file(alias: str) -> dict:
    """Load a persona YAML schema instance by alias from schemas/."""
    candidates = sorted(SCHEMAS_DIR.glob(f"*-{alias}.persona.yaml"))
    if not candidates:
        candidates = sorted(SCHEMAS_DIR.glob(f"{alias}.persona.yaml"))
    if not candidates:
        raise FileNotFoundError(
            f"No persona schema for alias '{alias}' in {SCHEMAS_DIR}"
        )
    return yaml.safe_load(candidates[0].read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _load_baseline_schema() -> dict:
    """Load the structured baseline YAML (schemas/_baseline.yaml)."""
    path = SCHEMAS_DIR / "_baseline.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _render_persona_from_schema(instance: dict) -> str:
    """Merge baseline content into persona schema instance and dump as YAML.

    The output is a self-contained YAML document with baseline strategies,
    variants, and learning merged in (tagged from_baseline: true) according
    to baseline_excludes.
    """
    excludes = set(instance.get("baseline_excludes", []))
    merged = {k: v for k, v in instance.items()}  # shallow copy preserving order

    if instance["status"] == "stub":
        return yaml.safe_dump(merged, allow_unicode=True, sort_keys=False, width=120)
    if instance["status"] != "elaborated":
        raise ValueError(f"Unsupported persona status: {instance['status']!r}")

    baseline = _load_baseline_schema()

    # Merge baseline strategies
    extra_strats = [
        {**s, "from_baseline": True}
        for s in baseline["strategies"]
        if s["id"] not in excludes
    ]
    merged["strategies"] = list(instance["strategies"]) + extra_strats

    # Merge baseline variants
    extra_vars = [
        {**v, "from_baseline": True}
        for v in baseline["user_variants"]
        if v["id"] not in excludes
    ]
    merged["user_variants"] = list(instance["user_variants"]) + extra_vars

    # Merge baseline learning
    extra_learn = [
        {**lc, "from_baseline": True}
        for lc in baseline["learning"]
        if lc["id"] not in excludes
    ]
    merged["learning"] = list(instance["learning"]) + extra_learn

    header = (
        f"# Accessibility persona: {instance['alias']} "
        f"(FPS {instance['clause']})\n"
        f"# Baseline merged (excludes: {', '.join(sorted(excludes)) or 'none'})\n"
    )
    body = yaml.dump(
        merged,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )
    return header + body


@lru_cache(maxsize=None)
def load_persona(clause: str) -> str:
    """Load a persona file by its clause number (e.g. '4.2.2').

    Picks the unique persona file whose name starts with the clause.
    Raises FileNotFoundError if no match or ambiguous match.
    """
    candidates = sorted(PERSONAS_DIR.glob(f"{clause}-*.md"))
    if not candidates:
        raise FileNotFoundError(f"No persona file for clause {clause}")
    if len(candidates) > 1:
        # 4.2.7 has two files (keyboard-only and voice-access); require
        # alias-suffixed callers to use load_persona_by_alias instead.
        raise ValueError(
            f"Multiple personas for clause {clause}: "
            f"{[p.name for p in candidates]}; use load_persona_by_alias"
        )
    return _read(candidates[0])


def load_persona_by_alias(alias: str) -> str:
    return _load_persona_by_alias(alias, _get_persona_source())


@lru_cache(maxsize=None)
def _load_persona_by_alias(alias: str, source: str) -> str:
    if source == "schema":
        try:
            instance = _load_persona_schema_file(alias)
        except FileNotFoundError:
            logger.warning(
                "Schema not found for persona '%s'; falling back to markdown",
                alias,
            )
        else:
            result = _render_persona_from_schema(instance)
            logger.info("Loaded persona '%s' from schema (YAML)", alias)
            return result
    candidates = sorted(PERSONAS_DIR.glob(f"*-{alias}.md"))
    if not candidates:
        raise FileNotFoundError(f"No persona file for alias '{alias}'")
    logger.info("Loaded persona '%s' from markdown", alias)
    return _read(candidates[0])


# Ordered list of per-heuristic files. Index is the Nielsen number (1..10).
HEURISTIC_FILES: tuple[str, ...] = (
    "h1-visibility.md",
    "h2-match.md",
    "h3-control.md",
    "h4-consistency.md",
    "h5-error-prevention.md",
    "h6-recognition.md",
    "h7-flexibility.md",
    "h8-minimalist.md",
    "h9-errors.md",
    "h10-help.md",
)


@lru_cache(maxsize=None)
def load_heuristic_index() -> str:
    """Load the heuristics index file.

    Contains supplementary concerns (Privacy/Discreet, Bad Prediction) and a
    menu of the 10 Nielsen heuristics with filename pointers. Use this when
    the agent needs to plan which heuristics to load on demand.
    """
    return _read(HEURISTICS_DIR / "index.md")


@lru_cache(maxsize=None)
def load_heuristic(n: int) -> str:
    """Load a single Nielsen heuristic file by number (1..10)."""
    if not 1 <= n <= len(HEURISTIC_FILES):
        raise ValueError(f"Heuristic number out of range: {n}")
    return _read(HEURISTICS_DIR / HEURISTIC_FILES[n - 1])


@lru_cache(maxsize=None)
def load_all_elaborated_persona_briefs() -> str:
    personas: list[str] = []
    for path in sorted(PERSONAS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = _read(path)
        if not re.search(r"^status:\s*elaborated\s*$", text, re.MULTILINE):
            continue
        clause_match = re.search(r"^clause:\s*(.+?)\s*$", text, re.MULTILINE)
        alias_match = re.search(r"^alias:\s*(.+?)\s*$", text, re.MULTILINE)
        title_match = re.search(r"^title:\s*(.+?)\s*$", text, re.MULTILINE)
        clause = clause_match.group(1).strip().strip('"\'') if clause_match else ""
        alias = alias_match.group(1).strip().strip('"\'') if alias_match else path.stem
        title = title_match.group(1).strip().strip('"\'') if title_match else ""
        persona_prompt = extract_section(text, "Persona Prompt")
        strategy_headings = _extract_h3_headings(extract_section(text, "Exploration Strategies"))
        variant_headings = _extract_h3_headings(extract_section(text, "User Variants"))
        brief_lines = [f"## {alias} ({clause} — {title})"]
        if persona_prompt:
            brief_lines.extend(["### Persona Prompt", persona_prompt])
        if strategy_headings:
            brief_lines.append("### Exploration Strategy Headings")
            brief_lines.extend(f"- {heading}" for heading in strategy_headings)
        if variant_headings:
            brief_lines.append("### User Variant Headings")
            brief_lines.extend(f"- {heading}" for heading in variant_headings)
        personas.append("\n".join(brief_lines))
    return "\n\n".join(personas)


@lru_cache(maxsize=None)
def load_heuristics() -> str:
    """Back-compat aggregator: concatenates the index and all 10 heuristic
    files into a single string. New callers should prefer
    ``load_heuristic_index()`` plus targeted ``load_heuristic(n)`` calls so
    they only pay for the heuristics the evaluation actually needs.
    """
    parts: list[str] = [load_heuristic_index().rstrip()]
    for n in range(1, len(HEURISTIC_FILES) + 1):
        parts.append(load_heuristic(n).rstrip())
    return "\n\n".join(parts) + "\n"


@lru_cache(maxsize=None)
def load_severity() -> str:
    return _read(HEURISTICS_DIR / "severity.md")


@lru_cache(maxsize=None)
def load_methodology(name: str) -> str:
    return _read(METHODOLOGY_DIR / f"{name}.md")


@lru_cache(maxsize=None)
def load_required_persona_safeguards() -> str:
    """Load methodology that must accompany every persona evaluation prompt."""
    return "\n\n".join(
        f"# Required methodology: methodology/{name}.md\n\n{load_methodology(name)}"
        for name in _REQUIRED_PERSONA_METHODOLOGY
    )


def with_required_persona_safeguards(persona_context: str) -> str:
    """Prepend mandatory licensing, responsible-use, and interpretation policy."""
    return f"{load_required_persona_safeguards()}\n\n# Persona evaluation context\n\n{persona_context}"


@lru_cache(maxsize=None)
def load_standard(name: str) -> str:
    """Load a standards reference file from ``standards/`` by base name
    (e.g. 'wcag-requirements')."""
    return _read(STANDARDS_DIR / f"{name}.md")


def set_eval_persona_context_mode(mode: str) -> None:
    normalized = mode.strip().lower() or "single"
    allowed = (
        _SINGLE_PERSONA_CONTEXT_MODES
        | _COMPACT_PERSONA_CONTEXT_MODES
        | _MEDIUM_PERSONA_CONTEXT_MODES
    )
    if normalized not in allowed:
        raise ValueError(
            "Unsupported persona_context_mode "
            f"'{mode}'. Use 'single', 'all', or 'medium'."
        )

    global _EVAL_PERSONA_CONTEXT_MODE
    _EVAL_PERSONA_CONTEXT_MODE = normalized


def get_eval_persona_context_mode() -> str:
    return _EVAL_PERSONA_CONTEXT_MODE


def load_eval_persona_context(alias: str) -> str:
    mode = get_eval_persona_context_mode()
    if mode in _SINGLE_PERSONA_CONTEXT_MODES:
        return with_required_persona_safeguards(load_persona_by_alias(alias))
    if mode in _COMPACT_PERSONA_CONTEXT_MODES | _MEDIUM_PERSONA_CONTEXT_MODES:
        primary_persona = load_persona_by_alias(alias)
        is_elaborated = bool(
            re.search(r"^status:\s*elaborated\s*$", primary_persona, re.MULTILINE)
        )
        supporting_label = "Compact Catalog"
        supporting_personas = load_all_elaborated_persona_catalog_except(alias)
        if mode in _MEDIUM_PERSONA_CONTEXT_MODES:
            supporting_label = "Medium Briefs"
            supporting_personas = load_all_elaborated_persona_medium_briefs_except(alias)
        background_instruction = (
            "Use the additional persona briefs only as background context. "
            "Answer for the target persona unless the prompt explicitly asks for multi-"
            "persona synthesis. Do not average personas together, substitute another "
            "persona's needs, or dump the full loaded bundle back to the user."
        )
        if not is_elaborated:
            background_instruction += (
                " The primary persona is a stub and remains authoritative. "
                "If the prompt asks for assistive technologies, exploration strategies, "
                "or variants that the stub does not define, explicitly acknowledge that "
                "the persona is not yet elaborated and do not borrow or infer those "
                "details from the background personas."
            )
        context = (
            "You are running a persona eval module with all elaborated persona briefs "
            "loaded into context. The primary target persona for this module is "
            f"'{alias}'. The primary persona definition below is authoritative for task "
            f"answers. {background_instruction}\n\n"
            f"# Primary Persona (Authoritative)\n\n{primary_persona}\n\n"
            f"# Multi-Persona Guidance\n\n{load_methodology('multi-persona')}\n\n"
            f"# Other Loaded Personas ({supporting_label})\n\n"
            f"{supporting_personas}"
        )
        return with_required_persona_safeguards(context)
    raise ValueError(
        "Unsupported persona_context_mode "
        f"'{mode}'. Use 'single', 'all', or 'medium'."
    )


def _extract_h3_headings(text: str) -> list[str]:
    return re.findall(r"^###\s+(.+?)\s*$", text, re.MULTILINE)


@lru_cache(maxsize=None)
def load_all_elaborated_persona_catalog_except(alias: str) -> str:
    items: list[str] = []
    for path in sorted(PERSONAS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = _read(path)
        if not re.search(r"^status:\s*elaborated\s*$", text, re.MULTILINE):
            continue
        alias_match = re.search(r"^alias:\s*(.+?)\s*$", text, re.MULTILINE)
        item_alias = alias_match.group(1).strip().strip('"\'') if alias_match else path.stem
        if item_alias == alias:
            continue
        clause_match = re.search(r"^clause:\s*(.+?)\s*$", text, re.MULTILINE)
        title_match = re.search(r"^title:\s*(.+?)\s*$", text, re.MULTILINE)
        clause = clause_match.group(1).strip().strip('"\'') if clause_match else ""
        title = title_match.group(1).strip().strip('"\'') if title_match else ""
        persona_prompt = re.sub(r"\s+", " ", extract_section(text, "Persona Prompt")).strip()
        summary = persona_prompt[:220].rsplit(" ", 1)[0] if len(persona_prompt) > 220 else persona_prompt
        items.append(f"- {item_alias} ({clause} — {title}): {summary}")
    return "\n".join(items)


@lru_cache(maxsize=None)
def load_all_elaborated_persona_medium_briefs_except(alias: str) -> str:
    items: list[str] = []
    for path in sorted(PERSONAS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = _read(path)
        if not re.search(r"^status:\s*elaborated\s*$", text, re.MULTILINE):
            continue
        alias_match = re.search(r"^alias:\s*(.+?)\s*$", text, re.MULTILINE)
        item_alias = alias_match.group(1).strip().strip('"\'') if alias_match else path.stem
        if item_alias == alias:
            continue
        clause_match = re.search(r"^clause:\s*(.+?)\s*$", text, re.MULTILINE)
        title_match = re.search(r"^title:\s*(.+?)\s*$", text, re.MULTILINE)
        clause = clause_match.group(1).strip().strip('"\'') if clause_match else ""
        title = title_match.group(1).strip().strip('"\'') if title_match else ""
        persona_prompt = re.sub(r"\s+", " ", extract_section(text, "Persona Prompt")).strip()
        if len(persona_prompt) > 320:
            persona_prompt = persona_prompt[:320].rsplit(" ", 1)[0] + "..."
        strategy_headings = _extract_h3_headings(
            extract_section(text, "Exploration Strategies")
        )[:3]
        variant_headings = _extract_h3_headings(
            extract_section(text, "User Variants")
        )[:3]

        lines = [f"## {item_alias} ({clause} — {title})"]
        if persona_prompt:
            lines.append(f"Persona prompt: {persona_prompt}")
        if strategy_headings:
            lines.append("Strategy headings: " + "; ".join(strategy_headings))
        if variant_headings:
            lines.append("Variant headings: " + "; ".join(variant_headings))
        items.append("\n".join(lines))
    return "\n\n".join(items)


def extract_section(text: str, heading: str, level: int = 2) -> str:
    """Return the raw text under a markdown heading, up to the next
    same-or-higher-level heading or end of file. Used by deterministic
    consistency checks; not used to rewrite content."""
    marker = "#" * level
    pattern = rf"^{re.escape(marker)} {re.escape(heading)}\n(.*?)(?=^#{{1,{level}}} |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()
