# LLM evaluation suite

These tests verify that the instruction files in this repository
(personas, heuristics, methodology, standards) actually transfer
accessibility subject-matter expertise to an LLM. The harness is
[inspect-ai](https://inspect.aisi.org.uk/), driven from Python.

Authenticated LLM evaluations are **manually invoked**, not run on CI pull requests.
Offline structural, provenance, fixture, loader and consistency tests are configured in
[CI](../../../.github/workflows/dpt-validate.yml), subject to authorized runner availability.
Each granular model task isolates instruction
artifacts and grades the model's output against
expectations rooted in the source file.

## Status

The maintained suite covers all 12 elaborated personas and photosensitive-stub handling.
Heuristic lens evaluations span the 10 heuristics; methodology and negative evaluations
cover selected principles and scenarios. Coverage is not certification of every persona,
device, standard or model. A passing offline suite does not demonstrate LLM behavior.

| Category | Example artifact | Module |
|---|---|---|
| Persona | `4.2.2-low-vision.md` | `personas/eval_low_vision.py` |
| Heuristic | Heuristic 1 + severity scale | `heuristics/eval_heuristic_1.py` |
| Methodology | `confidence-gate.md` | `methodology/eval_confidence_gate.py` |
| Consistency | Baseline propagation (low-vision) | `consistency/test_baseline_propagation.py` |
| Negative | Clause 4.2.11 refusal | `negative/eval_privacy_clause.py` |

## Setup

Follow the [Windows or macOS/Linux setup](../../README.md#development-and-offline-validation)
from the resource directory. Use Python 3.12 or 3.14, the offline CI matrix.
Reading content requires no development dependencies.

All models route through the GitHub Copilot SDK provider. No API keys needed.

### Copilot SDK setup

One-time setup:

1. Install Node.js 22 or later.
2. Install the Copilot CLI globally:

   ```pwsh
   npm install -g @github/copilot
   ```

3. Authenticate with `copilot login`. A Copilot entitlement and access to the selected
   models are required. Do not commit authentication state.
4. Verify `copilot --version` and select models available to your account.
   CLI and SDK versions evolve together; use the declared development dependencies.

Run evals via the local runner:

```pwsh
python tests\evals\run_copilot_eval.py copilot/gpt-5-mini smoke:smoke
python tests\evals\run_copilot_eval.py copilot/claude-sonnet-4.5 smoke_copilot:smoke_copilot
python tests\evals\run_copilot_eval.py copilot/gpt-5-mini tests/evals/personas/eval_low_vision.py@at_recall
```

### Hidden answer-key evals ("pop quiz")

Use `answer_key_scorer()` for deterministic checks where the expected
answer must stay out of the model prompt.

These are a good fit for stable persona facts or bounded persona behaviors that
should reliably be triggered by the prompt, such as:

- assistive technology categories for a persona
- distinct persona-specific user types or variants the evaluator must consider
- persona-specific exploration strategies the evaluator must keep in scope
- other closed-set recall where an answer key is clearer than LLM judging
- stable scenario prompts with a bounded set of acceptable persona behaviors

**Per-persona convention:**

- Put deterministic persona modules in `tests/evals/deterministic/<alias>.py`.
- Use one task per section or bounded behavior, with names of the form `<alias>_<section>_deterministic`.
- Prefer the shared builder in `tests/evals/deterministic/_persona.py` so task shape, naming, and hidden-answer-key wiring stay consistent.
- Keep answer keys in `tests/evals/answer_keys/<alias>.json`, with one top-level key per section slug.
- Keep recall slugs aligned with canonical section names such as `at_categories` or `user_variants`.
- Name behavior slugs as `behavior_<mode>_<target>` so future tasks sort and group predictably, for example `behavior_navigation_button`, `behavior_interaction_form`, or `behavior_recovery_form_errors`.

**Deterministic coverage examples (not exhaustive):**

- `low_vision` covers `at_categories`, `persona_types`, `exploration_strategies`, and `user_variants`.
- `blind` covers `at_categories`, `assistive_technologies`, `exploration_strategies`, `user_variants`, `behavior_navigation_button`, `behavior_navigation_main_content`, `behavior_interaction_form`, and `behavior_recovery_form_errors`.
- `color_blind` covers `at_categories`, `assistive_technologies`, `exploration_strategies`, `user_variants`, `behavior_interpretation_state_feedback`, and `behavior_interaction_affordance`.
- `keyboard_only`, `deaf`, `hard_of_hearing`, `without_speech`, and `voice_access` each cover `at_categories`, `exploration_strategies`, `user_variants`, and `baseline_strategies`.

- `limited_reach`, `cognitive_memory`, `cognitive_language`, and `cognitive_numeracy`
  also have maintained deterministic modules and answer-key registries.
- `photosensitive` remains a stub, with a refusal/non-fabrication model task rather than
  invented closed-set recall facts.

**Answer key organization:**

- Store answer keys in per-module registries such as `answer_keys/low_vision.json`, using one top-level key per section slug (for example, `at_categories`).
- Use `load_answer_key()` with a name like `low_vision.at_categories`. `load_answer_key_from_file()` remains as a compatibility wrapper for the shared builder.
- Store the loaded key in `Sample.metadata["answer_key"]`.
- Keep `Sample.target` for plain string or list targets only; `inspect-ai`
  validates that field and will reject arbitrary dicts.
- The default pass threshold is `0.8`, so responses pass at 80% weighted
  coverage or better.

**Behavior-task leniency:**

- For `behavior_*` tasks, expect slight wording differences across supported models even when the underlying persona behavior is correct.
- Make behavior answer keys more alias-rich than fact-recall keys. Include alternate phrasings observed from both current target models instead of overfitting to one exact wording.
- Before treating a behavior-task answer key as stable, run that task against both current supported models: `copilot/gpt-5-mini` and `copilot/claude-sonnet-4.5`.
- Add aliases for equivalent phrasing differences that preserve the same persona behavior. Keep `forbidden_items` focused on genuinely wrong strategies, not harmless wording variation.

**Example answer key registry file** (`answer_keys/low_vision.json`):

```json
{
  "at_categories": {
    "threshold": 0.8,
    "items": [
      {"id": "browser_zoom", "matches": ["browser zoom", "page zoom"]},
      {"id": "magnifier", "matches": ["screen magnifier", "zoomtext"]},
      {"id": "high_contrast", "matches": ["high contrast", "forced colors"]}
    ]
  }
}
```

**Example task using the loader:**

```python
from tests.evals._context import load_persona_by_alias
from tests.evals.deterministic._persona import build_persona_deterministic_task

PERSONA = load_persona_by_alias("low-vision")


@task
def at_categories_deterministic() -> Task:
  return build_persona_deterministic_task(
    persona_slug="low_vision",
    section_slug="at_categories",
    prompt="Name the assistive technology categories described in this persona.",
    persona_prompt=PERSONA,
  )()
```

See `deterministic/low_vision.py` for the complete working example and `answer_keys/low_vision.json` for the corresponding answer-key registry.

**Safety note.** The provider opens a tool-less, single-turn session per
generation: `tools=[]`, `available_tools=[]`, `mcp_servers={}`,
`enable_config_discovery=False`, plus a permission handler that rejects
all requests. The model under test cannot read repository files, run
shell commands, or load repository agent instructions or skills. This boundary
is what makes it acceptable to run benchmarks whose answer keys live in
the same repository.

To target a different model or provider, override these env vars:

| Variable | Purpose |
|---|---|
| `EVAL_MODEL_PRIMARY` | Model under test (default `copilot/gpt-5-mini`) |
| `EVAL_MODEL_SECONDARY` | Mid-tier model (default `copilot/claude-haiku-4.5`) |
| `EVAL_MODEL_CLAUDE` | Claude model (default `copilot/claude-sonnet-4.5`) |
| `EVAL_JUDGE_MODEL` | Judge model for rubric scoring |
| `EVAL_RUBRIC_THRESHOLD` | Pass threshold (default 0.8) |
| `EVAL_QUICK` | `1` to subset parameterized samples |
| `COPILOT_CLI_PATH` | Path to the `copilot` binary (default: resolved from PATH) |

## Running

Shortest launcher (Copilot models):

```pwsh
python -m tests.evals [--persona_context_mode MODE] [--heuristic_context_mode MODE] [--severity_expectation_mode MODE] [--quick] [model] [task ...]
```

`persona_context_mode` options:

- `single` — target persona only
- `all` — full target persona plus compact supporting-persona catalog (default multi-persona mode)
- `medium` — full target persona plus medium supporting-persona briefs

All three modes prepend the complete licensing, responsible-persona-use, and
persona-interpretation methodology documents through `load_eval_persona_context()`. Focused
heuristic evaluators use the same safeguard loader in slim and full modes, and
`sub_agents/_loaders.py` prepends it to every per-heuristic sub-agent system prompt. Low-level
`load_persona_by_alias()` calls return raw persona content; custom prompt builders must wrap that
content with `with_required_persona_safeguards()` or include the three documents explicitly.

`heuristic_context_mode` options (for `heuristics/eval_heuristics_lens.py`):

- `slim` — force slim context injection (`EVAL_FULL_CONTEXT=0`)
- `full` — force full heuristics + full persona injection (`EVAL_FULL_CONTEXT=1`)

`severity_expectation_mode` options (for `heuristics/eval_severity_scale.py`):

- `strict` — authored expected windows
- `benchmark` — widened per-persona windows by ±1

`--quick`:

- sets `EVAL_QUICK=1` for fast subset runs

If a task is a module path without `@task_name` (for example,
`personas/eval_low_vision.py`), the runner executes all tasks in that
module.

Pass multiple task specs to evaluate a list of files in one run.
The legacy `all` group combines persona evals with selected deterministic, negative and
heuristic/methodology tasks; it is not the entire suite. `all-deterministic` runs the original
eight-persona group; pass the cognitive and limited-reach module paths explicitly for additional
coverage. `all-negatives` and `all-other` are selected legacy subsets. Use `all-heuristics`
for heuristic lens + severity scale evals, and `all-methodology` for every methodology eval module.
Use `all-personas` to run every elaborated persona's non-deterministic eval module.

Examples:

```pwsh
python -m tests.evals
python -m tests.evals copilot/gpt-5-mini personas/eval_low_vision.py
python -m tests.evals copilot/gpt-5-mini deterministic/low_vision.py
python -m tests.evals copilot/gpt-5-mini personas/eval_low_vision.py heuristics/eval_heuristic_1.py
python -m tests.evals copilot/gpt-5-mini all-deterministic
python -m tests.evals copilot/gpt-5-mini all-negatives
python -m tests.evals copilot/gpt-5-mini all-other
python -m tests.evals copilot/gpt-5-mini all-heuristics
python -m tests.evals copilot/gpt-5-mini all-methodology
python -m tests.evals copilot/gpt-5-mini all-personas
python -m tests.evals copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
python -m tests.evals --quick copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
python -m tests.evals --heuristic_context_mode slim copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
python -m tests.evals --heuristic_context_mode full copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
python -m tests.evals --quick --heuristic_context_mode full copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
python -m tests.evals copilot/gpt-5-mini heuristics/eval_severity_scale.py
python -m tests.evals copilot/gpt-5-mini heuristics/eval_severity_scale.py@severity_scale_assignment
python -m tests.evals copilot/gpt-5-mini heuristics/eval_severity_scale.py@severity_persona_variance
python -m tests.evals --severity_expectation_mode strict copilot/gpt-5-mini heuristics/eval_severity_scale.py
python -m tests.evals --severity_expectation_mode benchmark copilot/gpt-5-mini heuristics/eval_severity_scale.py
python -m tests.evals copilot/gpt-5-mini all
python -m tests.evals copilot/gpt-5-mini smoke:smoke
python -m tests.evals --persona_context_mode all copilot/gpt-5-mini personas/eval_low_vision.py@at_recall
python -m tests.evals --persona_context_mode medium copilot/gpt-5-mini personas/eval_low_vision.py@at_recall
python -m tests.evals copilot/claude-sonnet-4.5 personas/eval_low_vision.py@at_recall
python -m tests.evals copilot/claude-sonnet-4.5 deterministic/low_vision.py
python -m tests.evals copilot/claude-sonnet-4.5 tests/evals/personas/eval_low_vision.py@at_recall
```

All elaborated persona evals (Phase 2.5a):

**PowerShell:**

```pwsh
python -m tests.evals copilot/gpt-5-mini `
  personas/eval_blind.py `
  personas/eval_color_blind.py `
  personas/eval_deaf.py `
  personas/eval_hard_of_hearing.py `
  personas/eval_without_speech.py `
  personas/eval_keyboard_only.py `
  personas/eval_voice_access.py
```

**Bash:**

```bash
python -m tests.evals copilot/gpt-5-mini \
  personas/eval_blind.py \
  personas/eval_color_blind.py \
  personas/eval_deaf.py \
  personas/eval_hard_of_hearing.py \
  personas/eval_without_speech.py \
  personas/eval_keyboard_only.py \
  personas/eval_voice_access.py
```

Smoke test (one Sample, fastest sanity check):

```pwsh
python -m inspect_ai eval tests/evals/smoke.py --model copilot/gpt-5-mini
```

Legacy combined task group (not every LLM task):

```pwsh
python -m tests.evals copilot/gpt-5-mini all
```

Legacy eight-persona deterministically scored model subset:

```pwsh
python -m tests.evals copilot/gpt-5-mini all-deterministic
```

Selected heuristic/methodology subset:

```pwsh
python -m tests.evals copilot/gpt-5-mini all-other
```

Heuristic-only subset (heuristic lens + severity scale; excludes `eval_heuristic_1.py`):

```pwsh
python -m tests.evals copilot/gpt-5-mini all-heuristics
```

All methodology evals:

```pwsh
python -m tests.evals copilot/gpt-5-mini all-methodology
```

All elaborated personas, non-deterministic evals only:

```pwsh
python -m tests.evals copilot/gpt-5-mini all-personas
```

Heuristic lens matrix eval (default slim context):

```pwsh
python -m tests.evals copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
```

Heuristic lens matrix eval with explicit runner mode (slim or full):

```pwsh
python -m tests.evals --heuristic_context_mode slim copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
python -m tests.evals --heuristic_context_mode full copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
```

Heuristic lens matrix eval in quick mode (10 cells):

```pwsh
python -m tests.evals --quick copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
```

Heuristic lens matrix eval in full-context mode:

```pwsh
$env:EVAL_FULL_CONTEXT = "1"
python -m tests.evals copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
```

Heuristic lens matrix eval with quick + full-context mode:

```pwsh
python -m tests.evals --quick --heuristic_context_mode full copilot/gpt-5-mini heuristics/eval_heuristics_lens.py
```

Severity-scale evals (both `severity_scale_assignment` and `severity_persona_variance`):

```pwsh
python -m tests.evals copilot/gpt-5-mini heuristics/eval_severity_scale.py
```

Single severity task:

```pwsh
python -m tests.evals copilot/gpt-5-mini heuristics/eval_severity_scale.py@severity_scale_assignment
python -m tests.evals copilot/gpt-5-mini heuristics/eval_severity_scale.py@severity_persona_variance
```

Severity-scale evals in benchmark expectation mode (widens per-persona windows by ±1):

```pwsh
python -m tests.evals --severity_expectation_mode benchmark copilot/gpt-5-mini heuristics/eval_severity_scale.py
```

Severity-scale evals in strict expectation mode:

```pwsh
python -m tests.evals --severity_expectation_mode strict copilot/gpt-5-mini heuristics/eval_severity_scale.py
```

Env-var equivalents (still supported for compatibility):

```pwsh
$env:EVAL_QUICK = "1"
$env:EVAL_FULL_CONTEXT = "1"
$env:EVAL_SEVERITY_EXPECTATION_MODE = "benchmark"
```

Severity-scale evals via Copilot/Claude:

```pwsh
python -m tests.evals copilot/claude-sonnet-4.5 heuristics/eval_severity_scale.py
```

Equivalent explicit file list:

```pwsh
python -m tests.evals copilot/gpt-5-mini `
  personas/eval_low_vision.py `
  deterministic/low_vision.py `
  heuristics/eval_heuristic_1.py `
  methodology/eval_confidence_gate.py `
  negative/eval_privacy_clause.py
```

Single sub-task:

```pwsh
python -m inspect_ai eval tests/evals/personas/eval_low_vision.py@at_recall `
  --model copilot/gpt-5-mini
```

Unified runner (works in both modes):

```pwsh
python -m tests.evals copilot/gpt-5-mini personas/eval_low_vision.py@at_recall
python -m tests.evals copilot/claude-sonnet-4.5 personas/eval_low_vision.py@at_recall
python -m tests.evals copilot/gpt-5-mini deterministic/low_vision.py
python -m tests.evals copilot/claude-sonnet-4.5 deterministic/low_vision.py
```

Low-vision persona eval with all-persona background context:

```pwsh
python -m tests.evals --persona_context_mode all `
  copilot/gpt-5-mini `
  personas/eval_low_vision.py@at_recall
```

Low-vision persona eval with medium supporting briefs:

```pwsh
python -m tests.evals --persona_context_mode medium `
  copilot/gpt-5-mini `
  personas/eval_low_vision.py@at_recall
```

Offline validation (no LLM, no authentication):

```pwsh
python tests/validate_structure.py
python -m pytest tests/validate_structure.py tests -q
```

## Source modes

`PERSONA_SOURCE=md` (default) loads the authoring Markdown, including inline baseline copies.
`PERSONA_SOURCE=schema` loads generated YAML and merges applicable baseline items for
elaborated personas only. Stubs remain minimal. Set the source before running a task; invalid
values are reported as errors. Supporting multi-persona summaries remain Markdown-based.

```sh
PERSONA_SOURCE=schema python -m pytest tests/test_schema_loading.py tests/test_prompt_safeguards.py tests/evals/sub_agents/test_per_heuristic_loading.py -q
```

In PowerShell, set `$env:PERSONA_SOURCE = "schema"` first and remove it after the command.
The [PowerShell wrappers](../../scripts/) also accept a YAML persona selector where supported.
Their dry-run mode prints commands without starting a model session; the wrappers locate either
a Windows or POSIX virtual environment and create the ignored log directory on first use.

## Data flow and artifacts

Model evaluations send assembled reference content, task examples and image attachments to the
selected Copilot/model service. Rubric judging also sends the model response and rubric to the
judge. Tool-less sessions prevent repository/tool access, not disclosure of supplied prompts.
Use only approved, redistributable examples; do not supply private customer data, credentials
or identifying screenshots. See the [original synthetic fixtures](../fixtures/images/README.md).

Inspect logs can contain prompts, outputs, rubric results, model identifiers and usage data.
Keep `logs/` and local authentication/environment files out of source control and public bundles.
Delete specific unneeded log files deliberately; do not publish a log just because its eval passed.
Generation and judging can consume paid quota and incur cost; start with one task or `--quick`.
Record Python, dependency, CLI and model versions with results, since dependencies are not locked.

## Viewing `.eval` files

Inspect writes eval results to binary `.eval` log files (typically in
`logs/`). Use the commands below to inspect them.

Interactive viewer (browse all logs in `logs/`):

```pwsh
python -m inspect_ai view start --log-dir logs
```

List available logs:

```pwsh
python -m inspect_ai log list --log-dir logs
```

Print one `.eval` file as JSON in the terminal:

```pwsh
python -m inspect_ai log dump logs/<your-log-file>.eval
```

Convert `.eval` to `.json` for sharing or offline inspection:

```pwsh
python -m inspect_ai log convert logs/<your-log-file>.eval --to json
```

## Cost note

Each rubric scorer issues one judge-model call per sample. The pilot
runs ~10 samples plus a judge call per sample, so a full pilot pass
is roughly 20 model calls. GitHub Models' free tier rate-limits
aggressively; if you hit limits, run modules one at a time or set
`EVAL_QUICK=1`.

## Related

- [tests/validate_structure.py](../validate_structure.py) — fast,
  schema-level validation of the markdown files. Always run this
  before committing changes to `personas/` or `heuristics/`.
