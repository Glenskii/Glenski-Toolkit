from types import SimpleNamespace

import pytest

import guardian_service


def message(message_id="message-1"):
    return {
        "id": message_id,
        "labelIds": ["INBOX"],
        "payload": {
            "headers": [
                {"name": "From", "value": "Bad Sender <sender@bad.example>"},
                {"name": "Return-Path", "value": "<sender@bad.example>"},
                {"name": "Subject", "value": "Blocked your account"},
            ]
        },
    }


class FakeEngine:
    def __init__(self, config, messages=None, verdict="QUARANTINE_BLOCKLIST"):
        self.config = config
        self.messages = messages or [message()]
        self.verdict = verdict
        self.executed = []
        self.deleted = []
        self.service = SimpleNamespace(
            users=lambda: SimpleNamespace(
                messages=lambda: SimpleNamespace(
                    delete=lambda **kwargs: SimpleNamespace(
                        execute=lambda: self.deleted.append(kwargs)
                    )
                )
            )
        )

    def reload_config(self):
        return None

    def fetch_messages_paginated(self, query, max_results):
        assert query == "in:inbox"
        assert max_results == 10
        return self.messages

    def classify_message(self, headers, labels):
        return self.verdict, "Matched explicit blocklist"

    def execute_quarantine(self, message_id, **kwargs):
        self.executed.append((message_id, kwargs))
        return "quarantined"


def options(action="quarantine", purge=False):
    return {
        "scheduled_service": {
            "action": action,
            "queries": ["in:inbox"],
            "max_messages_per_query": 10,
            "refresh_dashboard": False,
            "purge_blocklisted_messages": purge,
        }
    }


def test_service_options_rejects_unarmed_purge():
    with pytest.raises(ValueError, match="purge_blocklisted_messages"):
        guardian_service.service_options(options(action="purge", purge=False))


def test_scheduled_quarantine_uses_existing_engine_action(monkeypatch):
    engine = FakeEngine(options())
    monkeypatch.setattr(guardian_service, "log", lambda message: None)
    counts = guardian_service.run_once(engine)

    assert counts["quarantined"] == 1
    assert engine.executed[0][0] == "message-1"
    assert engine.deleted == []


def test_scheduled_purge_requires_direct_blocklist_match(monkeypatch):
    engine = FakeEngine(options(action="purge", purge=True))
    monkeypatch.setattr(guardian_service, "log", lambda message: None)
    monkeypatch.setattr(guardian_service.stats, "record_neutralization", lambda *args: None)

    counts = guardian_service.run_once(engine)

    assert counts["purged"] == 1
    assert engine.deleted == [{"userId": "me", "id": "message-1"}]


def test_scheduled_purge_skips_non_blocklist_matches(monkeypatch):
    engine = FakeEngine(options(action="purge", purge=True), verdict="QUARANTINE_KEYWORD")
    monkeypatch.setattr(guardian_service, "log", lambda message: None)

    counts = guardian_service.run_once(engine)

    assert counts["skipped"] == 1
    assert engine.deleted == []
