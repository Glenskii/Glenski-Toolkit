# Python Web App Security Audit

Version 1.1.0

A pytest suite that runs pre-release security checks against your own Python web app, running locally. It works with FastAPI, Django, Flask (through an ASGI adapter), and any other importable ASGI service. It is for developers who want a repeatable check before they ship.

It tests authentication, authorization, hostile input, security headers, CORS, cookies, rate limits, error handling, HTTP methods, and runtime configuration. Each finding states what was tested and where the test stopped.

## Why it exists

A generic scanner does not know your routes, your accounts, your limits, or who owns which record. You tell this suite those things in its config. A default or a skipped route is never counted as a pass.

## What is in the folder

- A pytest suite for common application-layer controls.
- A copy helper that will not overwrite an existing security directory.
- References for frameworks, routes, fixture safety, and assertions.
- A report template and release decision guidance.
- Hard rules: no account creation, no record changes, no destructive database commands.

## How to run it

1. Read [setup and boundaries](references/setup-and-boundaries.md).
2. Install `requirements-security-audit.txt` after using the copy helper, or install this folder's [requirements](requirements.txt).
3. Configure only the routes, users, thresholds, and origins that exist in your app.
4. Use dedicated non-production accounts in an isolated environment.
5. Leave `TEST_ALLOW_ACTIVE_PROBES=false` until the app owner authorizes active checks.
6. Before you enable active checks, set an explicit rate threshold and dedicated target IDs that no one owns.
7. Run `python -m pytest security/ -v` from the project root of the app you are testing.
8. Read every failure before you make a release decision.

## What a result means

`PASS`: the configured checks found nothing blocking and nothing that needs review. It does not prove the app is secure in production.

`REVIEW REQUIRED`: the owner has to make a call.

`BLOCKED`: a confirmed weakness. Fix it before release.

## Documentation

- [Skill instructions](SKILL.md)
- [Setup and boundaries](references/setup-and-boundaries.md)
- [Framework adapters](references/framework-adapters.md)
- [Route configuration](references/route-configuration.md)
- [Fixture safety](references/fixture-safety.md)
- [Assertion catalog](references/assertion-catalog.md)
- [Release decision guide](docs/release-decision-guide.md)
- [Continuous integration guide](docs/continuous-integration-guide.md)

## License

MIT. See [LICENSE](LICENSE).
