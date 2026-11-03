# Disability Persona Toolkit (DPT)

Structured disability personas for AI agents, evaluation tools, and anyone who needs to reason about how people with disabilities use technology.

## What this is

A knowledge base of disability persona definitions, usability heuristics with accessibility lenses, evaluation methodology, and standards references. Markdown is the authoring source and human-readable reference; generated YAML personas are the structured distribution format for agents and evaluation pipelines.

The personas are based on **EN 301 549 Functional Performance Statements (FPS)** — the European standard's framework for describing user needs by functional capability rather than specific disability diagnosis. Each persona includes assistive technology interaction models, exploration strategies, user variants, learning considerations, and per-heuristic evaluation lenses.

## Development and community involvement

The toolkit distinguishes three foundations:

- **Established accessibility knowledge:** standards, assistive-technology interaction patterns, and documented research.
- **Expert interpretation:** our team's synthesis of that knowledge into AI-consumable instructions.
- **Community validation:** direct input from people with disabilities on whether the personas reflect their experiences.

We welcome people with disabilities to help review and improve this resource. Personas and
automated evaluations do not replace co-design and testing with people with disabilities.
No individual's perspective represents an entire disability community.

## Who this is for

- **Agent developers** building accessibility evaluation, design review, requirements analysis, or compliance tools — reference persona files directly as LLM context
- **Accessibility evaluators** who want structured persona frameworks for heuristic evaluation
- **Designers and researchers** who need detailed models of how assistive technology users navigate interfaces
- **Anyone** building tools that need to reason about disability and assistive technology interaction

## Repository structure

```
schemas/
  _baseline.yaml            # Generated baseline bundled by downstream consumers
  *.persona.yaml            # Generated structured persona definitions
  persona.schema.json       # Elaborated persona contract
  persona-stub.schema.json  # Stub persona contract

personas/
  # Human-readable reference content and adjacent third-party notices
  _baseline.md              # Universal strategies, variants, learning shared by all users
  4.2.1-blind.md            # Screen reader users (elaborated)
  4.2.2-low-vision.md       # Magnification, zoom, high contrast users (elaborated)
  4.2.3-color-blind.md      # Colour vision deficiency users (elaborated)
  4.2.4-deaf.md             # Deaf / hard-of-hearing users (elaborated)
  4.2.5-hard-of-hearing.md  # Users with limited hearing (elaborated)
  4.2.6-without-speech.md   # Users with no or limited vocal capability (elaborated)
  4.2.7-keyboard-only.md    # Motor disability, keyboard-only users (elaborated)
  4.2.7b-voice-access.md    # Voice control users (elaborated, shares clause 4.2.7)
  4.2.8-limited-reach.md    # Pointer/motor software proxy (elaborated)
  4.2.9-photosensitive.md   # Stub
  4.2.10-cognitive-memory.md     # Cognitive — memory, attention, executive function (elaborated)
  4.2.10b-cognitive-language.md  # Cognitive — language and communication (elaborated)
  4.2.10c-cognitive-numeracy.md  # Cognitive — numeracy and mathematical concepts (elaborated)
  cognitive-sources.LICENSE.md   # W3C COGA attribution for the three cognitive personas

heuristics/
  index.md                  # Supplementary concerns + Nielsen menu (entry point)
  h1-visibility.md          # One file per Nielsen heuristic
  severity.md               # Severity scale (0–4) and assessment model

methodology/
  licensing.md              # MIT notice and third-party distribution obligations
  responsible-persona-use.md # Prevent diagnosis, profiling, and high-impact use
  persona-interpretation.md # Preserve qualifiers, alternatives, and limitations
  confidence-gate.md        # Don't build findings on unverified assumptions
  persona-strategy-filter.md # Filter false positives using persona exploration strategies
  title-evidence-consistency.md  # Ensure findings match their evidence
  standard-conventions.md   # Prefer standard patterns over custom inventions
  design-system-trust.md    # Trust named design system components
  persona-coverage-priority.md # Prioritize personas by task-contextual divergence
  multi-persona.md          # Guidance for evaluating with multiple personas at once

standards/
  wcag-requirements.md      # WCAG 2.2 success criteria reference for findings annotation

provenance.json             # Machine-readable adapted-content sources, terms, and notices
```

## Persona status

| Clause | Alias | Title | Status |
|--------|-------|-------|--------|
| 4.2.1 | blind | Usage without vision | **Elaborated** |
| 4.2.2 | low-vision | Usage with limited vision | **Elaborated** |
| 4.2.3 | color-blind | Usage without perception of colour | **Elaborated** |
| 4.2.4 | deaf | Usage without hearing | **Elaborated** |
| 4.2.5 | hard-of-hearing | Usage with limited hearing | **Elaborated** |
| 4.2.6 | without-speech | Usage with no or limited vocal capability | **Elaborated** |
| 4.2.7 | keyboard-only | Usage with limited manipulation or strength | **Elaborated** |
| 4.2.7 | voice-access | Usage with limited manipulation or strength | **Elaborated** |
| 4.2.8 | limited-reach | Usage with limited reach | **Elaborated software proxy** |
| 4.2.9 | photosensitive | Minimize photosensitive seizure triggers | Stub |
| 4.2.10 | cognitive-memory | Usage with limited cognition, language or learning (memory, attention, and executive function) | **Elaborated** |
| 4.2.10 | cognitive-language | Usage with limited cognition, language or learning (language and communication) | **Elaborated** |
| 4.2.10 | cognitive-numeracy | Usage with limited cognition, language or learning (numeracy and mathematical concepts) | **Elaborated** |

The limited-reach persona models pointer/motor interaction for software evaluation; it does not
replace the clause's physical hardware-reach requirements. The photosensitive persona remains a
stub: do not infer detailed strategies or technologies it does not define.

FPS 4.2.11 (Privacy) is not modelled as a persona. Privacy concerns apply across all personas; see
the "Privacy / Discreet" supplementary concern in [heuristics/index.md](heuristics/index.md).

## Safe downstream consumption

This repository stores prompt-bearing material. Production execution occurs in downstream
consumers, while the local evaluation harness may send repository instructions and examples to a
configured model. Consumers should:

- pin an immutable commit or submodule revision rather than a mutable branch;
- preserve source `provenance.json` and required notices, then generate and verify exact hashes in
  the downstream package manifest;
- review updates to schemas, personas, heuristics, methodology, standards, repository skills,
  agent instructions, and evaluation prompts before changing the pinned revision;
- keep untrusted runtime input separate from trusted repository instructions; and
- enforce prompt-boundary and integrity controls in the consuming application.

CODEOWNERS and pull-request checks govern source changes. They do not make arbitrary downstream
prompt composition safe. Structural validation also cannot prove that persona prose is free from
every stereotype; material changes require human accessibility and Responsible AI review.

## How to use

### As an agent developer

For dependency-free use, read the [Markdown personas](personas/) directly. Elaborated Markdown
personas include applicable baseline content inline, but still require the licensing and use
safeguards below. Persona files include:

- A **persona prompt** (the core evaluation framing)
- **Assistive technologies** with interaction models
- **Exploration strategies** describing how the user navigates
- **User variants** representing sub-populations within the persona
- **Learning considerations** for how the user approaches new interfaces
- **Heuristic lens overrides** that reframe each usability heuristic for the persona

Always load [licensing](methodology/licensing.md),
[responsible persona use](methodology/responsible-persona-use.md), and
[persona interpretation](methodology/persona-interpretation.md) with persona content.
Preserve adjacent third-party notices and [provenance.json](provenance.json) in distributions.
The [WCAG reference](standards/wcag-requirements.md) can annotate findings; it is supporting
material, not an authoritative specification or a guarantee of compliance.

For structured use, distribute a [generated persona](schemas/4.2.2-low-vision.persona.yaml)
with [schemas/_baseline.yaml](schemas/_baseline.yaml). For an elaborated persona, append
baseline `strategies`, `user_variants`, and `learning` items whose IDs are not in its
`baseline_excludes`, tagging appended items `from_baseline: true`. Do not append these fields to
a stub or invent its missing content. Keep persona aliases and standards identifiers unchanged.

With development dependencies installed, this local example performs the merge and includes the
three required safeguards without calling a model:

```sh
# Run from the resource directory.
PERSONA_SOURCE=schema python -c "from tests.evals._context import load_eval_persona_context; print(load_eval_persona_context('low-vision'))"
```

In PowerShell, set `$env:PERSONA_SOURCE = "schema"` before running the Python command, and remove
the override afterwards with `Remove-Item Env:PERSONA_SOURCE`. The default `PERSONA_SOURCE=md`
loads the authoring Markdown. Supporting multi-persona briefs remain Markdown-based summaries.

The repository evaluation harness automatically prepends these three documents to prompts assembled
through `load_eval_persona_context()` in single, all-persona, and medium modes, to focused heuristic
evaluations, and to per-heuristic sub-agent system prompts assembled by
`sub_agents/_loaders.py`. Low-level `load_persona_by_alias()` calls intentionally return raw persona
content; custom prompt builders must call `with_required_persona_safeguards()` or include all three
documents explicitly.

### As a human reader

Read persona files to understand how specific user groups interact with technology. Each file is structured reference documentation, not code.

## Baseline content and propagation

Each elaborated persona includes applicable baseline content (from `_baseline.md`) inline. This makes each file self-contained but means shared content is duplicated across personas.

**When updating baseline content:**
1. Update `personas/_baseline.md`
2. Propagate changes to all elaborated persona files (baseline content is marked `*(from baseline)*`)
3. Regenerate the baseline and affected YAML with the [persona-to-schema skill](../.github/skills/persona-to-schema/SKILL.md)
4. Review generated fidelity and run `python tests/validate_structure.py`

Structural validation checks markers and schema structure; strict inherited-body comparison
currently targets low vision. Neither check proves complete Markdown/YAML semantic equivalence.

## Development and offline validation

Use Python 3.12 or 3.14 (the offline CI matrix), create a virtual environment, and install
[requirements-dev.txt](requirements-dev.txt). Reading or copying the knowledge base needs no
Python, Copilot subscription, or model credentials.

```sh
# macOS / Linux, from the resource directory
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python tests/validate_structure.py
python -m pytest tests/validate_structure.py tests -q
```

```powershell
# Windows, from the resource directory
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python tests/validate_structure.py
python -m pytest tests/validate_structure.py tests -q
```

[Offline CI](../.github/workflows/dpt-validate.yml) is configured to run structural, provenance, fixture,
loader and consistency tests without authentication or model calls. GitHub-hosted runners must
be enabled by repository policy before these jobs can execute. Dependencies have minimum versions,
not a locked environment; record installed versions when comparing eval results.
See the [evaluation guide](tests/evals/README.md) for optional authenticated model evaluations.

### Monorepo workflow and agent instructions

From the monorepo root, run `cd Disability-Persona-Toolkit` before the commands above.
The workflow lives in the root `.github/workflows/` directory so GitHub discovers it, but both
pull-request and main-branch push triggers are filtered to toolkit content, its scoped
instructions/conversion skill, and its review-policy files. Every shell step runs in this
resource directory. Windows-only changes do not trigger DPT validation; the Windows release
workflow and tag pattern are unchanged. Manual workflow dispatch is also available.

Because path-filtered workflows are skipped for unrelated changes, do not make DPT checks
unconditionally required for every monorepo pull request without an always-running gate.

[Scoped Copilot instructions](../.github/instructions/dpt.instructions.md) load
[AGENTS.md](AGENTS.md) for toolkit work without applying persona rules to other projects.
The [persona-to-schema skill](../.github/skills/persona-to-schema/SKILL.md) remains available
when opening the monorepo. If opening just this resource folder, load the skill file explicitly.
Conversion gates, baseline propagation, and Markdown-to-YAML direction are unchanged.
The structural validator checks root-level CODEOWNERS and the review template as well as
resource-local content. CODEOWNERS declarations do not prove that reviewers have write access
or that reviews occurred; maintainers must enable appropriate branch review rules.

## Eval authoring patterns

The `tests/evals/` harness supports two grading styles:

- **Rubric evals** use `rubric_scorer(...)` when a judge model should assess semantic completeness against explicit criteria.
- **Hidden answer-key evals** use `answer_key_scorer()` for a deterministically scored model "pop quiz". Put the answer key in `Sample.metadata["answer_key"]`; it is not sent to the model under test. These still call a model, unlike offline consistency tests. The default pass threshold is `0.8`, so a response passes when it matches at least 80% of the weighted expected items.

See [deterministic/low_vision.py](tests/evals/deterministic/low_vision.py) for a concrete example.

## Branching model

`main` is the development branch. Consumers should pin a reviewed immutable commit or submodule
revision, not a mutable branch. Updating a pin requires reviewing changed
content and regenerating downstream hashes. A DPT release/tag convention is not yet
defined; do not assume another project's release is a release of this resource.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to elaborate stub personas, update baseline content, and add methodology or standards files.

## License, security and support

Original contributions are covered by the [MIT License](LICENSE.txt); upstream material has
additional terms described in [licensing](methodology/licensing.md) and the
[source inventory](standards/sources.md).
This resource does not replace research with people with disabilities, assistive-technology
testing, or a formal standards assessment.

Use GitHub issues for resource questions and bugs. Report security vulnerabilities privately using
[SECURITY.md](../SECURITY.md), not public issues. See the [Code of Conduct](../CODE_OF_CONDUCT.md)
and shared [support policy](../SUPPORT.md).
