"""Owner-configured background sweep for Inbox Guardian for Gmail.

This public service is intended for Windows Task Scheduler or another local
scheduler. It applies the configured quarantine or Trash action without a
visible terminal window when started through scripts/run_silent.vbs.

Permanent deletion is disabled by default. It can run only when the owner
sets both ``action`` to ``purge`` and ``purge_blocklisted_messages`` to true.
Purge is limited to messages that match an explicit local blocklist rule.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable

from guardian import GuardianEngine, log, stats


VALID_ACTIONS = {"quarantine", "trash", "purge"}
DEFAULT_OPTIONS = {
    "action": "quarantine",
    "queries": ["in:inbox newer_than:7d"],
    "max_messages_per_query": 50,
    "refresh_dashboard": True,
    "purge_blocklisted_messages": False,
}


def service_options(config: dict) -> dict:
    """Return validated owner options for an unattended local sweep."""
    raw = config.get("scheduled_service", {})
    if not isinstance(raw, dict):
        raw = {}

    options = {**DEFAULT_OPTIONS, **raw}
    action = str(options["action"]).lower().strip()
    if action not in VALID_ACTIONS:
        raise ValueError("scheduled_service.action must be quarantine, trash, or purge.")

    queries = options["queries"]
    if not isinstance(queries, list) or not queries or not all(isinstance(query, str) and query.strip() for query in queries):
        raise ValueError("scheduled_service.queries must be a non-empty list of Gmail search queries.")

    try:
        max_messages = int(options["max_messages_per_query"])
    except (TypeError, ValueError) as error:
        raise ValueError("scheduled_service.max_messages_per_query must be a whole number.") from error
    if not 1 <= max_messages <= 500:
        raise ValueError("scheduled_service.max_messages_per_query must be between 1 and 500.")

    if action == "purge" and options.get("purge_blocklisted_messages") is not True:
        raise ValueError(
            "Purge mode requires scheduled_service.purge_blocklisted_messages to be true."
        )

    return {
        "action": action,
        "queries": [query.strip() for query in queries],
        "max_messages_per_query": max_messages,
        "refresh_dashboard": bool(options["refresh_dashboard"]),
    }


def message_headers(message: dict) -> dict[str, str]:
    return {
        item["name"].lower(): item["value"]
        for item in message.get("payload", {}).get("headers", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str) and isinstance(item.get("value"), str)
    }


def apply_scheduled_action(engine: GuardianEngine, message: dict, options: dict) -> str:
    """Re-evaluate one message and apply the configured owner action."""
    headers = message_headers(message)
    verdict, reason = engine.classify_message(headers, message.get("labelIds", []))
    if not verdict.startswith("QUARANTINE"):
        return "skipped"

    message_id = str(message.get("id", ""))
    if not message_id:
        return "skipped"

    if options["action"] == "purge":
        if verdict != "QUARANTINE_BLOCKLIST":
            return "skipped"
        engine.service.users().messages().delete(userId="me", id=message_id).execute()
        stats.record_neutralization(
            headers.get("from", ""),
            headers.get("subject", ""),
            f"PURGE ({reason})",
        )
        return "purged"

    return engine.execute_quarantine(
        message_id,
        move_to_trash=options["action"] == "trash",
        from_h=headers.get("from", ""),
        subj=headers.get("subject", ""),
        reason=reason,
        rp_h=headers.get("return-path", ""),
    )


def run_once(engine: GuardianEngine | None = None) -> dict[str, int]:
    """Run one configured sweep and return only action counts."""
    engine = engine or GuardianEngine()
    engine.reload_config()
    options = service_options(engine.config)
    counts = {"quarantined": 0, "trashed": 0, "purged": 0, "skipped": 0, "errors": 0}

    seen_ids: set[str] = set()
    for query in options["queries"]:
        messages: Iterable[dict] = engine.fetch_messages_paginated(
            query=query,
            max_results=options["max_messages_per_query"],
        )
        for message in messages:
            message_id = str(message.get("id", ""))
            if not message_id or message_id in seen_ids:
                continue
            seen_ids.add(message_id)
            try:
                outcome = apply_scheduled_action(engine, message, options)
                counts[outcome] = counts.get(outcome, 0) + 1
            except Exception as error:
                counts["errors"] += 1
                log(f"[SERVICE ERROR] {message_id}: {error}")

    log(
        "[SERVICE COMPLETE] "
        f"quarantined={counts['quarantined']} trashed={counts['trashed']} "
        f"purged={counts['purged']} skipped={counts['skipped']} errors={counts['errors']}"
    )

    if options["refresh_dashboard"]:
        try:
            from guardian_dashboard import generate_dashboard_html

            generate_dashboard_html()
        except Exception as error:
            log(f"[DASHBOARD ERROR] {error}")

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one local Inbox Guardian scheduled sweep.")
    parser.add_argument("--once", action="store_true", help="Run one configured local sweep.")
    args = parser.parse_args()
    if not args.once:
        parser.error("Use --once. Your operating-system scheduler controls the interval.")
    run_once()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
