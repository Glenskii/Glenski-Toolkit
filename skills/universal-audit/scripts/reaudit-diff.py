#!/usr/bin/env python3
"""
reaudit-diff.py
Universal Audit re-audit helper: decide, from the SOURCE, how much of a prior audit still holds.

PURPOSE
    A prior report date or version string is not evidence that code is unchanged. This
    script compares the commit each prior finding and rejected claim was established
    against with the current commit, using `git diff --name-status -M`, and classifies:

        SOURCE_UNCHANGED   none of the finding's source_paths changed. The finding is
                           still carried forward, but it must be re-confirmed on the
                           current evidence (spec Section 16), not copied.
        SOURCE_CHANGED     at least one source path was modified, deleted or renamed.
                           Re-validate from scratch. A prior fix may have landed, or
                           the code around it changed.
        SOURCE_UNKNOWN     no source_ref/source_paths recorded (older audit). Treat as
                           changed.

    Rejected claims: SOURCE_UNCHANGED keeps the claim suppressed, SOURCE_CHANGED reopens
    it as new work.

USAGE
    python -I reaudit-diff.py --prior audits/<prior-id> --repo <path> [--current <ref>]
        [--out reaudit-diff.json]

    --current defaults to HEAD. Requires git on PATH. Read-only.

EXIT CODES
    0 ok, 1 bad inputs or git failure
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# SECTION: helpers
# ---------------------------------------------------------------------------
def die(message):
    print("ERROR: " + message, file=sys.stderr)
    sys.exit(1)


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    return result.returncode, result.stdout, result.stderr.strip()


def load_list(path, key):
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return data.get(key, [])


def changed_files(repo, base, current, cache):
    """Return {path: status} for files that changed between two refs, with rename tracking."""
    cache_key = (base, current)
    if cache_key in cache:
        return cache[cache_key]
    code, out, err = git(repo, "diff", "--name-status", "-M", f"{base}..{current}")
    if code != 0:
        cache[cache_key] = None
        return None
    changed = {}
    for line in out.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") and len(parts) >= 3:
            changed[parts[1]] = "renamed"
            changed[parts[2]] = "renamed"
        elif len(parts) >= 2:
            changed[parts[1]] = {"M": "modified", "D": "deleted", "A": "added"}.get(status[0], status)
    cache[cache_key] = changed
    return changed


def classify(record, repo, current, cache):
    base = record.get("source_ref")
    paths = list(dict.fromkeys(p.get("file") for p in record.get("source_paths", []) if p.get("file")))
    if not base or not paths:
        return "SOURCE_UNKNOWN", "no source_ref or source_paths recorded", []
    changed = changed_files(repo, base, current, cache)
    if changed is None:
        return "SOURCE_UNKNOWN", f"commit {base} not reachable in this repository", []
    norm = lambda p: p.replace("\\", "/")
    touched = [(norm(p), changed[norm(p)]) for p in paths if norm(p) in changed]
    if touched:
        return "SOURCE_CHANGED", "; ".join(f"{p} ({s})" for p, s in touched), [p for p, _ in touched]
    return "SOURCE_UNCHANGED", f"{len(paths)} source path(s) identical between {base[:10]} and {current[:10]}", []


# ---------------------------------------------------------------------------
# SECTION: main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Classify prior audit records by source change.")
    parser.add_argument("--prior", required=True, help="prior audits/<audit-id> folder")
    parser.add_argument("--repo", required=True, help="git repository of the audited product")
    parser.add_argument("--current", default="HEAD", help="ref audited now (default HEAD)")
    parser.add_argument("--out", help="write JSON result here")
    args = parser.parse_args()

    prior = Path(args.prior)
    repo = Path(args.repo)
    code, resolved, err = git(repo, "rev-parse", args.current)
    if code != 0:
        die(f"cannot resolve {args.current} in {repo}: {err}")
    current = resolved.strip()

    findings = load_list(prior / "findings.json", "findings")
    rejected = load_list(prior / "rejected-claims.json", "rejected_claims")
    if not findings and not rejected:
        die(f"no findings.json or rejected-claims.json under {prior}")

    cache = {}
    rows = []
    for f in findings:
        verdict, why, touched = classify(f, repo, current, cache)
        rows.append({"kind": "finding", "id": f.get("finding_id"), "status": f.get("status"),
                     "severity": f.get("severity"), "source_ref": f.get("source_ref"),
                     "classification": verdict, "detail": why, "changed_paths": touched})
    for r in rejected:
        verdict, why, touched = classify(r, repo, current, cache)
        rows.append({"kind": "rejected-claim", "id": r.get("claim_id"), "status": "REJECTED",
                     "severity": None, "source_ref": r.get("source_ref"),
                     "classification": verdict, "detail": why, "changed_paths": touched,
                     "action": "stays suppressed" if verdict == "SOURCE_UNCHANGED" else "reopen as new work"})

    summary = {k: sum(1 for row in rows if row["classification"] == k)
               for k in ("SOURCE_UNCHANGED", "SOURCE_CHANGED", "SOURCE_UNKNOWN")}
    result = {"prior": str(prior), "current_ref": current, "summary": summary, "records": rows}

    print(f"prior {prior.name} vs {current[:10]}: "
          f"{summary['SOURCE_UNCHANGED']} unchanged, {summary['SOURCE_CHANGED']} changed, "
          f"{summary['SOURCE_UNKNOWN']} unknown")
    for row in rows:
        print(f"  {row['classification']:17} {row['kind']:14} {row['id']}  {row['detail']}")
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("wrote " + args.out)


if __name__ == "__main__":
    main()
