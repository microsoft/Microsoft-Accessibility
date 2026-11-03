# Disability Persona Toolkit (DPT) — Agent Instructions

A knowledge base based on EN 301 549 Functional Performance Statements (FPS). Author personas
and baseline in Markdown; generated YAML is the structured distribution format. See
[CONTRIBUTING.md](CONTRIBUTING.md) for conversion and review requirements.

These instructions apply only to this resource. All paths and commands below are relative
to `Disability-Persona-Toolkit`; change to that directory when working from the monorepo root.
The [persona-to-schema skill](../.github/skills/persona-to-schema/SKILL.md) is discovered at
the monorepo root. When opening this resource alone, load that file explicitly for conversion.

## Commands

### Setup

```sh
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows
pip install -r requirements-dev.txt
copilot login                   # authenticate with GitHub Copilot
```

### Validate structure (run before every commit to `personas/` or `heuristics/`)

```sh
python tests/validate_structure.py
# or via pytest:
pytest tests/validate_structure.py
```

### Deterministic consistency checks (no API key needed)

```sh
python -m pytest tests/validate_structure.py tests -q
```

### LLM eval — smoke test (fastest sanity check)

```sh
python tests/evals/run_copilot_eval.py copilot/gpt-5-mini smoke.py
```

### LLM eval — single task

```sh
python tests/evals/run_copilot_eval.py copilot/gpt-5-mini personas/eval_low_vision.py@at_recall
```

### LLM eval — selected persona/heuristic/methodology checks

```sh
python tests/evals/run_copilot_eval.py copilot/gpt-5-mini `
  personas/eval_low_vision.py `
  heuristics/eval_heuristic_1.py `
  methodology/eval_confidence_gate.py `
  negative/eval_privacy_clause.py
```

### LLM eval — Claude

```sh
python tests/evals/run_copilot_eval.py copilot/claude-sonnet-4.5 smoke_copilot:smoke_copilot
```

### View eval results

```sh
python -m inspect_ai view start --log-dir logs   # interactive browser
python -m inspect_ai log dump logs/<file>.eval   # JSON dump to terminal
```

Set `EVAL_QUICK=1` to subset parameterized samples for fast iteration.

## Architecture

### Content layer (`schemas/`, `personas/`, `heuristics/`, `methodology/`, `standards/`)

Reference Markdown and generated YAML consumed as LLM context. No code runs in these directories.

- **`schemas/_baseline.yaml`** — generated shared strategies, user variants, and learning guidance.
- **`schemas/4.2.N-*.persona.yaml`** — generated persona definitions bundled by downstream
  consumers. Adapted schemas carry structured provenance.
- **`personas/`** — authoring source, human-readable reference content and adjacent third-party notices.
- **`heuristics/index.md` + `heuristics/h1-visibility.md` … `heuristics/h10-help.md`** — the 10 usability heuristics with generic accessibility lenses, split per file for focused sub-agent loading. `index.md` holds the supplementary concerns (Privacy/Discreet, Bad Prediction) and the Nielsen menu; each `h<N>-*.md` holds one heuristic's Definition + Accessibility Lens. Each elaborated persona overrides these per-heuristic in its `## Heuristic Lens Overrides` section.
- **`methodology/`** — standalone evaluation principles. Always load `licensing.md`,
  `responsible-persona-use.md`, and `persona-interpretation.md` with persona content.
- **`standards/`** — the WCAG 2.2 success criteria reference used to annotate findings with applicable success criteria.

### Validation layer (`tests/validate_structure.py`)

Pure-Python, no LLM. Validates canonical YAML schema structure, nuance, provenance, notices, and
Markdown consistency. Runs as both a CLI script and a pytest module.

### AI-consumed content security

Treat schemas, personas, heuristics, methodology, standards, instructions, skills, and evaluation
prompts or rubrics as prompt-bearing content. Do not add instructions that override consumer
policy, redirect tool use, request secrets, or conceal behavior. Keep external quotations and
examples bounded as data, preserve provenance, and recommend immutable commit or submodule pins
rather than mutable branches. Source controls do not replace runtime enforcement by downstream
consumers.

### LLM eval layer (`tests/evals/`)

[inspect-ai](https://inspect.aisi.org.uk/)-based. Each eval module loads one instruction artifact as the system prompt and rubric-grades model output. Authenticated model evaluations are manual; offline tests run in CI. Key files:

- `_providers.py` — loads `.env`, exposes model IDs from `config.yaml` and env overrides
- `_scorers.py` — shared rubric-scoring helpers
- `_context.py` — shared context loader
- `config.yaml` — default model matrix and generation settings
- `copilot_provider/` — wraps `@github/copilot` CLI for routing all models through the Copilot SDK

Eval results are written as binary `.eval` files to `logs/`.

## Key conventions

### Persona file structure (elaborated)

```
---
clause: "4.2.N"
title: "EN 301 549 FPS title"
alias: short-name
status: elaborated
baseline_excludes:          # optional — list of baseline strategy IDs to omit
  - mouse-pointer-interaction
---

<!-- inheritance comment -->

# FPS 4.2.N — Title

## Persona Prompt
## Assistive Technologies
## Exploration Strategies
## User Variants
## Learning Considerations
## Heuristic Lens Overrides
```

All six H2 sections are required for `status: elaborated`. Sections must appear in this order. Validate with `python tests/validate_structure.py`.

Persona content is an interface-evaluation lens, not evidence about a real person. Never infer
disability, diagnosis, capability, or accommodation from observed behavior, zoom, preferences, or
assistive-technology use. Preserve qualifiers and meaningful variation.

### Baseline propagation

Baseline content is copied inline into every elaborated persona. Each copied item's H3 header ends with `*(from baseline)*`. When `_baseline.md` changes:
1. Update `_baseline.md`
2. Find all elaborated personas using that content (grep for `*(from baseline)*`)
3. Update the inline copy in each persona to match
4. Regenerate baseline and affected persona YAML using the persona-to-schema skill
5. Review fidelity and run validation — it will flag missing `*(from baseline)*` markers

### Heuristic lens overrides

Each H3 under `## Heuristic Lens Overrides` must match the format `Heuristic N — ...` where N is 1–10. The validator parses this to confirm IDs are in range.

### AT entry format

Each AT under `## Assistive Technologies` is an H3 and must include: name, `**Category**`, `**Platforms**`, `**Device context**`, and an interaction model description.

### Branching

- `main` — active development
- Consumers pin reviewed immutable commits or submodule revisions, not mutable branches.

### Eval model env overrides

| Variable | Default |
|---|---|
| `EVAL_MODEL_PRIMARY` | `copilot/gpt-5-mini` |
| `EVAL_MODEL_SECONDARY` | `copilot/claude-haiku-4.5` |
| `EVAL_MODEL_CLAUDE` | `copilot/claude-sonnet-4.5` |
| `EVAL_JUDGE_MODEL` | same as primary |
| `EVAL_RUBRIC_THRESHOLD` | `0.8` |
| `EVAL_QUICK` | `1` to use one sample per parameterized task |
