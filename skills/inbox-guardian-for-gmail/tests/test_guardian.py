import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from guardian import GuardianEngine, merge_config, normalize_domain, normalize_email


class FakeMessages:
    def __init__(self):
        self.deleted = []

    def delete(self, **kwargs):
        self.deleted.append(kwargs["id"])
        return self

    def execute(self):
        return {}


class FakeUsers:
    def __init__(self):
        self._messages = FakeMessages()

    def messages(self):
        return self._messages


class FakeService:
    def __init__(self):
        self._users = FakeUsers()

    def users(self):
        return self._users


class GuardianTests(unittest.TestCase):
    def engine(self, **changes):
        config = merge_config(changes)
        return GuardianEngine(service=FakeService(), config=config)

    def test_normalizes_valid_domain_and_email(self):
        self.assertEqual(normalize_domain("Example.COM."), "example.com")
        self.assertEqual(normalize_email("Person <owner@Example.COM>"), "owner@example.com")
        self.assertIsNone(normalize_domain("example.com in:anywhere"))
        self.assertIsNone(normalize_email("not-an-email"))

    def test_whitelist_does_not_match_lookalike_domain(self):
        engine = self.engine(whitelist_domains=["example.com"])
        safe, _ = engine.check_message({"from": "Mail <notice@example.com.bad>"}, [])
        trusted, _ = engine.check_message({"from": "Mail <notice@mail.example.com>"}, [])
        self.assertEqual(safe, "LEGITIMATE")
        self.assertEqual(trusted, "SAFE")

    def test_blocklist_requires_exact_email_or_domain_boundary(self):
        engine = self.engine(blocklist_domains=["example.com"], blocklist_senders=["owner@example.net"])
        wrong, _ = engine.check_message({"from": "owner@example.net.bad"}, [])
        domain, _ = engine.check_message({"from": "notice@alerts.example.com"}, [])
        sender, _ = engine.check_message({"from": "Owner <owner@example.net>"}, [])
        self.assertEqual(wrong, "LEGITIMATE")
        self.assertEqual(domain, "CANDIDATE")
        self.assertEqual(sender, "CANDIDATE")

    def test_protected_labels_override_rules(self):
        engine = self.engine(blocklist_domains=["example.com"])
        verdict, _ = engine.check_message({"from": "spam@example.com"}, ["STARRED"])
        self.assertEqual(verdict, "SAFE")

    def test_subject_and_tld_rules_create_candidates(self):
        engine = self.engine(spam_phishing_keywords=["account is locked"], botnet_suspicious_tlds=[".xyz"])
        subject, _ = engine.check_message({"from": "mail@example.org", "subject": "Account is locked"}, [])
        tld, _ = engine.check_message({"from": "mail@example.xyz"}, [])
        self.assertEqual(subject, "CANDIDATE")
        self.assertEqual(tld, "CANDIDATE")

    def test_purge_requires_three_explicit_owner_controls(self):
        engine = self.engine(action_mode="purge", allow_owner_purge=True, oauth_scope_mode="modify")
        with self.assertRaises(PermissionError):
            engine._apply_action("message-1", "purge", True)
        engine = self.engine(action_mode="purge", allow_owner_purge=True, oauth_scope_mode="owner_purge")
        with self.assertRaises(PermissionError):
            engine._apply_action("message-1", "purge", False)
        self.assertEqual(engine._apply_action("message-1", "purge", True), "permanently deleted")

    def test_legacy_seconds_setting_is_rejected(self):
        with self.assertRaises(ValueError):
            merge_config({"sweep_interval_seconds": 60})

    def test_boolean_safeguards_do_not_accept_strings(self):
        with self.assertRaises(ValueError):
            merge_config({"allow_owner_purge": "false"})


if __name__ == "__main__":
    unittest.main()
