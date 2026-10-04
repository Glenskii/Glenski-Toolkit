# Project Log

Durable decisions only, newest at the bottom. Use `scripts/memctl.py log` to append entries. Each entry has four lines: asked, decided, why, shipped. Keep secrets, personal data, and client confidential material out of this file. Older entries rotate into `docs/PROJECT-LOG-ARCHIVE.md`.

<!--
Entry format (example, not a real entry):
## YYYY-MM-DD - Choose SQLite for local cache
asked: which store to use for the offline cache
decided: SQLite through the standard library
why: no extra dependency and enough for the expected data size
shipped: cache module and migration script
-->
