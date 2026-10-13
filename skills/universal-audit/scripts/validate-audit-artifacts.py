#!/usr/bin/env python3
"""
validate-audit-artifacts.py
Universal Audit: validate an audit folder before scoring and before the report is released.

PURPOSE
    score.py checks arithmetic. This script checks that the records feeding it are well
    formed and agree with each other, so a malformed findings.json cannot slip into a report.

CHECKS
    1. findings.json, evidence-ledger.json, rejected-claims.json validate against the
       schemas in references/schemas/ (stdlib subset validator, no dependencies).
    2. Cross references: every finding's evidence_ids exist; every control_id is in
       selected-controls.json; IDs are unique and carry the audit ID.
    3. Rules the schema cannot express:
         - WARN may not be Critical (spec 13.4)
         - FAIL/WARN/NOTE need a severity; UNVERIFIED must not carry one
         - a selected control marked FAIL/WARN must list at least one finding that exists
    4. Evidence hygiene: a secret/exploit-material scan over every excerpt.
    5. --release (run before rendering report.md): every Critical/High FAIL, and every
       WARN-High, must have a challenge_outcome (spec Phase 5).

USAGE
    python -I validate-audit-artifacts.py audits/<audit-id> [--release]

EXIT CODES
    0 clean, 1 errors found, 2 usage or missing files
"""

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMA_DIR = SKILL_DIR / "references" / "schemas"

# ---------------------------------------------------------------------------
# SECTION: secret / exploit material patterns (evidence excerpts must be clean)
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("API key (sk-)", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Cloudflare/other long token", re.compile(r"\b[A-Za-z0-9_-]{40,}\b(?=.*\b(token|secret|key)\b)", re.I)),
    ("bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{20,}=*", re.I)),
    ("password assignment", re.compile(r"\b(password|passwd|pwd|secret|api[_-]?key)\s*[:=]\s*['\"]?[^\s'\"<>]{6,}", re.I)),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
]


# ---------------------------------------------------------------------------
# SECTION: tiny JSON-schema subset validator
# ---------------------------------------------------------------------------
TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


def check(value, schema, path, errors):
    expected = schema.get("type")
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        if not any(TYPE_CHECKS[t](value) for t in types):
            errors.append(f"{path}: expected {types}, got {type(value).__name__}")
            return
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than {schema['maxLength']} characters")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: needs at least {schema['minItems']} item(s)")
        if "items" in schema:
            for i, item in enumerate(value):
                check(item, schema["items"], f"{path}[{i}]", errors)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required '{key}'")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                check(value[key], sub, f"{path}.{key}", errors)
        for clause in schema.get("allOf", []):
            condition = clause.get("if")
            if condition is None:
                continue
            probe = []
            check(value, condition, path, probe)
            matched = not probe and all(k in value for k in condition.get("properties", {}))
            if matched and "then" in clause:
                check(value, clause["then"], path, errors)


# ---------------------------------------------------------------------------
# SECTION: loading
# ---------------------------------------------------------------------------
def load(path, required=True):
    if not path.exists():
        if required:
            print(f"ERROR: missing {path}", file=sys.stderr)
            sys.exit(2)
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: {path} is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)


def as_list(data, key):
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get(key), list):
        return data[key]
    return None


# ---------------------------------------------------------------------------
# SECTION: main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Validate a Universal Audit artifact folder.")
    parser.add_argument("audit_dir")
    parser.add_argument("--release", action="store_true",
                        help="also enforce the Phase 5 challenge requirement (run before report.md)")
    args = parser.parse_args()
    audit_dir = Path(args.audit_dir)
    errors, warnings = [], []

    manifest = load(audit_dir / "audit-manifest.json")
    audit_id = manifest.get("audit_id", "")
    selected = load(audit_dir / "selected-controls.json")
    controls = {c["control_id"]: c for c in selected.get("controls", [])}

    findings_raw = load(audit_dir / "findings.json", required=False)
    findings = as_list(findings_raw, "findings") if findings_raw is not None else []
    if findings is None:
        errors.append("findings.json: expected an array or {\"findings\": [...]}")
        findings = []
    evidence_raw = load(audit_dir / "evidence-ledger.json", required=False)
    evidence = as_list(evidence_raw, "evidence") if evidence_raw is not None else []
    if evidence is None:
        errors.append("evidence-ledger.json: expected an array or {\"evidence\": [...]}")
        evidence = []
    rejected_raw = load(audit_dir / "rejected-claims.json", required=False)
    rejected = as_list(rejected_raw, "rejected_claims") if rejected_raw is not None else []
    rejected = rejected or []

    finding_schema = load(SCHEMA_DIR / "finding.schema.json")
    evidence_schema = load(SCHEMA_DIR / "evidence.schema.json")
    rejected_schema = load(SCHEMA_DIR / "rejected-claim.schema.json")

    # 1. schema checks
    for i, f in enumerate(findings):
        check(f, finding_schema, f"findings[{f.get('finding_id', i)}]", errors)
    for i, e in enumerate(evidence):
        check(e, evidence_schema, f"evidence[{e.get('evidence_id', i)}]", errors)
    for i, r in enumerate(rejected):
        check(r, rejected_schema, f"rejected[{r.get('claim_id', i)}]", errors)

    # 2. cross references and uniqueness
    evidence_ids = [e.get("evidence_id") for e in evidence]
    finding_ids = [f.get("finding_id") for f in findings]
    claim_ids = [r.get("claim_id") for r in rejected]
    for label, ids in (("evidence_id", evidence_ids), ("finding_id", finding_ids), ("claim_id", claim_ids)):
        duplicates = sorted({i for i in ids if ids.count(i) > 1 and i})
        if duplicates:
            errors.append(f"duplicate {label}: {duplicates}")
        for item in ids:
            if item and audit_id and not str(item).startswith(audit_id):
                errors.append(f"{label} {item} does not start with audit ID {audit_id}")
    evidence_set = set(evidence_ids)
    for f in findings:
        fid = f.get("finding_id", "?")
        for ev in f.get("evidence_ids", []):
            if ev not in evidence_set:
                errors.append(f"{fid}: evidence_id {ev} is not in evidence-ledger.json")
        for cid in f.get("control_ids", []):
            if cid not in controls:
                errors.append(f"{fid}: control_id {cid} is not in selected-controls.json "
                              f"(add it to the selection or correct the mapping)")
        # 3. rules the schema cannot express
        status, severity = f.get("status"), f.get("severity")
        if status == "WARN" and severity == "Critical":
            errors.append(f"{fid}: WARN may not be Critical (spec 13.4)")
        if status == "UNVERIFIED" and severity is not None:
            errors.append(f"{fid}: UNVERIFIED must not carry a severity")
        if status in ("FAIL", "WARN", "NOTE") and severity is None:
            errors.append(f"{fid}: {status} needs a severity")
        if f.get("origin") == "security-hunt" and not f.get("hunt_fingerprint"):
            errors.append(f"{fid}: origin security-hunt without hunt_fingerprint")
        if "needs-control-review" in f.get("cross_tags", []):
            warnings.append(f"{fid}: control mapping was defaulted, confirm the control_id")

    # control rows that claim FAIL/WARN must point at real findings
    finding_set = set(finding_ids)
    for cid, c in controls.items():
        if c.get("status") in ("FAIL", "WARN"):
            linked = c.get("finding_ids", [])
            if not linked:
                errors.append(f"{cid}: status {c['status']} but no finding_ids")
            for fid in linked:
                if fid not in finding_set:
                    errors.append(f"{cid}: finding {fid} not found in findings.json")
    # findings the controls table does not know about
    linked_all = {fid for c in controls.values() for fid in c.get("finding_ids", [])}
    for f in findings:
        if f.get("finding_id") not in linked_all and f.get("status") in ("FAIL", "WARN"):
            warnings.append(f"{f.get('finding_id')}: not linked from any selected control row "
                            f"(score.py will not count it)")

    # 4. secret scan over evidence excerpts and finding text
    scan_targets = [(e.get("evidence_id"), e.get("excerpt", "")) for e in evidence]
    for f in findings:
        for key in ("observable_condition", "technical_risk", "verification", "recommended_fix"):
            scan_targets.append((f"{f.get('finding_id')}.{key}", f.get(key) or ""))
    for label, text in scan_targets:
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(str(text)):
                errors.append(f"{label}: looks like {name}. Sanitize before release.")

    # 5. release gate: challenge required for High/Critical
    if args.release:
        for f in findings:
            high = f.get("severity") in ("Critical", "High") and f.get("status") in ("FAIL", "WARN")
            if high and not f.get("challenge_outcome"):
                errors.append(f"{f.get('finding_id')}: {f.get('severity')} {f.get('status')} "
                              f"has no challenge_outcome (Phase 5 not done)")

    print(f"audit {audit_id}: {len(findings)} findings, {len(evidence)} evidence records, "
          f"{len(rejected)} rejected claims, {len(controls)} selected controls")
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    if errors:
        print(f"RESULT: {len(errors)} error(s). Fix before scoring or releasing.")
        sys.exit(1)
    print("RESULT: clean" + (" (release gate checked)" if args.release else ""))


if __name__ == "__main__":
    main()
