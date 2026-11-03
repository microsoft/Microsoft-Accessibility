# Run all eval harnesses (personas, deterministic, negative) across all models.
# For running individual harnesses, use the focused scripts:
#   run-persona-evals.ps1, run-deterministic-evals.ps1, run-negative-evals.ps1
param(
    [ValidateRange(1, 1000)]
    [int]$SamplesPerTest = 5,

    # Path to a persona YAML file (e.g. schemas/4.2.1-blind.persona.yaml) or a bare alias (e.g. blind).
    # When set, TaskSpecs is auto-populated from matching evals in personas/, deterministic/, and negative/.
    [string]$Persona,

    # Run only the personas/ eval for the resolved persona, skipping deterministic/ and negative/.
    [switch]$SingleTask,

    [string[]]$TaskSpecs = @("personas/eval_keyboard_only.py"),

    [string[]]$Models = @(
        "copilot/gpt-5.6-sol",
        "copilot/gpt-5-mini",
        "copilot/claude-sonnet-5",
        "copilot/claude-sonnet-4.6",
        "copilot/claude-opus-4.6",
        "copilot/claude-haiku-4.5",
        "copilot/mai-code-1-flash-picker",
        "copilot/gemini-3.1-pro-preview"
    ),

    [ValidateSet("single", "medium", "all")]
    [string]$PersonaContextMode = "single",

    [ValidateSet("slim", "full")]
    [string]$HeuristicContextMode,

    [ValidateSet("strict", "benchmark")]
    [string]$SeverityExpectationMode,

    [hashtable]$JudgeOverrides = @{
        "copilot/gpt-5-mini" = "copilot/claude-opus-4.6"
    },

    [switch]$Quick,

    [switch]$DryRun
)

. (Join-Path $PSScriptRoot "_eval-base.ps1")

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).ProviderPath

if ($Persona) {
    $alias = Resolve-PersonaAlias -PersonaInput $Persona -RepoRoot $repoRoot
    $evalsRoot = Join-Path $repoRoot 'tests\evals'
    $candidates = @(
        "personas/eval_${alias}.py",
        "deterministic/${alias}.py",
        "negative/eval_${alias}_difficulties.py"
    )
    if ($SingleTask) { $candidates = @($candidates[0]) }

    $found = @()
    foreach ($spec in $candidates) {
        $fullPath = Join-Path $evalsRoot ($spec -replace '/', '\')
        if (Test-Path $fullPath) {
            $found += $spec
        } else {
            Write-Host "Skipping (not found): $spec"
        }
    }

    if ($found.Count -eq 0) {
        throw "No eval files found for persona '$alias'. Searched in tests/evals/{personas,deterministic,negative}."
    }
    $TaskSpecs = $found
}

$personaSource = if ($env:PERSONA_SOURCE -and $env:PERSONA_SOURCE.Trim()) { $env:PERSONA_SOURCE.Trim().ToLowerInvariant() } else { "md" }
if ($Persona -and $Persona -match '\.ya?ml$') {
    $personaSource = "schema"
}

$invokeParams = @{
    SamplesPerTest     = $SamplesPerTest
    TaskSpecs          = $TaskSpecs
    Models             = $Models
    PersonaContextMode = $PersonaContextMode
    JudgeOverrides     = $JudgeOverrides
    Quick              = $Quick
    DryRun             = $DryRun
    PersonaSource      = $personaSource
}
if ($HeuristicContextMode) { $invokeParams.HeuristicContextMode = $HeuristicContextMode }
if ($SeverityExpectationMode) { $invokeParams.SeverityExpectationMode = $SeverityExpectationMode }

$exitCode = Invoke-EvalSuite @invokeParams

exit $exitCode
