#!/usr/bin/env python3
"""aitl-mcp — local stdio MCP server exposing the `aitl` AI-tell detector.

Single source of truth: this loads the skill's detect.py (word lists + scoring)
instead of re-implementing them, so the CLI script and the MCP tool never drift.

Run (ephemeral env, nothing installed globally):
    uv run --with mcp python server.py

If the skill moves, point at the detector explicitly:
    AITL_DETECT_PY=/path/to/detect.py uv run --with mcp python server.py
"""
import importlib.util
import json
import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer

DEFAULT_DETECT = Path.home() / ".claude" / "skills" / "aitl" / "scripts" / "detect.py"


def _load_detector():
    path = Path(os.environ.get("AITL_DETECT_PY", DEFAULT_DETECT)).expanduser()
    if not path.exists():
        raise RuntimeError(f"detect.py not found at {path}; set AITL_DETECT_PY")
    spec = importlib.util.spec_from_file_location("aitl_detect", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _get_detector():
    """Re-import detect.py on every call, so edits to the word lists / scoring
    take effect immediately without restarting this MCP server."""
    return _load_detector()


mcp = MCPServer("aitl")


@mcp.tool()
def analyze_text(text: str) -> str:
    """Analyze text for AI-writing tells (Chinese + English).

    Returns JSON with: score (0-100), band (人类 / 基本人味 / 可疑 / AI 味明显 /
    纯 AI slop), em_dash_uses, colon, hedge_count, negative_parallelism,
    ai_emoji, sentence_cv (burstiness — low = uniform = AI-ish), opening_formula,
    closing_formula, and the matched stock phrases (zh_hits / en_hits).

    This is a QUANTITATIVE BASE, not a verdict. Always read the text too:
    structural tells, register (technical notes / legalese / non-native writing),
    and short samples are NOT captured here.
    """
    return json.dumps(_get_detector().analyze(text), ensure_ascii=False, indent=2)


@mcp.tool()
def score_text(text: str) -> str:
    """Return just the AI-tell score and band, e.g. '66/100  AI 味明显'."""
    r = _get_detector().analyze(text)
    return f"{r['score']}/100  {r['band']}"


if __name__ == "__main__":
    mcp.run()
