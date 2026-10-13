Upstream: https://github.com/cloudflare/security-audit-skill
Commit: c1c8a8c (2026-09-14, "Clarify guidance and full audit modes")
License: MIT (see LICENSE)
Vendored into universal-audit on 2026-10-12. Local changes are listed below.

## Local changes

- 2026-10-12: validate-findings.cjs and validate-coverage-ledger.cjs, readFileWithinLimit():
  win32-only fallback. Upstream threw "OS no-follow and nonblocking input protection is
  unavailable" for every input on Windows because Node exposes no O_NOFOLLOW/O_NONBLOCK there.
  The patch does an lstat symlink check and the existing fstat regular-file check on win32
  only. POSIX behaviour is unchanged (still fails closed). Upstream tests on this machine:
  validate-findings 29 pass / 0 fail / 5 skipped (was 22 pass / 7 fail), validate-coverage-ledger
  24 pass / 0 fail / 7 skipped. Skips are POSIX-only symlink/FIFO cases.
- Everything else is byte-identical to upstream c1c8a8c. Re-apply the patch after any upgrade.

- 2026-10-12: entry file SKILL.md renamed PROTOCOL.md, YAML front matter removed, and every
  textual reference to SKILL.md in the vendored markdown rewritten to PROTOCOL.md. Reason: nested
  skill folders can be registered as a second skill by a host, and the Toolkit rule is one skill
  per folder.

## Integration

Driven by the parent skill (see ../../references/security-hunt-integration.md).
Import script: ../../scripts/import-security-hunt.py.
