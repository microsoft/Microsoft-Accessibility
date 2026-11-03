"""Offline regression coverage for generated persona loading."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tests.evals import _context

SCHEMA_FILES = sorted(_context.SCHEMAS_DIR.glob("*.persona.yaml"))


@pytest.mark.parametrize("path", SCHEMA_FILES, ids=lambda path: path.stem)
def test_schema_loading_preserves_metadata_and_baseline(path, monkeypatch):
    monkeypatch.setenv("PERSONA_SOURCE", "schema")
    source = yaml.safe_load(path.read_text(encoding="utf-8"))
    rendered = yaml.safe_load(_context.load_persona_by_alias(source["alias"]))
    for field in ("clause", "title", "alias", "status", "fps_statement", "provenance"):
        assert rendered.get(field) == source.get(field)
    if source["status"] == "stub":
        assert rendered == source
        return
    baseline = _context._load_baseline_schema()
    for field in ("strategies", "user_variants", "learning"):
        inherited = [
            {**item, "from_baseline": True}
            for item in baseline[field]
            if item["id"] not in source.get("baseline_excludes", [])
        ]
        assert rendered[field] == source[field] + inherited


@pytest.mark.parametrize("source", ("md", "schema"))
@pytest.mark.parametrize("mode", ("single", "all", "medium"))
def test_stub_context_preserves_limits_and_required_safeguards(source, mode, monkeypatch):
    monkeypatch.setenv("PERSONA_SOURCE", source)
    previous = _context.get_eval_persona_context_mode()
    try:
        _context.set_eval_persona_context_mode(mode)
        prompt = _context.load_eval_persona_context("photosensitive")
    finally:
        _context.set_eval_persona_context_mode(previous)
    assert "status: stub" in prompt
    for name in ("licensing", "responsible-persona-use", "persona-interpretation"):
        assert _context.load_methodology(name) in prompt
    if mode != "single":
        assert "do not borrow or infer" in prompt


def test_source_switch_does_not_reuse_other_source_cache(monkeypatch):
    monkeypatch.setenv("PERSONA_SOURCE", "md")
    markdown = _context.load_persona_by_alias("low-vision")
    monkeypatch.setenv("PERSONA_SOURCE", "schema")
    structured = _context.load_persona_by_alias("low-vision")
    assert markdown.startswith("---")
    assert structured.startswith("# Accessibility persona:")
    assert structured != markdown


def test_invalid_source_is_reported(monkeypatch):
    monkeypatch.setenv("PERSONA_SOURCE", "scheam")
    with pytest.raises(ValueError, match="Unsupported PERSONA_SOURCE"):
        _context.load_persona_by_alias("low-vision")


def test_missing_baseline_does_not_fall_back_to_markdown(monkeypatch):
    def missing_baseline():
        raise FileNotFoundError("Missing baseline")

    monkeypatch.setenv("PERSONA_SOURCE", "schema")
    monkeypatch.setattr(_context, "_load_baseline_schema", missing_baseline)
    _context._load_persona_by_alias.cache_clear()
    try:
        with pytest.raises(FileNotFoundError, match="Missing baseline"):
            _context.load_persona_by_alias("low-vision")
    finally:
        _context._load_persona_by_alias.cache_clear()


def test_resource_loaders_work_after_relocation(tmp_path):
    resource = tmp_path / "monorepo" / "resource"
    for folder in ("personas", "schemas", "heuristics", "methodology", "standards"):
        shutil.copytree(_context.REPO_ROOT / folder, resource / folder)
    module = resource / "tests" / "evals" / "_context.py"
    module.parent.mkdir(parents=True)
    shutil.copyfile(Path(_context.__file__), module)
    code = (
        "import importlib.util, json; "
        f"spec = importlib.util.spec_from_file_location('context', {str(module)!r}); "
        "context = importlib.util.module_from_spec(spec); spec.loader.exec_module(context); "
        "print(json.dumps({'root': str(context.REPO_ROOT), "
        "'prompt': context.load_eval_persona_context('photosensitive')}))"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["root"] == str(resource)
    assert "status: stub" in payload["prompt"]
