#!/usr/bin/env python3
"""Static SkillSpector scan of every vendored module + baseline diff.

Skillspector (NVIDIA) must be installed (`skillspector`, static stage). This wrapper:
  * scans each module dir under skills/atelier/references/ with --no-llm
  * compares the findings against scripts/security-baseline.json (committed)
  * reports only NEW findings vs baseline (matched on rule+severity+title)
  * --update-baseline rewrites the baseline (called from the re-vendor PR)

Exit codes: 0 = no new findings, 10 = new findings present, 1 = environment error.
The LLM (semantic) stage is intentionally NOT used here; static-only reports mention it.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "scripts" / "security-baseline.json"
REFS = ROOT / "skills" / "atelier" / "references"
TMP = Path("/tmp/atelier-ss")

def clean_env():
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("SKILLSPECTOR_"):
            env.pop(k, None)
    # workflow budget: default 600s total per scan -> static_patterns analyzers on
    # large modules (.mjs/CSS bundles) hit the wall and degrade. Give 3h.
    env["SKILLSPECTOR_MAX_WORKFLOW_SECONDS"] = "10800"
    env["SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT"] = "1200"
    return env

def warm_cache(dir_: Path):
    """skillspector has a 30s discovery hard-cap (MAX_BUNDLE_DISCOVERY_SECONDS);
    cold page cache on large module trees blows past it -> degraded scans. Pre-read."""
    subprocess.run(["find", "-L", str(dir_), "-type", "f", "-exec", "cat", "{}", "+"],
                   capture_output=True, timeout=120)

def scan_static(dir_: Path):
    out = TMP / f"{dir_.name}.json"
    for attempt in (1, 2):
        warm_cache(dir_)
        r = subprocess.run(
            ["skillspector", "scan", str(dir_), "--no-llm", "-f", "json", "-o", str(out)],
            capture_output=True, text=True, timeout=1700, env=clean_env())
        if not out.exists():
            return None, (r.stderr or r.stdout or "")[:200]
        d = json.loads(out.read_text())
        ac = d.get("analysis_completeness", {})
        # Deterministic-layer span limits: huge data lines (CSV/JSON knowledge
        # bases) legitimately exceed the obfuscation/parser span limit; the
        # meta-analysis then FAILS CLOSED to 100/CRITICAL. These are waived.
        WAIVED = {"obfuscated_instruction_text", "static_parse_limit", "reference_unresolved"}
        waived_analyzers = set()
        waived_rows = []
        for e in ac.get("ledger_exceptions") or []:
            if e.get("reason_code") in WAIVED and not e.get("fatal"):
                waived_analyzers.update(e.get("analyzers") or [])
                waived_rows.append(e)
        degraded = [a["analyzer_id"] for a in ac.get("analyzer_statuses", [])
                    if a.get("status") not in ("completed", "not_applicable", "disabled")
                    and a["analyzer_id"] not in waived_analyzers]
        if not degraded:
            ra = d.get("risk_assessment", {})
            findings = []
            for f in d.get("findings_after_filtering") or []:
                findings.append({
                    "rule": f.get("rule_id") or f.get("rule") or f.get("analyzer_id") or "?",
                    "severity": f.get("severity") or "?",
                    "title": (f.get("title") or f.get("message") or f.get("description") or "")[:120],
                })
            return {
                "score": ra.get("score"),
                "severity": ra.get("severity"),
                "recommendation": ra.get("recommendation"),
                "findings": findings,
                "coverage": ac.get("coverage_percent"),
                "waived": [{"reason_code": e.get("reason_code"), "path": e.get("path")}
                           for e in waived_rows],
            }, None
        if attempt == 2:
            return None, f"incomplete: {','.join(degraded)} (even after retry)"
    return None, "unreachable"

def key(f):
    return json.dumps([f["rule"], f["severity"], f["title"]], sort_keys=True)

def main():
    update = "--update-baseline" in sys.argv
    baseline = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    TMP.mkdir(exist_ok=True)
    new_any = False
    report = ["# SkillSpector static scan (per vendored module)\n"]
    report.append("| module | score | severity | rec | new findings |")
    report.append("|---|---|---|---|---|")
    report.append("(note: score/rec become failure-closed 100/DO_NOT_INSTALL when span-limit")
    report.append(" exceptions exist in huge data files; the actual criterion is per-finding-info.)")
    current = {}
    module_dirs = [m for m in sorted(REFS.iterdir()) if m.is_dir()]
    if [m for m in sys.argv[1:] if not m.startswith("--")]:
        module_dirs = [m for m in module_dirs if m.name in [x for x in sys.argv[1:] if not x.startswith("--")]]
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            results = list(pool.map(scan_static, module_dirs))
        for mod, (res, err) in zip(module_dirs, results):
            if res is None:
                report.append(f"| {mod.name} | env error | | | `{err}` |")
                new_any = True
                continue
            current[mod.name] = res
            old = baseline.get(mod.name, {}).get("findings", [])
            old_keys = {key(f) for f in old}
            new = [f for f in res["findings"] if key(f) not in old_keys]
            wa = len(res.get("waived") or [])
            wa_txt = f" ({wa} waived span-limit)" if wa else ""
            if new:
                new_any = True
                report.append(f"| {mod.name} | {res['score']}{wa_txt} | {res['severity']} | {res['recommendation']} | {len(new)} NEW |")
                for f in new:
                    report.append(f"  - NEW [{f['severity']}] {f['rule']}: {f['title']}")
            else:
                report.append(f"| {mod.name} | {res['score']}{wa_txt} | {res['severity']} | {res['recommendation']} | none |")
    finally:
        if update:
            BASELINE.write_text(json.dumps(current, indent=2) + "\n")
            report.append("\n_baseline updated._")
    print("\n".join(report))
    sys.exit(10 if new_any else 0)

if __name__ == "__main__":
    main()
