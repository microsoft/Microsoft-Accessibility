# Run persona evals (tests/evals/personas/) across all models.
param(
    [ValidateRange(1, 1000)]
    [int]$SamplesPerTest = 5,

    # Path to a persona YAML file (e.g. schemas/4.2.1-blind.persona.yaml) or a bare alias (e.g. blind).
    [string]$Persona,

    [string[]]$TaskSpecs,

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

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).ProviderPath

if (-not $TaskSpecs) {
    if ($Persona) {
        $alias = Resolve-PersonaAlias -PersonaInput $Persona -RepoRoot $repoRoot
        $evalsRoot = Join-Path $repoRoot 'tests\evals'
        $spec = "personas/eval_${alias}.py"
        $fullPath = Join-Path $evalsRoot ($spec -replace '/', '\')
        if (-not (Test-Path $fullPath)) {
            throw "Persona eval not found: $spec (searched $fullPath)"
        }
        $TaskSpecs = @($spec)
    } else {
        # Default: all persona evals
        $evalsRoot = Join-Path $repoRoot 'tests\evals\personas'
        $TaskSpecs = @(Get-ChildItem -Path $evalsRoot -Filter "eval_*.py" -File | ForEach-Object { "personas/$($_.Name)" })
    }
}

$personaSource = "md"
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
