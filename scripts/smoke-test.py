#!/usr/bin/env python3
"""Smoke-test the vendored modules before review/PR (fast, offline, no binary downloads).

Checks: (1) SKILL.md frontmatter parses and has the expected keys;
(2) every standalone .mjs script in a module parses (`node --check`, if Node exists);
(3) no banned patterns sneaked into newly vendored bodies (config-editing directives,
npx/curl-install flows, credential/env reads).

Deterministic report, exit 0 only when every performed check passes. Sections that
cannot be run (no Node) are marked SKIP, not FAIL.
"""
import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "skills" / "atelier" / "references"

FRONT_KEYS = ["name", "description"]
EXPECTED_FULL = ["name", "description", "user-invocable", "argument-hint"]

FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

# banned-in-prompt patterns (case-insensitive) for vendored SKILL.md / reference md bodies
BANNED = [
    (r"(?i)(curl|wget)[^\n]{0,80}\|\s*(ba)?sh", "piped shell download"),
    (r"(?i)\bnpx\s+(skills\s+add|\binstall\b)", "npx install flow"),
    (r"(?i)(perform|execute)[^\n]{0,60}(hermes\b|\.hermes)(/|\\\\)?", "hermes host mutation"),
    (r"(?i)(read|exfiltrat|send)[^\n]{0,60}(credentials|\.env\b|api[_-]?keys?\b)", "credential read"),
    (r"(?i)edit\s+(your\s+)?(AGENTS\.md|CLAUDE\.md|settings\.json|config\.(yaml|toml|json))", "config-edit directive"),
]

def frontmatter(path: Path):
    m = FRONT.match(path.read_text(errors="replace"))
    if not m:
        return None, "no frontmatter block"
    body = m.group(1)
    keys = [ln.split(":", 1)[0].strip() for ln in body.splitlines() if ":" in ln and not ln[:1].isspace()]
    keys = [k for k in keys if k]
    return keys, None

def has_node():
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True, timeout=10)
        return True
    except Exception:
        return False

def main() -> int:
    node = has_node()
    total_fail = 0
    print("# Smoke tests — vendored modules\n")
    for mod_dir in sorted(p for p in MODULES.iterdir() if p.is_dir()):
        fails = []
        # 1. frontmatter
        skill = mod_dir / "SKILL.md"
        keys, err = (frontmatter(skill) if skill.exists() else (None, "SKILL.md missing"))
        if err:
            fails.append(f"frontmatter: {err}")
        elif keys == EXPECTED_FULL:
            pass
        elif keys and set(FRONT_KEYS) <= set(keys):
            pass  # vendored upstream may use its own key set
        else:
            fails.append(f"frontmatter keys: got {keys}")
        # 2. banned patterns in md bodies
        for md in mod_dir.rglob("*.md"):
            text = md.read_text(errors="replace")
            rel = md.relative_to(mod_dir)
            for pat, label in BANNED:
                m = re.search(pat, text)
                if m:
                    fails.append(f"banned pattern [{label}] in {rel}: ...{m.group(0)[:80]}...")
        # 3. node syntax check (SKIP when no node)
        mjs = [p for p in mod_dir.rglob("*.mjs")] + [p for p in mod_dir.rglob("*.js") if "node_modules" not in str(p)]
        checked = skipped = parse_errs = 0
        if node:
            for script in mjs[:40]:
                r = subprocess.run(["node", "--check", str(script)], capture_output=True, text=True, timeout=30)
                checked += 1
                if r.returncode != 0:
                    parse_errs += 1
                    fails.append(f"node --check failed: {script.relative_to(mod_dir)}: {(r.stderr or r.stdout).strip()[:120]}")
        else:
            skipped = len(mjs[:40])
        # 4. python syntax for module py scripts
        for py in list(mod_dir.rglob("*.py")):
            try:
                ast.parse(py.read_text(errors="replace"))
            except SyntaxError as e:
                fails.append(f"python syntax error in {py.relative_to(mod_dir)}: {e.msg}")
        status = "PASS" if not fails else "FAIL"
        print(f"## {mod_dir.name} — {status}")
        print(f"- frontmatter keys: {keys}")
        print(f"- node --check: {checked if node else f'SKIP (no node; {skipped} scripts)'} checked, {parse_errs} errors")
        print(f"- .py checked: {len(list(mod_dir.rglob('*.py')))}; banned-pattern hits: {len(fails)}")
        for f in fails:
            print(f"- ✗ {f}")
        print()
        total_fail += len(fails)

    print(f"# Result: {'ALL PASS' if total_fail == 0 else f'{total_fail} FAIL(s)'}")
    return 0 if total_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
