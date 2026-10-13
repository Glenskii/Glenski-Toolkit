# Threat Intelligence Overlay, 2026

Read in **Phase 0**, as input to `GOV-THREAT-001`. The spec controls stay
normative. This file shows where current attacker behaviour lands on the catalog,
and what evidence to demand, so the threat model reflects how attacks actually
happen in 2026 rather than a textbook list.

Compiled 22 September 2026 from public reporting (sources at the end). Re-check
anything older than six months before relying on it.

---

## 1. The five shifts that change how evidence is judged

| # | Shift | Headline evidence | What it changes in an audit |
|---|---|---|---|
| S1 | **Exploitation windows have collapsed** | 88% of exploitation of public-PoC vulnerabilities happened within 48 hours of the PoC (CrowdStrike, H1 2026). China-nexus actors attacked within 24 hours of a critical web flaw. React2Shell (CVE-2025-55182, CVSS 10) produced 800+ leads across 80+ victims in four days. | "We patch monthly" is a FAIL for internet-facing code. Judge `INF-PATCH-001`, `SUP-DEP-001` and `CICD-DEPLOY-001` on **hours to production**, and on whether anyone is actually alerted. |
| S2 | **Identity is the way in** | Device-code phishing up 15x in six months, and it bypasses MFA. Vishing doubled. One group went from account takeover to data theft in under five minutes. eCrime activity aimed at cloud up 171%. | MFA alone does not PASS `SEC-MFA-001`. Ask which OAuth flows are allowed (device code), how long tokens last, and whether every privileged console and vendor login uses phishing-resistant factors. |
| S3 | **Supply chain has moved upstream** | One actor compromised 300+ dependencies in a day, then used them to get into cloud accounts. 131 AI-framework packages were poisoned through one dependency. 87% of registry threats were npm. The Shai-Hulud worm spread through npm maintainer accounts using `postinstall`. | `SUP-DEP-001/002` need pinning, lockfile integrity and install-script policy, not just "npm audit clean". A clean scan today says nothing about the next install. |
| S4 | **AI is a tool, a target and a force multiplier** | AI-agent activity produces 2.5x the detection leads of human activity, so it is hard to tell from legitimate AI work. An LLMJacking campaign made about 200K API requests in two minutes on stolen AI access. One prompt-injection payload made Claude Code, Gemini CLI and Copilot all leak repository secrets ("Comment and Control", April 2026; Anthropic rated it CVSS 9.4). | Always include **the development process** in scope: AI coding agents that hold production credentials are privileged identities. `CODE-AI-001`, `AI-INJECT-001`, `SEC-SECRET-001`, `ADM-LEAST-001` apply even when the product has no AI feature. |
| S5 | **Trusted platforms are used for delivery** | Card skimmers stored inside Stripe customer metadata, delivered through compromised Google Tag Manager containers. Phishing kits running on Cloudflare Workers. | A trusted vendor domain in a CSP allow list is not proof of safety. `SEC-WEB-001` needs a script inventory and SRI, not just "the script is from a big name". |

---

## 2. Control overlay: extra evidence to demand

For each control, the minimum evidence in spec Appendix A still applies. These are
**additional** questions that 2026 attacks make necessary. If the answer is missing,
the control is UNVERIFIED, not PASS.

### Identity and access (S2, S4)

| Control | Ask for |
|---|---|
| `SEC-MFA-001` | 2FA state on every privileged account, **including vendor dashboards** (cloud, registrar, DNS, payments, email provider, code host). Phishing-resistant factors (passkey, hardware key) for owners. Organisation-level "require 2FA" switched on at the code host. |
| `SEC-AUTHN-001..003` | Whether OAuth **device-code** flow is allowed for any account the organisation uses, and whether it can be blocked. Help-desk and reset paths that a voice caller could abuse. |
| `SEC-SESS-001/002` | Token lifetime, revocation on password change, and how long a stolen session or device-trust cookie stays useful. |
| `INF-IAM-001`, `ADM-LEAST-001` | Every API token: scope, IP restriction, expiry, owner, last used. Tokens that can delete (for example `delete_repo`) or write to the database held on a developer laptop. |
| `ADM-TRACE-001`, `OPS-AUDIT-001` | Whether the audit trail records **who**, from **where** (IP, country, ASN, device), for sign-in failures as well as successes, and for vendor-side changes (new account members, new tokens). A 2026 report describes an attacker adding themselves as an account member first. |
| `ADM-BREAK-001` | A recovery path that does not depend on the one mailbox an attacker would take over first. |

### Supply chain (S3)

| Control | Ask for |
|---|---|
| `SUP-DEP-001` | Lockfile committed and used (`npm ci`, not `npm install`). Direct dependencies pinned or range-limited with a reason. Count of transitive packages. |
| `SUP-DEP-002` | Who is alerted to a new advisory, and how fast. Absence of any alerting (no Dependabot, no feed) is a finding under S1. |
| `SUP-BUILD-001` | Install scripts: `ignore-scripts` policy, or a reviewed allow list. Where builds run, and whether secrets are present in that environment during install. |
| `CICD-SECRET-001` | Whether a pull request or changed `package.json` can reach the deploy token before review (a Wrangler token theft path was reported in September 2026). With no CI, check the laptop that deploys. |
| `SEC-WEB-001`, `SEC-XSS-001` | Inventory of every third-party script on pages that take payment or sign-in. SRI on static scripts. CSP that names hosts, with no wildcard on payment pages. Tag managers treated as full code execution. |

### AI in the build and in the product (S4)

| Control | Ask for |
|---|---|
| `CODE-AI-001` | Which AI agents write or deploy code; which credentials they can read (`.env`, API tokens, `gh` auth); whether they read untrusted content (inbound email, web pages, member uploads, issues) in the same session. **Private data + untrusted content + a way to send data out = exploitable.** |
| `AI-INJECT-001` | If the product has an AI feature: indirect injection through stored content. If not: record NA for the product, but assess the development agents under `CODE-AI-001`. |
| `COST-ABUSE-001` | Any metered API (AI, email, SMS, maps) whose key could be stolen and run up at LLMJacking speed. Spend caps and alerts. |
| `SEC-SECRET-001/002` | Secrets reachable by an AI session, and whether sessions can be limited to read-only or given short-lived, narrow tokens. |

Use OWASP **Top 10 for Agentic Applications 2026** (ASI01 goal hijack, ASI02 tool
misuse, ASI03 identity and privilege abuse, ASI04 agentic supply chain, ASI05
unexpected code execution, ASI06 memory and context poisoning, ASI07 inter-agent
communication, ASI08 cascading failures, ASI09 human-agent trust exploitation,
ASI10 rogue agents) as the sub-checklist whenever agents hold real credentials.

### Speed of response (S1)

| Control | Ask for |
|---|---|
| `INF-PATCH-001` | Measured time from advisory to deployed fix, on a real example. Target: under 48 hours for internet-facing critical issues. |
| `CICD-DEPLOY-001`, `CICD-ROLL-001` | How many people can deploy, from where, and how fast a rollback happens. One person on one machine is a single point of failure for incident response. |
| `OPS-IR-001` | A written first-hour plan: revoke tokens, rotate secrets, block at the edge, preserve logs. Who does it if the developer is unreachable. |
| `INF-NET-001` | Whether an edge rule can be written, **proved** (for example with a request tracer) and deployed in minutes. |

### Privacy and recovery (Canada)

| Control | Ask for |
|---|---|
| `OPS-IR-001`, `PRIV-NOTICE-001` | PIPEDA: breaches that pose a **real risk of significant harm** must be reported to the Privacy Commissioner and the people affected. **Every** breach, reportable or not, must be recorded and the record kept **24 months**. Check a breach register exists. PIPEDA applies to non-profits carrying on commercial activity (membership sales count). |
| `BAK-*` | An off-platform, encrypted backup the organisation can reach without the developer. Point-in-time recovery inside the same account does not protect against losing the account. |

---

## 3. Fast checks worth running first

Cheap, high-yield, and read-only:

1. Code host: organisation 2FA requirement; members with 2FA off; token scopes on the deploy machine.
2. Cloud account: member list, 2FA per member, API tokens with scope and expiry, recent membership changes.
3. `npm audit`, lockfile present, direct dependency ranges, `postinstall` scripts in the tree.
4. Every `<script src>` on payment and sign-in pages; CSP and SRI.
5. Where `.env` files live and which agent sessions can read them.
6. Time from last dependency advisory to deployed fix, from git history.

---

## 4. Sources

- [CrowdStrike 2026 Threat Hunting Report](https://www.crowdstrike.com/en-us/blog/crowdstrike-2026-threat-hunting-report/): exploitation windows, LLMJacking, supply chain actors, device-code and vishing figures
- [Help Net Security: suppliers, logins and AI tools are attack paths](https://www.helpnetsecurity.com/2026/08/06/crowdstrike-cyber-threat-trends-report/)
- [SiliconANGLE: AI systems under direct attack as exploit windows shrink](https://siliconangle.com/2026/08/03/crowdstrike-finds-ai-systems-direct-attack-exploit-windows-shrink/)
- [Datadog Security Labs: React2Shell, CVE-2025-55182](https://securitylabs.datadoghq.com/articles/cve-2025-55182-react2shell-remote-code-execution-react-server-components/)
- [Google Cloud: threat actors exploit React2Shell](https://cloud.google.com/blog/topics/threat-intelligence/threat-actors-exploit-react2shell-cve-2025-55182)
- [Unit 42: npm threat landscape and mitigations](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/)
- [CSA Singapore: Shai-Hulud advisory, 2026](https://www.csa.gov.sg/alerts-and-advisories/advisories/ad-2026-009/)
- [Truesec: Shai-Hulud, disable postinstall](https://www.truesec.com/hub/blog/500-npm-packages-compromised-in-ongoing-supply-chain-attack-shai-hulud)
- [The Hacker News: device-code phishing hits 340+ Microsoft 365 orgs](https://thehackernews.com/2026/03/device-code-phishing-hits-340-microsoft.html)
- [Help Net Security: AI-enabled device-code phishing](https://www.helpnetsecurity.com/2026/04/07/microsoft-device-code-phishing-campaign/)
- [VentureBeat: three AI coding agents leaked secrets through one prompt injection](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026)
- [Help Net Security: prompt injection drives most agentic failures](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [Wrangnarok issue: PR code can steal the Cloudflare deploy token](https://github.com/Midtown-Technology-Group/Wrangnarok/issues/376)
- [The Hacker News: Cloudflare Workers Spectre attack (mitigated)](https://thehackernews.com/2026/08/cloudflare-workers-spectre-attack-leaks.html)
- [Reflectiz: the Stripe-hosted skimmer](https://www.reflectiz.com/blog/stripe-skimmer-2026/)
- [Office of the Privacy Commissioner: mandatory breach reporting](https://www.priv.gc.ca/en/privacy-topics/business-privacy/breaches-and-safeguards/privacy-breaches-at-your-business/gd_pb_201810/)
