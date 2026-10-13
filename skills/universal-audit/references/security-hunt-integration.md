# Security Hunt Integration

How `universal-audit` uses the vendored `security-audit` protocol (Cloudflare,
`github.com/cloudflare/security-audit-skill`, MIT), vendored in `vendor/security-audit/` with one
Windows validator patch listed in its `UPSTREAM.md`.

## Division of labour

| | security-audit (hunt) | universal-audit (assurance) |
|---|---|---|
| Question | What can an attacker actually do? | Is it safe to ship, and can we prove it? |
| Unit of work | Attack class × subsystem, many isolated agents | Control, scored with an evidence ledger |
| Verdicts | confirmed / needs_validation / rejected | PASS / FAIL / WARN / NOTE / UNVERIFIED / NA |
| Output | findings.json, coverage-ledger.json, REPORT.md | audit folder, score sheet, release verdict |

The hunt is an **evidence source** for the security control families. It never issues a
release verdict, and universal-audit never claims hunt coverage it did not run.

## When to run the hunt

| Situation | Hunt? | Profile |
|---|---|---|
| Source available, tier Standard or Deep | Yes | Standard -> `standard`, Deep -> `deep` |
| Source available, tier Rapid | Optional | `quick`, disclose as partial |
| Black-box or document-only audit | No | Record why in Audit Limitations |
| Re-audit | Yes, scoped to changed paths | `reaudit-diff.json` supplies the scope |

Set an agent budget before starting (it is a strict maximum in the hunt). On a large
target propose a scope or a coarser profile rather than thinning evidence.

## Windows reality

The hunt requires an OS-enforced sandbox before it executes any target code. A plain
Windows machine has none, so the hunt stays **source-only**: it traces and reasons, and
anything that needs execution comes back `needs_validation`. That is valid output, not a
failure. Run it in WSL2 or a container with no network if runtime validation matters.

The upstream findings and coverage validators rejected every input on Windows (no
`O_NOFOLLOW`). The local copies carry a win32-only fallback (lstat symlink check plus
fstat regular-file check). It is not race-safe, which is acceptable for validating a
run directory you created yourself, and POSIX behaviour is unchanged.

## Run

1. Start the hunt with an explicit output directory outside the target, e.g.
   `~/security-audit-skill/<repo>/run-N` (its default).
2. Let it finish both of its terminal states: Phase 6 artifacts written and both of its
   validators passing, or `run_status: "incomplete"` with the reason. If incomplete, the
   audit's coverage statement must say so.
3. Validate the hunt output:
   `node vendor/security-audit/validate-findings.cjs <run>/findings.json`
   `node vendor/security-audit/validate-coverage-ledger.cjs <run>/coverage-ledger.json`

## Import

```
python -I scripts/import-security-hunt.py --hunt <run-dir> --audit-dir audits/<audit-id>
```

| Hunt record | Becomes | Notes |
|---|---|---|
| `confirmed` | `findings.json`: status FAIL, severity from `overall_severity` | trace + evidence -> CODE evidence records |
| `needs_validation` | `findings.json`: status UNVERIFIED, severity `null` | blockers and validation plan kept |
| `rejected` | `rejected-claims.json` | never scored, reopens if its source changes |
| `execution.payloads` | **not imported** | evidence ledger must stay free of exploit material |

Also done by the import: findings are linked into `selected-controls.json`
(`finding_ids`, `evidence_ids`, FAIL + highest severity) so `score.py` counts them. The
import is idempotent, keyed by hunt fingerprint, and preserves a human-set `owner`,
`challenge_outcome` and `remediation_effort` on re-import.

### Control mapping

Keyword rules choose the control (SEC-AUTHZ-001, SEC-SSRF-001, SEC-XSS-001,
SEC-INJECT-001, SEC-TENANT-001, SEC-HOOK-001 and so on). Anything the rules cannot place
falls back to `--default-control` and is tagged `needs-control-review`; the validator
warns on each. Override with `--map map.json` (`{"<fingerprint>": "<control_id>"}`).
If a mapped control is not in `selected-controls.json` the import says so and the
validator errors: add the control to the selection, with a reason, before scoring.

### Severity

The hunt's `overall_severity` is accepted as the starting point only. Re-check it against
the audit's own calibration and the business context in the intake: the hunt scores
technical impact, and the imported `business_impact` text says so.

## After import

1. `python -I scripts/validate-audit-artifacts.py audits/<audit-id>`
2. Run Phase 5 on every Critical/High, including imported ones.
3. `python scripts/score.py ...`
4. `python -I scripts/validate-audit-artifacts.py audits/<audit-id> --release`
5. Report: list rejected claims under "Claims examined and disproved", state hunt profile,
   scope, whether execution was sandboxed, and the hunt's own coverage statement.

## What this integration deliberately does not do

- It does not let a clean hunt turn an UNVERIFIED control into PASS. PASS still needs the
  affirmative evidence the control catalogue lists.
- It does not import hunt prose as a report section. The report stays one document with
  one voice, built from the records.
- It does not lower the evidence bar for `quick`. Profiles change breadth, not standards.
