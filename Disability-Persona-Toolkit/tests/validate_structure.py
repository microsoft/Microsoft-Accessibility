"""Validate the structural consistency of Disability Persona Toolkit (DPT) files.

Checks:
- Canonical YAML persona schema structure and provenance
- YAML frontmatter schema in all persona files
- Required H2 sections in elaborated personas
- Baseline content consistency across persona files
- Heuristic lens override IDs reference valid heuristic numbers
- Stub personas have required minimal structure

Can run as:
  python tests/validate_structure.py
  pytest tests/validate_structure.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parent.parent
GOVERNANCE_ROOT = REPO_ROOT.parent
PERSONAS_DIR = REPO_ROOT / "personas"
SCHEMAS_DIR = REPO_ROOT / "schemas"
HEURISTICS_DIR = REPO_ROOT / "heuristics"
METHODOLOGY_DIR = REPO_ROOT / "methodology"
STANDARDS_DIR = REPO_ROOT / "standards"

REQUIRED_FRONTMATTER_FIELDS = {"clause", "title", "alias", "status"}
VALID_STATUSES = {"elaborated", "stub"}
VALID_HEURISTIC_IDS = set(range(1, 11))
COGA_PERSONAS = {
    "4.2.10-cognitive-memory.md",
    "4.2.10b-cognitive-language.md",
    "4.2.10c-cognitive-numeracy.md",
}
COGA_SCHEMAS = {
    "4.2.10-cognitive-memory.persona.yaml",
    "4.2.10b-cognitive-language.persona.yaml",
    "4.2.10c-cognitive-numeracy.persona.yaml",
}
COGA_SOURCE_URLS = {
    "https://www.w3.org/TR/coga-usable/",
    "https://www.w3.org/TR/2026/DNOTE-coga-research-modules-20260205/",
}
COGA_REQUIRED_NOTICES = (
    'This software or document includes material copied from or derived from '
    '"Making Content Usable for People with Cognitive and Learning Disabilities" '
    '(<https://www.w3.org/TR/coga-usable/>). Copyright © 2021 W3C® '
    '(MIT, ERCIM, Keio, Beihang).',
    'This software or document includes material copied from or derived from '
    '"Cognitive Accessibility Research Modules" '
    '(<https://www.w3.org/TR/2026/DNOTE-coga-research-modules-20260205/>). '
    'Copyright © 2026 World Wide Web Consortium. '
    '<https://www.w3.org/copyright/software-license-2023/>',
)
W3C_SOFTWARE_LICENSE_SECTION_HASHES = {
    "W3C Software and Document License — 2015 version": (
        "34e42464894a3ef240de95b8178dca73f110df4305eee313f810837571ead1df"
    ),
    "W3C Software and Document License — 2023 version": (
        "90024cfac00df2e0beadb08f24d53b3f97b7bd0ed18a0976084fe7c014e751c5"
    ),
}
INTERPRETATION_REQUIRED_TEXT = (
    "Preserve qualifiers",
    "Do not compress multiple strategies into one supposedly universal behavior",
    "Avoid deficit framing",
    "do not replace research with the intended audience",
)
REQUIRED_CODEOWNERS = (
    "@aarongustafson",
    "@ferbonnin",
)
PROMPT_BEARING_CODEOWNER_PATHS = (
    "/Disability-Persona-Toolkit/",
    "/Disability-Persona-Toolkit/schemas/",
    "/Disability-Persona-Toolkit/personas/",
    "/Disability-Persona-Toolkit/heuristics/",
    "/Disability-Persona-Toolkit/methodology/",
    "/Disability-Persona-Toolkit/standards/",
    "/Disability-Persona-Toolkit/provenance.json",
    "/Disability-Persona-Toolkit/LICENSE.txt",
    "/Disability-Persona-Toolkit/tests/validate_structure.py",
    "/Disability-Persona-Toolkit/tests/evals/",
    "/Disability-Persona-Toolkit/tests/fixtures/",
    "/Disability-Persona-Toolkit/scripts/",
    "/Disability-Persona-Toolkit/AGENTS.md",
    "/Disability-Persona-Toolkit/README.md",
    "/Disability-Persona-Toolkit/CONTRIBUTING.md",
    "/.github/workflows/dpt-validate.yml",
    "/.github/CODEOWNERS",
    "/.github/PULL_REQUEST_TEMPLATE.md",
    "/.github/instructions/dpt.instructions.md",
    "/.github/skills/persona-to-schema/",
)
CONDITIONAL_LANGUAGE = re.compile(
    r"\b(?:may|can|could|often|sometimes|some users|can vary|varies|depending on|not all)\b",
    re.IGNORECASE,
)

REQUIRED_ELABORATED_SECTIONS = [
    "Persona Prompt",
    "Assistive Technologies",
    "Exploration Strategies",
    "User Variants",
    "Learning Considerations",
    "Heuristic Lens Overrides",
]
REQUIRED_SCHEMA_FIELDS = {
    "clause",
    "title",
    "alias",
    "status",
    "fps_statement",
}
REQUIRED_ELABORATED_SCHEMA_FIELDS = {
    "prompt",
    "assistive_tech",
    "strategies",
    "user_variants",
    "learning",
    "heuristic_overrides",
}


def parse_frontmatter(path: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def get_h2_sections(path: Path) -> list[str]:
    """Extract H2 section titles from a markdown file."""
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^## (.+)$", text, re.MULTILINE)


def get_h3_sections(path: Path, under_h2: str) -> list[str]:
    """Extract H3 section titles under a specific H2."""
    text = path.read_text(encoding="utf-8")
    # Find content between the target H2 and the next H2 (or end of file)
    pattern = rf"^## {re.escape(under_h2)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    section_text = match.group(1)
    return re.findall(r"^### (.+)$", section_text, re.MULTILINE)


def get_baseline_content_markers(path: Path) -> list[str]:
    """Find all *(from baseline)* markers in a persona file."""
    text = path.read_text(encoding="utf-8")
    return re.findall(r"\*\(from baseline\)\*", text)


def get_persona_files() -> list[Path]:
    """Get all persona files (excluding _baseline.md)."""
    return sorted(
        p for p in PERSONAS_DIR.glob("4.2.*-*.md")
        if p.name != "_baseline.md"
    )


def get_schema_files() -> list[Path]:
    """Get canonical YAML persona schemas."""
    return sorted(SCHEMAS_DIR.glob("*.persona.yaml"))


@lru_cache(maxsize=None)
def _schema_validator(status: str) -> Draft202012Validator:
    """Load the canonical JSON Schema validator for a persona status."""
    schema_name = "persona.schema.json" if status == "elaborated" else "persona-stub.schema.json"
    schema = json.loads((SCHEMAS_DIR / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


class ValidationError:
    def __init__(self, file: str, message: str):
        self.file = file
        self.message = message

    def __str__(self):
        return f"{self.file}: {self.message}"


def _validate_provenance_object(
    file_name: str,
    provenance: object,
) -> list[ValidationError]:
    """Validate source metadata shared by Markdown and YAML representations."""
    if not isinstance(provenance, dict):
        return [ValidationError(file_name, "Missing provenance object")]

    errors = []
    source_urls = provenance.get("source_urls")
    if not isinstance(source_urls, list) or set(source_urls) != COGA_SOURCE_URLS:
        errors.append(ValidationError(file_name, "Provenance has incorrect source_urls"))
    expected = {
        "upstream_license": "W3C Software and Document License",
        "repository_license": "MIT",
        "required_notice": "personas/cognitive-sources.LICENSE.md",
        "adaptation": True,
    }
    for field, value in expected.items():
        if provenance.get(field) != value:
            errors.append(ValidationError(
                file_name,
                f"Provenance field {field!r} must be {value!r}",
            ))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(provenance.get("reviewed_on", ""))):
        errors.append(ValidationError(file_name, "Provenance reviewed_on must be YYYY-MM-DD"))

    notice_path = REPO_ROOT / str(provenance.get("required_notice", ""))
    if not notice_path.is_file():
        errors.append(ValidationError(file_name, "Required provenance notice is missing"))
    return errors


def validate_schema(path: Path) -> list[ValidationError]:
    """Validate canonical persona YAML used by downstream distributions."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [ValidationError(path.name, f"Cannot read persona schema: {exc}")]
    if not isinstance(data, dict):
        return [ValidationError(path.name, "Persona schema must be a mapping")]

    errors = []
    missing = REQUIRED_SCHEMA_FIELDS - set(data)
    if missing:
        errors.append(ValidationError(path.name, f"Missing schema fields: {missing}"))
    status = data.get("status")
    if status not in VALID_STATUSES:
        errors.append(ValidationError(path.name, f"Invalid schema status: {status!r}"))
        return errors

    schema_errors = sorted(
        _schema_validator(status).iter_errors(data),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    for error in schema_errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(
            ValidationError(
                path.name,
                f"JSON Schema violation at {location}: {error.message}",
            )
        )
    if schema_errors:
        return errors

    if status == "elaborated":
        missing = REQUIRED_ELABORATED_SCHEMA_FIELDS - set(data)
        if missing:
            errors.append(ValidationError(path.name, f"Missing elaborated schema fields: {missing}"))
        for field in ("assistive_tech", "strategies", "user_variants", "learning"):
            value = data.get(field)
            if not isinstance(value, list) or not value:
                errors.append(ValidationError(path.name, f"{field} must be a non-empty list"))
        prompt = data.get("prompt")
        if not isinstance(prompt, dict) or not prompt.get("role") or not prompt.get("checklist"):
            errors.append(ValidationError(path.name, "prompt must include role and checklist"))
        overrides = data.get("heuristic_overrides")
        if not isinstance(overrides, dict) or set(map(str, overrides)) != {
            str(value) for value in VALID_HEURISTIC_IDS
        }:
            errors.append(ValidationError(
                path.name,
                "heuristic_overrides must define every heuristic from 1 through 10",
            ))
        variation = yaml.safe_dump(
            {
                field: data.get(field, [])
                for field in ("assistive_tech", "strategies", "user_variants", "learning")
            },
            sort_keys=False,
        )
        if not CONDITIONAL_LANGUAGE.search(variation):
            errors.append(ValidationError(
                path.name,
                "Schema variation content lacks conditional language",
            ))

    if path.name in COGA_SCHEMAS:
        errors.extend(_validate_provenance_object(path.name, data.get("provenance")))
        for variant in data.get("user_variants", []):
            behavior = str(variant.get("behavior", ""))
            if not CONDITIONAL_LANGUAGE.search(behavior):
                errors.append(ValidationError(
                    path.name,
                    f"User variant {variant.get('id', '<unknown>')!r} lacks conditional language",
                ))
    elif "provenance" in data:
        errors.append(ValidationError(
            path.name,
            "Unexpected provenance on a persona not listed in provenance.json",
        ))
    return errors


def validate_frontmatter(path: Path) -> list[ValidationError]:
    """Validate frontmatter schema."""
    errors = []
    fm = parse_frontmatter(path)
    if fm is None:
        errors.append(ValidationError(path.name, "Missing YAML frontmatter"))
        return errors

    missing = REQUIRED_FRONTMATTER_FIELDS - set(fm.keys())
    if missing:
        errors.append(ValidationError(path.name, f"Missing frontmatter fields: {missing}"))

    if "status" in fm and fm["status"] not in VALID_STATUSES:
        errors.append(ValidationError(
            path.name,
            f"Invalid status '{fm['status']}'. Must be one of: {VALID_STATUSES}"
        ))

    if "baseline_excludes" in fm and not isinstance(fm["baseline_excludes"], list):
        errors.append(ValidationError(
            path.name,
            "baseline_excludes must be a list"
        ))

    return errors


def validate_elaborated_sections(path: Path) -> list[ValidationError]:
    """Validate that elaborated personas have all required H2 sections."""
    errors = []
    fm = parse_frontmatter(path)
    if fm is None or fm.get("status") != "elaborated":
        return errors

    sections = get_h2_sections(path)
    for required in REQUIRED_ELABORATED_SECTIONS:
        if required not in sections:
            errors.append(ValidationError(
                path.name,
                f"Missing required section: ## {required}"
            ))

    return errors


def _section_content(path: Path, heading: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.DOTALL)
    match = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    return re.sub(r"^#{1,6}\s.*$", "", match.group(1), flags=re.MULTILINE).strip()


def validate_persona_nuance(path: Path) -> list[ValidationError]:
    """Require substantive variation sections and conditional language."""
    errors = []
    fm = parse_frontmatter(path)
    if fm is None or fm.get("status") != "elaborated":
        return errors

    contents = []
    for section in (
        "Assistive Technologies",
        "Exploration Strategies",
        "User Variants",
        "Learning Considerations",
    ):
        content = _section_content(path, section)
        if content is None:
            continue
        if not re.search(r"[a-z0-9]", content, re.IGNORECASE):
            errors.append(ValidationError(path.name, f"Empty section: ## {section}"))
        contents.append(content)

    if contents and not CONDITIONAL_LANGUAGE.search("\n".join(contents)):
        errors.append(ValidationError(
            path.name,
            "Variation sections lack conditional language such as 'may' or 'some users'",
        ))
    return errors


def validate_provenance(path: Path) -> list[ValidationError]:
    """Validate machine-readable provenance for known adapted personas."""
    if path.name not in COGA_PERSONAS:
        return []
    fm = parse_frontmatter(path) or {}
    provenance = fm.get("provenance")
    errors = _validate_provenance_object(path.name, provenance)
    if (
        isinstance(provenance, dict)
        and str(provenance.get("required_notice", "")) not in path.read_text(encoding="utf-8")
    ):
        errors.append(ValidationError(path.name, "Persona does not reference its provenance notice"))
    return errors


def validate_coga_notice(coga_notice: str) -> list[ValidationError]:
    """Validate complete, version-specific W3C notices for adapted COGA material."""
    errors = []
    normalized_notice = " ".join(coga_notice.split())
    for value in (*COGA_SOURCE_URLS, *COGA_REQUIRED_NOTICES):
        if " ".join(value.split()) not in normalized_notice:
            errors.append(ValidationError(
                "personas/cognitive-sources.LICENSE.md",
                f"Missing or incorrect W3C notice: {value}",
            ))

    for heading, expected_hash in W3C_SOFTWARE_LICENSE_SECTION_HASHES.items():
        section_match = re.search(
            rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
            coga_notice,
            re.MULTILINE | re.DOTALL,
        )
        if not section_match:
            errors.append(ValidationError(
                "personas/cognitive-sources.LICENSE.md",
                f"Missing W3C license section: {heading}",
            ))
            continue
        normalized_section = " ".join(section_match.group(1).split())
        actual_hash = hashlib.sha256(normalized_section.encode("utf-8")).hexdigest()
        if actual_hash != expected_hash:
            errors.append(ValidationError(
                "personas/cognitive-sources.LICENSE.md",
                f"{heading} complete normalized license text differs from the canonical copy",
            ))

    obsolete_2026_notice = "Copyright © 2026 W3C® (MIT, ERCIM, Keio, Beihang)"
    if obsolete_2026_notice in coga_notice:
        errors.append(ValidationError(
            "personas/cognitive-sources.LICENSE.md",
            "The 2026 source uses the obsolete 2015 copyright-holder form",
        ))
    return errors


def validate_interpretation_guidance(text: str) -> list[ValidationError]:
    """Require the policy statements that bound stereotype-prone persona use."""
    errors = []
    normalized = " ".join(text.split())
    for value in INTERPRETATION_REQUIRED_TEXT:
        if " ".join(value.split()).lower() not in normalized.lower():
            errors.append(ValidationError(
                "methodology/persona-interpretation.md",
                f"Missing required interpretation safeguard: {value}",
            ))
    return errors


def validate_codeowners(text: str) -> list[ValidationError]:
    """Require owner review for every source of AI-consumed repository content."""
    errors = []
    entries = {
        parts[0]: parts[1:]
        for line in text.splitlines()
        if (parts := line.split()) and not parts[0].startswith("#")
    }
    for path in PROMPT_BEARING_CODEOWNER_PATHS:
        owners = entries.get(path, [])
        for owner in REQUIRED_CODEOWNERS:
            if owner not in owners:
                errors.append(ValidationError(
                    ".github/CODEOWNERS",
                    f"{path} must require {owner}",
                ))
    return errors


def validate_cross_cutting_controls() -> list[ValidationError]:
    """Validate controls that must travel with persona and standards content."""
    errors = []
    license_text = (REPO_ROOT / "LICENSE.txt").read_text(encoding="utf-8")
    licensing_path = METHODOLOGY_DIR / "licensing.md"
    responsible_path = METHODOLOGY_DIR / "responsible-persona-use.md"
    interpretation_path = METHODOLOGY_DIR / "persona-interpretation.md"
    for path in (licensing_path, responsible_path, interpretation_path):
        if not path.is_file():
            errors.append(ValidationError(str(path.relative_to(REPO_ROOT)), "Required methodology missing"))

    if licensing_path.is_file() and license_text not in licensing_path.read_text(encoding="utf-8"):
        errors.append(ValidationError(
            "methodology/licensing.md",
            "Does not embed the repository MIT license verbatim",
        ))
    if responsible_path.is_file():
        responsible = responsible_path.read_text(encoding="utf-8")
        for phrase in (
            "infer whether an identifiable person has a disability",
            "At 200% zoom",
            "The employee is a person with low vision",
        ):
            if phrase not in responsible:
                errors.append(ValidationError(
                    "methodology/responsible-persona-use.md",
                    f"Missing required safeguard: {phrase}",
                ))
    if interpretation_path.is_file():
        errors.extend(validate_interpretation_guidance(
            interpretation_path.read_text(encoding="utf-8")
        ))

    codeowners_path = GOVERNANCE_ROOT / ".github" / "CODEOWNERS"
    if not codeowners_path.is_file():
        errors.append(ValidationError(".github/CODEOWNERS", "Required owner policy missing"))
    else:
        errors.extend(validate_codeowners(codeowners_path.read_text(encoding="utf-8")))
    pr_template = GOVERNANCE_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
    if not pr_template.is_file():
        errors.append(ValidationError(
            ".github/PULL_REQUEST_TEMPLATE.md",
            "Required review checklist missing",
        ))
    else:
        template_text = pr_template.read_text(encoding="utf-8")
        for phrase in (
            "AI-consumed content security",
            "override consumer policy",
            "pin an immutable commit or submodule revision",
        ):
            if phrase not in template_text:
                errors.append(ValidationError(
                    ".github/PULL_REQUEST_TEMPLATE.md",
                    f"Missing prompt-content review check: {phrase}",
                ))

    baseline = (PERSONAS_DIR / "_baseline.md").read_text(encoding="utf-8")
    if "Do not infer" not in baseline or "responsible-persona-use.md" not in baseline:
        errors.append(ValidationError(
            "personas/_baseline.md",
            "Missing responsible persona-use reminder",
        ))

    coga_notice_path = PERSONAS_DIR / "cognitive-sources.LICENSE.md"
    coga_notice = coga_notice_path.read_text(encoding="utf-8")
    errors.extend(validate_coga_notice(coga_notice))

    wcag_path = STANDARDS_DIR / "wcag-requirements.md"
    wcag_notice = STANDARDS_DIR / "wcag-requirements.LICENSE.md"
    wcag = wcag_path.read_text(encoding="utf-8")
    if not wcag_notice.is_file():
        errors.append(ValidationError(str(wcag_notice.relative_to(REPO_ROOT)), "Required notice missing"))
    for value in (
        "wcag-requirements.LICENSE.md",
        "https://www.w3.org/TR/WCAG22/",
        "not the authoritative specification",
    ):
        if value not in wcag:
            errors.append(ValidationError(
                "standards/wcag-requirements.md",
                f"Missing distribution warning: {value}",
            ))

    manifest_path = REPO_ROOT / "provenance.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(ValidationError("provenance.json", f"Cannot read manifest: {exc}"))
        return errors
    errors.extend(validate_distribution_manifest(manifest))
    return errors


def validate_distribution_manifest(manifest: object) -> list[ValidationError]:
    """Check packaged representations and notices relative to the resource root."""
    errors = []
    if not isinstance(manifest, dict):
        return [ValidationError("provenance.json", "Manifest must be an object")]
    materials = manifest.get("materials")
    if manifest.get("schemaVersion") != 1 or not isinstance(materials, list):
        errors.append(ValidationError("provenance.json", "Invalid manifest shape"))
        return errors
    ids = set()
    for material in materials:
        if not isinstance(material, dict):
            return [ValidationError("provenance.json", "Material must be an object")]
        material_id = material.get("id")
        if not isinstance(material_id, str) or not material_id or material_id in ids:
            errors.append(ValidationError("provenance.json", "Material IDs must be unique non-empty strings"))
        else:
            ids.add(material_id)
        content = material.get("content")
        if not isinstance(content, list) or not content or not all(isinstance(path, str) for path in content):
            errors.append(ValidationError("provenance.json", "Material content must list file paths"))
            continue
        source_urls = material.get("sourceUrls")
        if not isinstance(source_urls, list) or not all(isinstance(url, str) for url in source_urls):
            errors.append(ValidationError("provenance.json", "Material sourceUrls must be a list of strings"))
        paths = content + [material.get("requiredNotice"), material.get("requiredRepositoryNotice")]
        for value in paths:
            if not isinstance(value, str) or not value or Path(value).is_absolute() or ".." in Path(value).parts:
                errors.append(ValidationError("provenance.json", f"Invalid resource-relative path: {value!r}"))
            elif not (REPO_ROOT / value).is_file():
                errors.append(ValidationError("provenance.json", f"Required distribution file missing: {value}"))
    if errors:
        return errors
    coga = next((item for item in materials if item.get("id") == "w3c-coga-personas"), None)
    if not isinstance(coga, dict):
        errors.append(ValidationError("provenance.json", "Missing w3c-coga-personas material"))
        return errors
    if set(coga.get("content", [])) != (
        {f"schemas/{name}" for name in COGA_SCHEMAS}
        | {f"personas/{name}" for name in COGA_PERSONAS}
    ):
        errors.append(ValidationError("provenance.json", "COGA content paths are incomplete"))
    if set(coga.get("sourceUrls", [])) != COGA_SOURCE_URLS:
        errors.append(ValidationError("provenance.json", "COGA source URLs are incorrect"))
    for field, value in {
        "requiredNotice": "personas/cognitive-sources.LICENSE.md",
        "requiredRepositoryNotice": "LICENSE.txt",
        "upstreamLicense": "W3C Software and Document License",
        "repositoryLicense": "MIT",
        "adaptation": True,
    }.items():
        if coga.get(field) != value:
            errors.append(ValidationError(
                "provenance.json",
                f"Field {field!r} must be {value!r}",
            ))
    wcag = next((item for item in materials if item.get("id") == "w3c-wcag-reference"), None)
    if not isinstance(wcag, dict):
        errors.append(ValidationError("provenance.json", "Missing w3c-wcag-reference material"))
    else:
        expected = {
            "content": ["standards/wcag-requirements.md"],
            "requiredNotice": "standards/wcag-requirements.LICENSE.md",
            "requiredRepositoryNotice": "LICENSE.txt",
            "sourceUrls": ["https://www.w3.org/TR/WCAG22/"],
            "upstreamLicense": "W3C Document License (2023)",
            "repositoryLicense": "MIT",
            "adaptation": True,
        }
        for field, value in expected.items():
            if wcag.get(field) != value:
                errors.append(ValidationError("provenance.json", f"WCAG field {field!r} must be {value!r}"))
    return errors


def validate_heuristic_overrides(path: Path) -> list[ValidationError]:
    """Validate heuristic lens override IDs are valid (1-10)."""
    errors = []
    fm = parse_frontmatter(path)
    if fm is None or fm.get("status") != "elaborated":
        return errors

    h3s = get_h3_sections(path, "Heuristic Lens Overrides")
    for h3 in h3s:
        # Extract heuristic number from "Heuristic N — ..."
        match = re.match(r"Heuristic (\d+)", h3)
        if match:
            hid = int(match.group(1))
            if hid not in VALID_HEURISTIC_IDS:
                errors.append(ValidationError(
                    path.name,
                    f"Invalid heuristic ID {hid} in lens overrides. Valid: 1-10"
                ))
        else:
            errors.append(ValidationError(
                path.name,
                f"Heuristic lens override '{h3}' doesn't match expected format 'Heuristic N — ...'"
            ))

    return errors


def validate_baseline_consistency() -> list[ValidationError]:
    """Check that all elaborated personas include baseline content markers."""
    errors = []
    for path in get_persona_files():
        fm = parse_frontmatter(path)
        if fm is None or fm.get("status") != "elaborated":
            continue

        markers = get_baseline_content_markers(path)
        if not markers:
            errors.append(ValidationError(
                path.name,
                "Elaborated persona has no '*(from baseline)*' markers — "
                "baseline content may not be included"
            ))

    return errors


def validate_stub_structure(path: Path) -> list[ValidationError]:
    """Validate that stub personas have minimal required structure."""
    errors = []
    fm = parse_frontmatter(path)
    if fm is None or fm.get("status") != "stub":
        return errors

    text = path.read_text(encoding="utf-8")
    if not re.search(r"^# ", text, re.MULTILINE):
        errors.append(ValidationError(path.name, "Stub persona missing H1 title"))

    return errors


def run_validation() -> list[ValidationError]:
    """Run all validations and return errors."""
    all_errors = []

    # Check personas directory exists
    if not PERSONAS_DIR.exists():
        all_errors.append(ValidationError("personas/", "Directory does not exist"))
        return all_errors

    if not SCHEMAS_DIR.exists():
        all_errors.append(ValidationError("schemas/", "Directory does not exist"))
        return all_errors
    schema_baseline = SCHEMAS_DIR / "_baseline.yaml"
    if not schema_baseline.is_file():
        all_errors.append(ValidationError("schemas/_baseline.yaml", "Schema baseline missing"))
    for path in get_schema_files():
        all_errors.extend(validate_schema(path))

    # Check baseline exists
    baseline_path = PERSONAS_DIR / "_baseline.md"
    if not baseline_path.exists():
        all_errors.append(ValidationError("personas/_baseline.md", "Baseline file missing"))

    # Validate each persona file
    for path in get_persona_files():
        all_errors.extend(validate_frontmatter(path))
        all_errors.extend(validate_elaborated_sections(path))
        all_errors.extend(validate_persona_nuance(path))
        all_errors.extend(validate_provenance(path))
        all_errors.extend(validate_heuristic_overrides(path))
        all_errors.extend(validate_stub_structure(path))

    # Cross-file validations
    all_errors.extend(validate_baseline_consistency())
    all_errors.extend(validate_cross_cutting_controls())

    return all_errors


# --- pytest integration ---

def test_all_validations():
    """Pytest entry point — runs all validations."""
    errors = run_validation()
    if errors:
        error_messages = "\n".join(f"  - {e}" for e in errors)
        raise AssertionError(f"Validation errors found:\n{error_messages}")


def test_cognitive_schema_requires_provenance(tmp_path):
    """Canonical cognitive schemas cannot lose their source metadata."""
    source = SCHEMAS_DIR / "4.2.10-cognitive-memory.persona.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    data.pop("provenance")
    candidate = tmp_path / source.name
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    errors = validate_schema(candidate)
    assert any("Missing provenance object" in error.message for error in errors)


def test_elaborated_schema_requires_substantive_variation(tmp_path):
    """Canonical elaborated schemas cannot ship an empty strategy collection."""
    source = SCHEMAS_DIR / "4.2.10-cognitive-memory.persona.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    data["strategies"] = []
    candidate = tmp_path / source.name
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    errors = validate_schema(candidate)
    assert any(
        "JSON Schema violation at strategies" in error.message for error in errors
    )


def test_elaborated_schema_rejects_malformed_nested_values(tmp_path):
    """Canonical JSON Schema validation rejects malformed nested persona values."""
    source = SCHEMAS_DIR / "4.2.2-low-vision.persona.yaml"
    source_data = yaml.safe_load(source.read_text(encoding="utf-8"))
    mutations = (
        ("empty assistive technology", lambda data: data["assistive_tech"].__setitem__(0, {})),
        ("missing prompt field", lambda data: data["prompt"].pop("blocked_input")),
        ("null heuristic override", lambda data: data["heuristic_overrides"].__setitem__("1", None)),
    )
    for label, mutate in mutations:
        data = yaml.safe_load(yaml.safe_dump(source_data, sort_keys=False))
        mutate(data)
        candidate = tmp_path / f"{label.replace(' ', '-')}.persona.yaml"
        candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        errors = validate_schema(candidate)
        assert any("JSON Schema violation" in error.message for error in errors), label


def test_cognitive_user_variant_requires_conditional_language(tmp_path):
    """A qualifier elsewhere cannot mask an absolute cognitive user variant."""
    source = SCHEMAS_DIR / "4.2.10-cognitive-memory.persona.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    data["user_variants"][0]["behavior"] = "This user always follows one fixed strategy."
    candidate = tmp_path / source.name
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    errors = validate_schema(candidate)
    assert any("lacks conditional language" in error.message for error in errors)


def test_interpretation_guidance_rejects_missing_anti_stereotype_policy():
    """Policy existence alone cannot satisfy the interpretation safeguard."""
    text = (METHODOLOGY_DIR / "persona-interpretation.md").read_text(encoding="utf-8")
    incomplete = text.replace(
        "Do not compress multiple strategies into one supposedly universal behavior.",
        "",
    )
    errors = validate_interpretation_guidance(incomplete)
    assert any("universal behavior" in error.message for error in errors)


def test_codeowners_rejects_unowned_prompt_content():
    """Prompt-bearing source paths cannot silently lose required owner review."""
    text = (GOVERNANCE_ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    owner_list = " ".join(REQUIRED_CODEOWNERS)
    incomplete = text.replace(f"/Disability-Persona-Toolkit/methodology/ {owner_list}", "")
    errors = validate_codeowners(incomplete)
    assert any("/methodology/" in error.message for error in errors)


def test_coga_notice_rejects_incomplete_2015_license():
    """The 2023 license copy cannot mask missing terms in the 2015 notice."""
    notice = (PERSONAS_DIR / "cognitive-sources.LICENSE.md").read_text(encoding="utf-8")
    incomplete = notice.replace(
        "https://www.w3.org/Consortium/Legal/copyright-software-short-notice",
        "https://example.invalid/missing-2015-short-notice",
    )
    errors = validate_coga_notice(incomplete)
    assert any("2015 version complete normalized license text differs" in error.message for error in errors)


def test_coga_notice_rejects_removed_permission_grants():
    """Both complete W3C permission grants must remain in the distributed notice."""
    notice = (PERSONAS_DIR / "cognitive-sources.LICENSE.md").read_text(encoding="utf-8")
    incomplete, replacements = re.subn(
        r"Permission to copy, modify, and distribute this work,.*?"
        r"of the work or portions thereof, including modifications:\n",
        "",
        notice,
        flags=re.DOTALL,
    )
    assert replacements == 2
    errors = validate_coga_notice(incomplete)
    assert sum(
        "complete normalized license text differs" in error.message
        for error in errors
    ) == 2


def test_coga_notice_rejects_obsolete_2026_holder():
    """The 2026 source must retain the copyright-holder form from the 2023 license."""
    notice = (PERSONAS_DIR / "cognitive-sources.LICENSE.md").read_text(encoding="utf-8")
    obsolete = notice.replace(
        "Copyright © 2026 World Wide Web Consortium.",
        "Copyright © 2026 W3C® (MIT, ERCIM, Keio, Beihang).",
    )
    errors = validate_coga_notice(obsolete)
    assert any("obsolete 2015 copyright-holder form" in error.message for error in errors)


# --- CLI entry point ---

if __name__ == "__main__":
    errors = run_validation()
    if errors:
        print(f"FAILED — {len(errors)} validation error(s):\n")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        persona_count = len(get_schema_files())
        elaborated = sum(
            1
            for path in get_schema_files()
            if yaml.safe_load(path.read_text(encoding="utf-8")).get("status") == "elaborated"
        )
        print(f"PASSED — {persona_count} persona schemas validated ({elaborated} elaborated)")
        sys.exit(0)
