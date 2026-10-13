#!/usr/bin/env python3
"""
import-security-hunt.py
Universal Audit: import a security-audit (Cloudflare skill) run into an audit folder.

PURPOSE
    The security-audit skill hunts for exploitable vulnerabilities and writes findings.json
    with three verdicts: confirmed, needs_validation, rejected. This script converts those
    records into Universal Audit artifacts so the scorer and release gates can use them:

        confirmed         -> findings.json   status FAIL, severity from the hunt
        needs_validation  -> findings.json   status UNVERIFIED, no severity
        rejected          -> rejected-claims.json (no severity, never scored)

    Every trace/evidence location becomes an evidence-ledger.json record (class CODE).

    Imported findings are also linked into selected-controls.json (finding_ids, evidence_ids,
    and FAIL + severity for confirmed records) so score.py counts them.

SAFETY
    - Hunt `execution.payloads` are NEVER copied. The evidence ledger must stay free of
      working exploit material (spec Section 8.2). Only the descriptive text is imported.
    - Import is idempotent: records are keyed by hunt fingerprint, so re-running updates
      existing findings instead of duplicating them.
    - Control mapping is keyword-based and heuristic. Anything that fell back to the
      default control is tagged `needs-control-review` and listed in import-log.json.

USAGE
    python -I import-security-hunt.py --hunt <run-dir | findings.json> --audit-dir audits/<audit-id>
        [--commit <sha>] [--default-control SEC-INPUT-001] [--map map.json] [--dry-run]

    map.json is an object of {"<hunt fingerprint>": "<control_id>"} overrides.

EXIT CODES
    0 imported, 1 problem with inputs, 2 hunt file failed basic shape checks
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# SECTION: constants
# ---------------------------------------------------------------------------
HUNT_COLLECTOR = "security-audit skill (cloudflare/security-audit-skill)"
SEVERITY_MAP = {"critical": "Critical", "high": "High", "medium": "Medium",
                "low": "Low", "informational": "Informational"}
LIKELIHOOD_MAP = {"critical": "High", "high": "High", "medium": "Medium",
                  "low": "Low", "informational": "Low"}
CONFIDENCE_MAP = {"high": "High", "medium": "Medium", "low": "Low"}

# Ordered: first match wins. Patterns run against title + description + root cause.
CONTROL_RULES = [
    (r"\bssrf\b|server-side request forgery|fetch(es|ing)? (a )?user[- ]supplied url", "SEC-SSRF-001"),
    (r"tenant|cross-account|cross-org|cross-customer", "SEC-TENANT-001"),
    (r"idor|insecure direct object|ownership|owner check|object[- ]level|another (user|customer|account)'?s?|"
     r"other users?'? (data|records|files)", "SEC-AUTHZ-001"),
    (r"\bxss\b|cross-site scripting|dom[- ]based|innerhtml|script injection", "SEC-XSS-001"),
    (r"sql injection|sqli|command injection|shell injection|os command|code injection|template injection|"
     r"\binject", "SEC-INJECT-001"),
    (r"csrf|cross-site request forgery", "SEC-CSRF-001"),
    (r"\bcors\b|cross-origin resource", "SEC-CORS-001"),
    (r"path traversal|directory traversal|zip slip|file upload|arbitrary file", "SEC-FILE-001"),
    (r"webhook|signature (is )?not (verified|checked)|hmac", "SEC-HOOK-001"),
    (r"session|cookie|token (lifetime|expiry|revocation)|jwt", "SEC-SESS-001"),
    (r"authoriz|privilege escalation|missing (permission|access) check|broken access|role check", "SEC-AUTHZ-001"),
    (r"authenticat|login|password reset|credential stuffing|brute force|\bmfa\b|2fa", "SEC-AUTHN-001"),
    (r"hard-?coded (secret|key|token|credential)|secret (leak|exposure)|api key|private key", "SEC-SECRET-001"),
    (r"crypto|weak (hash|cipher|random)|insecure random|nonce reuse|iv reuse|tls", "SEC-CRYPTO-001"),
    (r"dependenc|supply chain|postinstall|lockfile|typosquat|vulnerable package", "SUP-DEP-001"),
    (r"build pipeline|ci/cd|workflow injection|github actions|release signing|update (channel|mechanism)|"
     r"code signing", "SUP-BUILD-001"),
    (r"prompt injection|llm|agent tool|tool call", "AI-INJECT-001"),
    (r"rate limit|resource exhaustion|denial of service|unbounded|quota|api (abuse|misuse)", "SEC-API-001"),
    (r"input validation|unvalidated|unsanitized|improper validation|parser", "SEC-INPUT-001"),
]


# ---------------------------------------------------------------------------
# SECTION: helpers
# ---------------------------------------------------------------------------
def die(message, code=1):
    print("ERROR: " + message, file=sys.stderr)
    sys.exit(code)


def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        if default is not None:
            return default
        die(f"missing file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"{path} is not valid JSON: {exc}")


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def unwrap(data, key):
    """Accept either a bare array or {"<key>": [...]} and report which shape it was."""
    if isinstance(data, list):
        return data, None
    if isinstance(data, dict) and isinstance(data.get(key), list):
        return data[key], key
    die(f"expected an array or an object with a '{key}' array")


def rewrap(items, key, original_shape_key):
    if original_shape_key is None:
        return items
    return {original_shape_key: items}


def next_number(existing_ids, suffix_letter):
    highest = 0
    for existing in existing_ids:
        match = re.search(rf"-{suffix_letter}(\d{{3,}})$", str(existing))
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def pick_control(record, default_control, overrides):
    fingerprint = record.get("fingerprint", "")
    if fingerprint in overrides:
        return overrides[fingerprint], "override"
    haystack = " ".join(
        str(record.get(k, "")) for k in ("title", "description", "root_cause", "claimed_root_cause")
    ).lower()
    for pattern, control in CONTROL_RULES:
        if re.search(pattern, haystack):
            return control, "keyword"
    return default_control, "defaulted"


def locations_of(record):
    """Unique (file, line, note) tuples from trace and evidence, trace first."""
    seen = set()
    result = []
    for item in list(record.get("trace", [])) + list(record.get("evidence", [])):
        file_name = item.get("file")
        line = item.get("line")
        if not file_name or (file_name, line) in seen:
            continue
        seen.add((file_name, line))
        note = item.get("description") or item.get("scope") or ""
        result.append((file_name, line, note))
    return result


def join_nonempty(parts, separator="; "):
    return separator.join(p.strip() for p in parts if p and str(p).strip())


def resolve_hunt_file(hunt_arg):
    path = Path(hunt_arg)
    if path.is_dir():
        path = path / "findings.json"
    if not path.is_file():
        die(f"hunt findings.json not found at {path}")
    return path


# ---------------------------------------------------------------------------
# SECTION: conversion
# ---------------------------------------------------------------------------
def evidence_for(record, audit_id, evidence_state, commit, environment, now_iso):
    """Create evidence ledger records for a hunt record, return their IDs."""
    ids = []
    for file_name, line, note in locations_of(record):
        location = f"{file_name}:{line}" if line else file_name
        key = (record["fingerprint"], location)
        if key in evidence_state["by_key"]:
            ids.append(evidence_state["by_key"][key])
            continue
        evidence_id = f"{audit_id}-E{evidence_state['next']:03d}"
        evidence_state["next"] += 1
        evidence_state["by_key"][key] = evidence_id
        evidence_state["new"].append({
            "schema_version": "1.0",
            "audit_id": audit_id,
            "evidence_id": evidence_id,
            "evidence_class": "CODE",
            "collected_at": now_iso,
            "collected_by": HUNT_COLLECTOR,
            "version_context": {"commit_or_build": commit, "environment": environment},
            "location": location,
            "method": f"security-audit {record['verdict']} record {record['fingerprint']}: source trace",
            "excerpt": note or record.get("title", ""),
            "integrity_ref": None,
            "limitations": "Descriptive excerpt only. Hunt payloads are deliberately not imported.",
        })
        ids.append(evidence_id)
    return ids


def finding_from_confirmed(record, base):
    severity = record.get("severity", {})
    overall = severity.get("overall_severity", "low")
    likelihood = severity.get("likelihood", {}).get("score", "low")
    confidence = record.get("confidence", {}).get("score", "medium")
    execution = record.get("execution", {})
    conditions = [f"{c.get('kind', '')}: {c.get('description', '')}" for c in record.get("conditions", [])]
    steps = execution.get("instructions", [])
    return {
        **base,
        "title": record["title"][:120],
        "status": "FAIL",
        "severity": SEVERITY_MAP.get(overall, "Medium"),
        "likelihood": LIKELIHOOD_MAP.get(likelihood, "Unknown"),
        "confidence": CONFIDENCE_MAP.get(confidence, "Medium"),
        "preconditions": join_nonempty(conditions) or None,
        "observable_condition": execution.get("observed_result") or record.get("description", ""),
        "expected_condition": record.get("intended_behavior", ""),
        "technical_risk": join_nonempty([record.get("description", ""), "Root cause: " + record.get("root_cause", "")], " "),
        "business_impact": severity.get("impact", {}).get("reason", "") +
                           " (technical impact text from the hunt: review for business wording)",
        "scope_of_impact": None,
        "recommended_fix": record.get("remediation", {}).get("strategy", ""),
        "alternative_control": None,
        "remediation_effort": "Requires discovery",
        "owner": "Unassigned",
        "verification": "Re-run the security-audit hunt on the fixed commit. Safe local steps: " +
                        join_nonempty(steps, " | "),
        "residual_risk": None,
        "challenge_outcome": None,
    }


def finding_from_needs_validation(record, base):
    blockers = record.get("blockers", [])
    blocker_text = join_nonempty([b if isinstance(b, str) else json.dumps(b, ensure_ascii=False) for b in blockers])
    plan = record.get("validation_plan", {})
    plan_text = plan if isinstance(plan, str) else json.dumps(plan, ensure_ascii=False)
    return {
        **base,
        "title": record["title"][:120],
        "status": "UNVERIFIED",
        "severity": None,
        "likelihood": "Unknown",
        "confidence": "Low",
        "preconditions": None,
        "observable_condition": record.get("description", ""),
        "expected_condition": "The trust boundary holds. The decisive fact is outside source or the sandbox.",
        "technical_risk": record.get("claimed_root_cause", ""),
        "business_impact": "Not assessed: blocked by " + (blocker_text or "an unresolved external fact"),
        "scope_of_impact": None,
        "recommended_fix": "Resolve the blocker by following the validation plan: " + plan_text,
        "alternative_control": None,
        "remediation_effort": "Requires discovery",
        "owner": "Unassigned",
        "verification": plan_text,
        "residual_risk": None,
        "challenge_outcome": None,
    }


SEVERITY_ORDER = {None: 0, "Informational": 1, "Low": 2, "Medium": 3, "High": 4, "Critical": 5}


def link_controls(selected, findings, hunt_ids):
    """Point each imported finding's control row at it so score.py counts it.

    Returns a list of human-readable notes (including controls that are not selected).
    """
    notes = []
    rows = {c["control_id"]: c for c in selected.get("controls", [])}
    for finding in findings:
        if finding.get("finding_id") not in hunt_ids:
            continue
        for control_id in finding.get("control_ids", []):
            row = rows.get(control_id)
            if row is None:
                notes.append(f"{finding['finding_id']}: {control_id} is not a selected control, not linked")
                continue
            row.setdefault("finding_ids", [])
            row.setdefault("evidence_ids", [])
            if finding["finding_id"] not in row["finding_ids"]:
                row["finding_ids"].append(finding["finding_id"])
            for evidence_id in finding.get("evidence_ids", []):
                if evidence_id not in row["evidence_ids"]:
                    row["evidence_ids"].append(evidence_id)
            if finding["status"] == "FAIL":
                row["status"] = "FAIL"
                if SEVERITY_ORDER[finding["severity"]] > SEVERITY_ORDER.get(row.get("severity"), 0):
                    row["severity"] = finding["severity"]
            elif row.get("status") in (None, "NOT_APPLICABLE"):
                row["status"] = "UNVERIFIED"
    return notes


# ---------------------------------------------------------------------------
# SECTION: main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Import a security-audit hunt into a Universal Audit folder.")
    parser.add_argument("--hunt", required=True, help="hunt run directory or its findings.json")
    parser.add_argument("--audit-dir", required=True, help="audits/<audit-id> folder")
    parser.add_argument("--commit", help="commit audited; defaults to the manifest version_context")
    parser.add_argument("--default-control", default="SEC-INPUT-001",
                        help="control used when no keyword rule matches (tagged needs-control-review)")
    parser.add_argument("--map", help="JSON file of {fingerprint: control_id} overrides")
    parser.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = parser.parse_args()

    audit_dir = Path(args.audit_dir)
    manifest = read_json(audit_dir / "audit-manifest.json")
    audit_id = manifest["audit_id"]
    environment = manifest.get("environment", "local")
    commit = args.commit or manifest.get("version_context", {}).get("commit_or_build", "unknown")
    overrides = read_json(args.map, {}) if args.map else {}
    if commit == "unknown":
        print("WARNING: no commit recorded. Pass --commit <sha> so reaudit-diff.py can compare source later.",
              file=sys.stderr)

    hunt = read_json(resolve_hunt_file(args.hunt))
    if not isinstance(hunt, list):
        die("hunt findings.json must be an array of records", 2)
    for record in hunt:
        if record.get("verdict") not in ("confirmed", "needs_validation", "rejected") or not record.get("fingerprint"):
            die(f"hunt record without a valid verdict/fingerprint: {str(record)[:120]}", 2)

    findings_raw = read_json(audit_dir / "findings.json", [])
    findings, findings_shape = unwrap(findings_raw, "findings")
    evidence_raw = read_json(audit_dir / "evidence-ledger.json", [])
    evidence, evidence_shape = unwrap(evidence_raw, "evidence")
    rejected_raw = read_json(audit_dir / "rejected-claims.json", [])
    rejected, rejected_shape = unwrap(rejected_raw, "rejected_claims")

    by_hunt = {f.get("hunt_fingerprint"): f for f in findings if f.get("hunt_fingerprint")}
    rejected_by_hunt = {r.get("hunt_fingerprint"): r for r in rejected if r.get("hunt_fingerprint")}
    evidence_state = {
        "next": next_number([e.get("evidence_id") for e in evidence], "E"),
        "by_key": {},
        "new": [],
    }
    for item in evidence:  # reuse prior imports of the same location
        match = re.match(r"security-audit \w+ record (\S+):", item.get("method", ""))
        if match:
            evidence_state["by_key"][(match.group(1), item.get("location"))] = item["evidence_id"]
    finding_number = next_number([f.get("finding_id") for f in findings], "F")
    claim_number = next_number([r.get("claim_id") for r in rejected], "X")
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    log = {"imported_at": now_iso, "hunt": str(resolve_hunt_file(args.hunt)), "audit_id": audit_id,
           "records": [], "needs_control_review": []}
    counts = {"confirmed": 0, "needs_validation": 0, "rejected": 0, "updated": 0}

    for record in hunt:
        verdict = record["verdict"]
        control, how = pick_control(record, args.default_control, overrides)
        source_paths = [{"file": f, "line": l} for f, l, _ in locations_of(record)]

        if verdict == "rejected":
            existing = rejected_by_hunt.get(record["fingerprint"])
            claim = {
                "schema_version": "1.0",
                "audit_id": audit_id,
                "claim_id": existing["claim_id"] if existing else f"{audit_id}-X{claim_number:03d}",
                "title": record["title"][:120],
                "control_ids": [control],
                "claimed_issue": join_nonempty([record.get("description", ""), record.get("claimed_root_cause", "")], " "),
                "reason_rejected": record.get("reason", ""),
                "source_ref": commit,
                "source_paths": source_paths,
                "origin": "security-hunt",
                "hunt_fingerprint": record["fingerprint"],
            }
            if existing:
                rejected[rejected.index(existing)] = claim
                counts["updated"] += 1
            else:
                rejected.append(claim)
                claim_number += 1
            counts["rejected"] += 1
            log["records"].append({"fingerprint": record["fingerprint"], "verdict": verdict,
                                   "id": claim["claim_id"], "control": control, "mapping": how})
            continue

        evidence_ids = evidence_for(record, audit_id, evidence_state, commit, environment, now_iso)
        if not evidence_ids:
            die(f"hunt record {record['fingerprint']} has no file:line evidence to import", 2)
        existing = by_hunt.get(record["fingerprint"])
        finding_id = existing["finding_id"] if existing else f"{audit_id}-F{finding_number:03d}"
        base = {
            "schema_version": "1.0",
            "audit_id": audit_id,
            "finding_id": finding_id,
            "control_ids": [control],
            "cross_tags": ["security-hunt"] + (["needs-control-review"] if how == "defaulted" else []),
            "evidence_ids": evidence_ids,
            "affected_version": commit,
            "environment": environment,
            "origin": "security-hunt",
            "hunt_fingerprint": record["fingerprint"],
            "source_ref": commit,
            "source_paths": source_paths,
            "reaudit_state": None,
        }
        converter = finding_from_confirmed if verdict == "confirmed" else finding_from_needs_validation
        finding = converter(record, base)
        if existing:
            # Preserve human edits that must survive a re-import.
            for kept in ("owner", "challenge_outcome", "reaudit_state", "remediation_effort"):
                if existing.get(kept) not in (None, "Unassigned", "Requires discovery"):
                    finding[kept] = existing[kept]
            findings[findings.index(existing)] = finding
            counts["updated"] += 1
        else:
            findings.append(finding)
            finding_number += 1
        counts[verdict] += 1
        log["records"].append({"fingerprint": record["fingerprint"], "verdict": verdict,
                               "id": finding_id, "control": control, "mapping": how})
        if how == "defaulted":
            log["needs_control_review"].append(finding_id)

    evidence.extend(evidence_state["new"])
    print(f"hunt records: {len(hunt)} | confirmed -> FAIL: {counts['confirmed']} | "
          f"needs_validation -> UNVERIFIED: {counts['needs_validation']} | "
          f"rejected -> rejected-claims: {counts['rejected']} | updated in place: {counts['updated']} | "
          f"new evidence: {len(evidence_state['new'])}")
    if log["needs_control_review"]:
        print("CONTROL REVIEW NEEDED (defaulted mapping): " + ", ".join(log["needs_control_review"]))
    print("Next: confirm control mappings, run validate-audit-artifacts.py, then score.py.")

    if args.dry_run:
        print("dry run: nothing written")
        return
    selected_path = audit_dir / "selected-controls.json"
    if selected_path.exists():
        selected = read_json(selected_path)
        imported_ids = {r["id"] for r in log["records"] if r["verdict"] != "rejected"}
        for note in link_controls(selected, findings, imported_ids):
            print("LINK  " + note)
        write_json(selected_path, selected)
    write_json(audit_dir / "findings.json", rewrap(findings, "findings", findings_shape))
    write_json(audit_dir / "evidence-ledger.json", rewrap(evidence, "evidence", evidence_shape))
    write_json(audit_dir / "rejected-claims.json", rewrap(rejected, "rejected_claims", rejected_shape))
    write_json(audit_dir / "security-hunt-import-log.json", log)


if __name__ == "__main__":
    main()
