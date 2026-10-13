---
name: universal-audit
description: 'Formal, evidence-based software engineering audit producing a scored, gated release verdict. Use when asked for a "full audit", "production audit", "release audit", "formal audit", "audit report with a verdict", "is this safe to ship", customer-assurance review, or a re-audit against a prior report. Runs the Universal Software Engineering Audit Specification v2.2 end to end: intake, control selection, evidence ledger, deterministic scoring, release gates, machine-readable artifacts. NOT for quick cleanup passes or refactoring - use a lighter review flow for those.'
---

# Universal Audit - Formal Production Assurance

This skill executes the **Universal Software Engineering Audit Specification v2.2**
(bundled at `spec/Universal_Software_Engineering_Audit_Specification.md`). The spec is
normative. This file is the execution procedure. When they conflict, the spec wins.

Core discipline, non-negotiable:

- Every conclusion traces to evidence. PASS requires affirmative evidence, never scanner silence.
- Insufficient evidence is **UNVERIFIED**, stated plainly, with what would verify it.
- Never invent defects, never soften verified risk, never pad findings to look thorough.
- The numeric score never overrides release gates.

## Phase 0 - Engagement Setup (blocking)

1. Confirm the target: repo path, running URL, or both. Read `package.json` /
   `requirements.txt` / `wrangler.toml` / equivalent before anything else.
2. Fill the intake from `references/templates/intake-template.md`. Ask the operator only
   for items you cannot establish yourself. Missing inputs go to **Audit Limitations**,
   never silently assumed.
3. Declare: audit type, depth tier (rapid / standard / deep), environment, access level,
   assurance objective, and risk profile (P1–P6, see `references/depth-and-profiles.md`).
   If the operator did not specify depth, propose one with rationale and wait.
4. Assign the audit ID: `AUD-[PRODUCT]-[YYYYMMDD]-[SEQ]`.
5. Rules of Engagement: this skill defaults to **passive, read-only inspection**. No load
   tests, no destructive actions, no auth bypass attempts, no tests against systems the
   operator does not own. Active testing requires the RoE template completed and explicit
   operator authorization recorded in the manifest.
6. Threat model: read `references/threat-intel-2026.md` and use it as input to
   `GOV-THREAT-001`. Its control overlay adds evidence demands to Phases 1 and 2.
   If the target has a project audit plan (for example `docs/audit/AUDIT-PLAN.md`),
   read that too.
7. Gate controls: evaluate `GOV-SCOPE-001` and `GOV-ROE-001` first. If either cannot PASS,
   the engagement is advisory only - say so now, not in the report.
8. Create the artifact directory: `audits/<audit-id>/` in the project root (or an
   operator-specified location).

## Phase 1 - Control Selection

1. Load the catalog: spec Appendix A. Select every control at or below the declared tier
   (Rapid = R; Standard = R+S; Deep = R+S+D). Profile-critical controls are mandatory
   regardless of tier.
2. Mark NOT APPLICABLE controls with recorded justification. NA without justification is
   invalid.
3. Assign each selected control its scoring category from spec A.0. A control without a
   category is a validation failure.
4. Write `selected-controls.json` (schema in `references/schemas/`). This freezes the
   coverage denominator before any evidence is gathered - selection cannot be trimmed
   later to inflate coverage.

## Phase 2 - Evidence Collection

Work the spec Section 12 order. For each selected control, gather the minimum PASS
evidence listed in the catalog or stronger. Practical guidance per family is in
`references/control-procedures.md`.

- Record every material observation in `evidence-ledger.json`: ID, class, timestamp,
  location (file:line, endpoint, config key), method, sanitized excerpt, limitations.
- Repository unavailable: source-dependent claims are `UNVERIFIED - Runtime inference only`.
- Tool output (linters, SCA, scanners) is evidence to assess, not a verdict. Validate
  before accepting severity.
- Sanitize as you go: no secrets, tokens, personal data, or working exploit payloads in
  the ledger.
- For large targets, fan evidence collection out to subagents by control family, one
  ledger merged afterward. Deduplicate observations across families before Phase 3.

### Phase 2b - Security hunt (source targets, code available)

Controls prove a defence exists. A hunt looks for the hole nobody listed. For any audit
with source access, run the bundled hunt protocol in `vendor/security-audit/PROTOCOL.md`
(Cloudflare security-audit, MIT) as the evidence source for the security families
(SEC-*, DATA-TENANT-001, SUP-*, CICD-*, AI-INJECT-001). Full procedure and the exact
mapping: `references/security-hunt-integration.md`. In short:

1. Map the tier to a hunt profile: Rapid -> `quick`, Standard -> `standard`, Deep -> `deep`.
   Record the profile, scope and agent budget in `audit-manifest.json` limitations.
2. Follow `vendor/security-audit/PROTOCOL.md` in full audit mode with its output directory
   OUTSIDE the target repository. Run its validators (`vendor/security-audit/*.cjs`, Node).
3. Import: `python -I scripts/import-security-hunt.py --hunt <hunt-run-dir> --audit-dir audits/<audit-id>`
   confirmed -> FAIL finding, needs_validation -> UNVERIFIED (no severity), rejected ->
   `rejected-claims.json`. Review every finding tagged `needs-control-review`.
4. The hunt's own verification does NOT replace Phase 5: every imported Critical/High
   still goes through the independent challenge.
5. If the hunt could not execute target code (no OS sandbox, the usual case on Windows),
   say so in Audit Limitations. Source-only hunt results stay valid, runtime-dependent ones
   stay UNVERIFIED. Never present a quick or scoped hunt as exhaustive coverage.

## Phase 3 - Findings and Status

1. Assign each selected control exactly one status: PASS / FAIL / WARN / NOTE /
   UNVERIFIED / NOT APPLICABLE.
2. Every FAIL and WARN becomes a finding using the twenty-field standard (spec Section 9),
   written to `findings.json`. Severity is impact, likelihood is separate, confidence is
   separate. Low-confidence concerns normally stay UNVERIFIED.
3. Consolidate duplicates around root causes. Apply the systemic-risk rule (spec 13.5)
   only when all four conditions hold.
4. WARN may not carry Critical severity. A WARN - High on a C3 control must survive the
   Phase 5 challenge or be reclassified FAIL - High.
5. **Rejected claims are recorded, not dropped.** A concern that was raised and then
   disproved (by you, the hunt, or the Phase 5 challenge) goes into `rejected-claims.json`
   with the concrete fact that disproved it, the commit, and its source paths. It carries
   no severity, never affects scoring, and appears in the report under "Claims examined
   and disproved". A changed source path reopens the claim.
6. **Severity discipline for UNVERIFIED.** An UNVERIFIED finding states the exact missing
   fact and a safe way to obtain it. It has no severity (`severity: null`), because a
   blocked hypothesis is not a low-confidence vulnerability.
7. Record `source_ref` and `source_paths` (files the finding depends on) on every finding
   so the re-audit can tell, from the source, whether it still applies.
8. Run the artifact validator before scoring:

   ```
   python -I scripts/validate-audit-artifacts.py audits/<audit-id>
   ```

   It checks schemas, cross references, the severity rules above and a secret scan over
   every excerpt. Fix every ERROR first.

## Phase 4 - Scoring and Verdict

1. Run `scripts/score.py`:

   ```
   python scripts/score.py audits/<audit-id>/selected-controls.json \
       --profile P4 --tier standard --out audits/<audit-id>/score-sheet.json
   ```

   It computes per-category provisional scores, applies the mandatory caps, computes
   tier-relative coverage (and the Standard-denominator figure for Rapid audits),
   validates category mapping, and evaluates the release gates. Do not hand-calculate
   scores; the script is the single source of arithmetic.
2. Select exactly one verdict - APPROVED / APPROVED WITH CONDITIONS / REQUIRES REWORK /
   DO NOT SHIP - from the script's gate evaluation plus the qualitative gates the script
   cannot check (critical-workflow verification, interim-control ownership). Justify the
   verdict against the gates line by line.
3. UNVERIFIED security controls that a hunt could not resolve stay UNVERIFIED and are
   named in the verdict. They are not rounded up to PASS and not rounded down to FAIL.

## Phase 5 - Independent Challenge

Standard tier: run a separate contradiction pass - a fresh subagent that did not author
the findings attempts to refute every Critical/High finding, every release-significant
Medium/WARN, and every C3 PASS supporting approval, and recalculates the score sheet.
Deep tier: the challenge must be a genuinely independent agent or human review.

Record each challenge outcome: UPHELD / MODIFIED / REJECTED / NEEDS MORE EVIDENCE, with
rationale, in `verification-log.json`, and mirror it into each finding's
`challenge_outcome`. A REJECTED outcome moves the finding to `rejected-claims.json`.
Resolve differences transparently.

Imported hunt findings (`origin: security-hunt`) were already verified by a fresh agent
inside the hunt. That reduces, but does not remove, this phase: every Critical/High is
still challenged by an agent that is independent of both the hunt and this audit's author.

## Phase 6 - Report and Release

1. Render `report.md` from `references/templates/report-template.md`. Executive summary
   is seven sentences maximum.
2. Confirm the twelve-point quality gate (spec 19.2). Any failure means the report is not
   ready - fix it, do not ship it annotated. Run
   `python -I scripts/validate-audit-artifacts.py audits/<audit-id> --release`
   first: it fails if any Critical/High finding has no challenge outcome.
3. Final artifact set in `audits/<audit-id>/`: `audit-manifest.json`,
   `selected-controls.json`, `evidence-ledger.json`, `findings.json`, `rejected-claims.json`,
   `score-sheet.json`, `risk-register.json`, `verification-log.json`, `report.md`
   (plus `security-hunt-import-log.json` when a hunt was imported).
4. Deliver the verdict, the top risks, and the coverage figures in the final message.
   Plain language, no alarmism, no softening.

## Re-Audit Mode

If the operator supplies a prior audit ID or report, run spec Section 16 instead of a
fresh Phase 1–3: verify each prior FAIL/WARN against its original reproduction, classify
(OPEN / PARTIALLY REMEDIATED / REMEDIATED / ACCEPTED / REGRESSED / NOT REPRODUCIBLE),
re-run all applicable C3 controls, recalculate from current evidence, and produce the
delta table. Never carry a PASS forward without confirming its evidence still holds.

Decide what is still current from the SOURCE, not from the report date:

```
python -I scripts/reaudit-diff.py --prior audits/<prior-id> --repo <repo> --out audits/<new-id>/reaudit-diff.json
```

- SOURCE_UNCHANGED finding: still carried forward, but re-confirm it on current evidence.
- SOURCE_CHANGED finding: re-validate from scratch. A fix may have landed, or the code
  around it moved.
- SOURCE_UNKNOWN: treat as changed (older audit with no recorded source paths).
- Rejected claim with unchanged source stays suppressed. With changed source it reopens
  as new work. A prior `quick` or scoped hunt only contributes its own evidence, never an
  implied "the rest is fine".

## Scope Control

- A time box changes coverage, not truth standards. Out of time: remaining controls are
  UNVERIFIED and reported as such.
- Never present a limited audit as full production assurance.
- Stop immediately if authorization is exceeded, a test risks material harm, or the
  audited version cannot be established.
