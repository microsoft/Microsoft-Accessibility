# Contributing to Disability Persona Toolkit (DPT)

Follow the monorepo's [contribution and CLA process](../CONTRIBUTING.md).
All commands and content paths below are relative to `Disability-Persona-Toolkit`.
GitHub discovers the [conversion skill](../.github/skills/persona-to-schema/SKILL.md),
[review template](../.github/PULL_REQUEST_TEMPLATE.md), and
[CODEOWNERS](../.github/CODEOWNERS) at the monorepo root.

## Elaborating a stub persona

Markdown under `personas/` is the authoring source. YAML under `schemas/` is generated for
structured distribution, not a separate authoring source. To elaborate a stub:

1. Read [keyboard-only](personas/4.2.7-keyboard-only.md) and
   [blind](personas/4.2.1-blind.md) for the Markdown structure.

2. Update the Markdown frontmatter:
   - Change `status: stub` to `status: elaborated`
   - Add `baseline_excludes` if any baseline strategies don't apply

3. Add all six required H2 sections: Persona Prompt, Assistive Technologies, Exploration
   Strategies, User Variants, Learning Considerations, and Heuristic Lens Overrides (1-10).

4. For each AT, include its name, category, platforms, device context, and interaction model.

5. For each strategy, include mechanisms, behavior, and UI requirements.

6. For each user variant, include behavior, preferred navigation/AT, and interface expectations.

7. Generate the matching YAML with the [persona-to-schema skill](../.github/skills/persona-to-schema/SKILL.md).
   Review fidelity, provenance, stable IDs, baseline exclusions and
   [persona.schema.json](schemas/persona.schema.json) validation. Do not reconstruct Markdown
   from compressed YAML.

8. Run `python tests/validate_structure.py` and `python -m pytest tests/validate_structure.py tests -q`.

9. Complete the material-persona review checklist in the pull request. Document evidence,
   limitations, the review method, and consented lived-experience perspectives without publishing
   reviewer identities or sensitive information.

## Updating baseline content

Author baseline strategies, variants, and learning considerations in
[personas/_baseline.md](personas/_baseline.md). To update:

1. Edit `personas/_baseline.md`.
2. Propagate applicable inline Markdown copies, preserving `*(from baseline)*` markers.
3. Regenerate `schemas/_baseline.yaml` and affected persona YAML with the conversion skill.
4. Review generated fidelity and run the offline validation commands above.

Structural validation checks baseline markers and schema structure. Strict inherited-body checks
currently target low vision; passing tests is not proof of complete semantic equivalence.

## Adding a methodology principle

1. Create a new markdown file in `methodology/` with a clear, descriptive filename
2. Write the principle as a standalone reference document — it should be understandable without external context
3. Update `README.md` to include the new file in the repository structure section

## Licensing and provenance

- Keep the complete repository MIT notice in `LICENSE.txt` and
  `methodology/licensing.md`; validation requires the agent-readable Markdown copy to match.
- For copied or adapted material, document the source, version, reuse terms and required notices
  before adding content. Preserve supported provenance in authoring Markdown and generated YAML;
  update `provenance.json` for all distributed representations.
- Keep required third-party notices adjacent to the affected source. The W3C-derived cognitive
  personas require `personas/cognitive-sources.LICENSE.md`; the WCAG reference requires
  `standards/wcag-requirements.LICENSE.md`.
- Do not use the repository MIT license to replace or obscure third-party terms.
- Consult the [source inventory](standards/sources.md). Attribution alone is not permission.
- Use original synthetic [image fixtures](tests/fixtures/images/README.md), not customer screenshots
  or third-party material without documented redistribution and privacy clearance.

## Responsible persona use

Persona content must evaluate possible interface barriers, not classify real people. Do not infer
disability, diagnosis, capability, or accommodation from behavior, zoom level, preferences, errors,
or assistive-technology use. Preserve conditional language, variations, limitations, and
intersectional needs. See `methodology/responsible-persona-use.md` and
`methodology/persona-interpretation.md`.

## AI-consumed content security

Persona schemas, personas, heuristics, methodology, standards references, Copilot instructions,
repository skills, and model-evaluation prompts or rubrics may become model context. Changes to
those paths and their governance files require CODEOWNER review.

- Review prompt-bearing changes for instructions that override consumer policy, redirect tool use,
  request secrets, conceal behavior, or promote external text from data to trusted instructions.
- Keep quoted, copied, and example content clearly bounded and preserve its provenance.
- Do not instruct consumers to fetch a mutable branch at runtime. Consumers should pin an immutable
  commit or submodule revision, preserve source provenance, and generate exact hashes in their
  downstream distribution manifest.
- Source review reduces the chance of introducing hostile instructions; it does not replace
  downstream prompt separation, runtime input handling, or integrity verification.

The structural validator checks required content, provenance, and selected safeguards. It cannot
prove that prose is stereotype-free or safe in every model and prompt composition. Material changes
still require human accessibility, Responsible AI, and adversarial-content review.

## File structure conventions

- Author personas in Markdown under `personas/`; distribute generated YAML with the generated
  baseline, required safeguards, provenance and notices. Markdown consumers still need safeguards.
- All H2 section headers in persona files are considered required for elaborated personas
- Baseline content included in persona files is marked with `*(from baseline)*` suffix on the H3 header
- Stub personas need only frontmatter and the H1 title + description
- A single EN 301 549 clause may be split across multiple schemas when it spans distinct
  functional profiles. Each schema shares the `clause` value but has its own `alias`; load these by
  alias, not by clause.
- When persona content adapts an external source, keep all source-derived material in the persona files and document attribution in a co-located `*.LICENSE.md` notice (e.g., `personas/cognitive-sources.LICENSE.md`)
- Every elaborated persona must contain substantive assistive-technology, exploration-strategy,
  user-variant, and learning-consideration sections with conditional language.

## Setup and review

See [README.md](README.md#development-and-offline-validation) for Windows and macOS/Linux setup.
Offline validation does not require model authentication. Authenticated evals are manual and
must follow the [evaluation data-flow guidance](tests/evals/README.md#data-flow-and-artifacts).
Review contributions under the [Code of Conduct](../CODE_OF_CONDUCT.md). Report vulnerabilities
privately using [SECURITY.md](../SECURITY.md); use the shared [support policy](../SUPPORT.md)
for non-security questions.
