#!/usr/bin/env python3
"""Check upstream repos of the 5 vendored modules in this repo for new commits.

Reads the vendored commit for each module from THIRD-PARTY-NOTICES.md, queries the
GitHub compare API (needs `gh` authenticated), and prints a DETERMINISTIC markdown
summary (no timestamps) suitable both for human reading and as a cron monitor:
only module names, SHA short hashes, and ahead-by counts.

Exit code is always 0 unless an environment error prevents all checks.
"""
import re
import subprocess
import sys
from pathlib import Path

NOTICES = Path(__file__).resolve().parent.parent / "THIRD-PARTY-NOTICES.md"

ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|.*?(https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+).*?\|[^\n]*?commit\s+`([0-9a-f]{7,40})`", re.I)


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def main() -> int:
    rows = []
    for line in NOTICES.read_text().splitlines():
        m = ROW.match(line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3)))
    if not rows:
        print("ERROR: no module rows parsed from THIRD-PARTY-NOTICES.md")
        return 1

    print("| module | upstream | vendored | new commits | latest SHA |")
    print("|---|---|---|---|---|")
    updated = []
    for module, repo_url, vendored in rows:
        repo = repo_url.replace("https://github.com/", "").rstrip("/")
        try:
            data = subprocess.run(
                ["gh", "api", f"repos/{repo}/compare/{vendored}...HEAD",
                 "--jq", '{"ahead": .ahead_by, "latest": .commits[-1].sha, "names": [ .commits[-3:][].commit.message | split("\\n")[0] ]}'],
                capture_output=True, text=True, check=False, timeout=60)
            if data.returncode != 0:
                print(f"| {module} | {repo} | {vendored[:7]} | ? (api error) | ? |")
                continue
            import json
            payload = json.loads(data.stdout)
            ahead = payload["ahead"]
            latest = (payload["latest"] or vendored)[:7]
            marker = "YES" if ahead else "no"
            print(f"| {module} | {repo} | {vendored[:7]} | {ahead if ahead else 0} ({marker}) | {latest} |")
            if ahead:
                updated.append((module, repo, ahead, latest, payload["names"]))
        except Exception as e:  # noqa: BLE001
            print(f"| {module} | {repo} | {vendored[:7]} | ? | ? |")

    print()
    if updated:
        for module, repo, ahead, latest, names in updated:
            print(f"UPDATE {module}: {repo} +{ahead} commits (HEAD {latest})")
            for n in names:
                if n:
                    print(f"  - {n}")
        sys.exit(10)  # has updates
    print("NO-UPDATES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
