#!/usr/bin/env python3
"""Regression runner for the samples/ corpus.

Sample format (see samples/README.md):

    # expect: <band substring>      <- assertion target
    # register: ...                 <- context (not asserted)
    # context: ...
    # source: ...
    ---
    <text under test, verbatim>

Only `expect` is asserted; the rest is context the detector can't see but the
reader needs.  Run:

    python3 scripts/test_samples.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"


def parse(path):
    """Return (meta: dict[str, str], body: str)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    meta, i = {}, 0
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        if line.lstrip().startswith("#") and ":" in line:
            key, val = line.lstrip("# ").split(":", 1)
            key = key.strip()
            meta[key] = (meta.get(key, "") + " " + val.strip()).strip()
        i += 1
    body = "\n".join(lines[i + 1:]) if i < len(lines) else ""
    return meta, body


def _load_detector():
    spec = importlib.util.spec_from_file_location("aitl_detect", ROOT / "scripts" / "detect.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(files, detect):
    fails = []
    for f in files:
        meta, body = parse(f)
        expect = meta.get("expect", "")
        register = meta.get("register", "-")
        r = detect.analyze(body)
        ok = expect in r["band"] if expect else True
        tag = "PASS" if ok else "FAIL"
        print(f"{tag}  {f.name:<22} {r['score']:>3}/100  {r['band']:<22} "
              f"expect={expect:<10} [{register}]")
        if not ok:
            fails.append(f.name)
    return fails


def main():
    files = sorted(SAMPLES.glob("*.txt"))
    if not files:
        print(f"no samples in {SAMPLES}")
        return 1
    fails = run(files, _load_detector())
    print(f"\n{len(files) - len(fails)}/{len(files)} passed"
          + (f"  FAILED: {', '.join(fails)}" if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
