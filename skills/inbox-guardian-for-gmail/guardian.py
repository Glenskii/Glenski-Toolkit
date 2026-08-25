#!/usr/bin/env python3
"""Inbox Guardian for Gmail.

Local, review-first mailbox triage. The owner may opt into irreversible
purging only through an explicit local configuration and command confirmation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import unicodedata
from email.utils import parseaddr
from pathlib import Path
from typing import Any, Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

APP_NAME = "Inbox Guardian for Gmail"
TASK_NAME = "InboxGuardian"
MODIFY_SCOPE = "https://www.googleapis.com/auth/gmail.modify"
PURGE_SCOPE = "https://mail.google.com/"
ROOT = Path(__file__).resolve().parent
CREDENTIALS_FILE = ROOT / "credentials.json"
TOKEN_FILE = ROOT / "token.json"
CONFIG_FILE = ROOT / "config.json"
CONFIG_EXAMPLE_FILE = ROOT / "config.example.json"
LOG_FILE = ROOT / "guardian.log"
LABEL_NAME = "Guardian/Quarantine"
VALID_ACTIONS = {"quarantine", "trash", "purge"}

DEFAULT_CONFIG: dict[str, Any] = {
    "version": 1,
    "action_mode": "quarantine",
    "allow_owner_purge": False,
    "allow_scheduled_purge": False,
    "oauth_scope_mode": "modify",
    "whitelist_domains": ["google.com", "github.com"],
    "whitelist_emails": [],
    "blocklist_domains": [],
    "blocklist_senders": [],
    "botnet_suspicious_tlds": [".biz", ".web.id", ".my.id", ".top", ".xyz"],
    "spam_phishing_keywords": [
        "last reminder", "blocked your account", "viruses found", "antivirus expired",
        "account is locked", "unauthorized access",
    ],
    "sweep_interval_minutes": 15,
    "max_messages_per_folder": 200,
    "logging": {"include_message_metadata": False},
}


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFKC", value or "").casefold().strip()


def normalize_domain(value: str) -> str | None:
    """Return a valid lower-case DNS name or None."""
    value = (value or "").strip().casefold().rstrip(".")
    if not value or "@" in value or len(value) > 253:
        return None
    try:
        value = value.encode("idna").decode("ascii")
    except UnicodeError:
        return None
    pattern = r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+"
    return value if re.fullmatch(pattern, value) else None


def normalize_email(value: str) -> str | None:
    """Extract and validate one email address without accepting a display name."""
    _, address = parseaddr(value or "")
    address = address.casefold().strip()
    if not address or address.count("@") != 1 or len(address) > 254:
        return None
    local, domain = address.rsplit("@", 1)
    normalized_domain = normalize_domain(domain)
    if not local or not normalized_domain or any(char.isspace() for char in local):
        return None
    return f"{local}@{normalized_domain}"


def header_email(value: str) -> str | None:
    return normalize_email(value)


def domain_matches(address_domain: str | None, configured_domain: str) -> bool:
    configured = normalize_domain(configured_domain)
    if not address_domain or not configured:
        return False
    return address_domain == configured or address_domain.endswith(f".{configured}")


def merge_config(loaded: dict[str, Any]) -> dict[str, Any]:
    """Migrate known legacy settings and reject invalid configuration."""
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    if not isinstance(loaded, dict):
        raise ValueError("Configuration must be a JSON object.")
    config.update({key: value for key, value in loaded.items() if key in config})
    if isinstance(loaded.get("logging"), dict):
        config["logging"].update(loaded["logging"])
    if "sweep_interval_seconds" in loaded and "sweep_interval_minutes" not in loaded:
        raise ValueError("Use sweep_interval_minutes. sweep_interval_seconds is no longer supported.")
    if config["action_mode"] not in VALID_ACTIONS:
        raise ValueError("action_mode must be quarantine, trash, or purge.")
    if config["oauth_scope_mode"] not in {"modify", "owner_purge"}:
        raise ValueError("oauth_scope_mode must be modify or owner_purge.")
    for key in ("allow_owner_purge", "allow_scheduled_purge"):
        if not isinstance(config[key], bool):
            raise ValueError(f"{key} must be true or false.")
    if not isinstance(config["logging"].get("include_message_metadata"), bool):
        raise ValueError("logging.include_message_metadata must be true or false.")
    if not isinstance(config["sweep_interval_minutes"], int) or not 1 <= config["sweep_interval_minutes"] <= 1440:
        raise ValueError("sweep_interval_minutes must be an integer from 1 to 1440.")
    if not isinstance(config["max_messages_per_folder"], int) or not 1 <= config["max_messages_per_folder"] <= 1000:
        raise ValueError("max_messages_per_folder must be an integer from 1 to 1000.")
    for key in ("whitelist_domains", "whitelist_emails", "blocklist_domains", "blocklist_senders", "botnet_suspicious_tlds", "spam_phishing_keywords"):
        if not isinstance(config[key], list) or not all(isinstance(item, str) for item in config[key]):
            raise ValueError(f"{key} must be a list of strings.")
    return config


def load_config() -> dict[str, Any]:
    source = CONFIG_FILE if CONFIG_FILE.exists() else CONFIG_EXAMPLE_FILE
    if not source.exists():
        return json.loads(json.dumps(DEFAULT_CONFIG))
    with source.open("r", encoding="utf-8") as handle:
        return merge_config(json.load(handle))


def save_config(config: dict[str, Any]) -> None:
    with CONFIG_FILE.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(merge_config(config), handle, indent=2, sort_keys=True)
        handle.write("\n")


def log(message: str) -> None:
    line = f"[{dt.datetime.now().isoformat(timespec='seconds')}] {message}"
    print(line, flush=True)
    with LOG_FILE.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{line}\n")


def scopes_for(config: dict[str, Any]) -> list[str]:
    return [PURGE_SCOPE] if config["oauth_scope_mode"] == "owner_purge" else [MODIFY_SCOPE]


class GmailAuth:
    @staticmethod
    def get_service(scopes: list[str]) -> Any:
        credentials = None
        if TOKEN_FILE.exists():
            credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE), scopes)
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        if not credentials or not credentials.valid or not credentials.has_scopes(scopes):
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_FILE.name}. Create your own local OAuth desktop-client file. Do not publish it."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), scopes)
            credentials = flow.run_local_server(port=0)
            TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")
        return build("gmail", "v1", credentials=credentials)


class GuardianEngine:
    def __init__(self, service: Any | None = None, config: dict[str, Any] | None = None) -> None:
        self.config = merge_config(config) if config is not None else load_config()
        self.service = service if service is not None else GmailAuth.get_service(scopes_for(self.config))
        self._quarantine_label_id: str | None = None

    def _addresses(self, headers: dict[str, str]) -> list[str]:
        values = (header_email(headers.get("from", "")), header_email(headers.get("return-path", "")))
        return [value for value in values if value]

    def is_safe_sender(self, headers: dict[str, str]) -> bool:
        addresses = self._addresses(headers)
        allowed_emails = {value for value in (normalize_email(item) for item in self.config["whitelist_emails"]) if value}
        if any(address in allowed_emails for address in addresses):
            return True
        return any(
            domain_matches(address.rsplit("@", 1)[1], allowed)
            for address in addresses for allowed in self.config["whitelist_domains"]
        )

    def is_blocked_sender(self, headers: dict[str, str]) -> bool:
        addresses = self._addresses(headers)
        blocked_emails = {value for value in (normalize_email(item) for item in self.config["blocklist_senders"]) if value}
        if any(address in blocked_emails for address in addresses):
            return True
        return any(
            domain_matches(address.rsplit("@", 1)[1], blocked)
            for address in addresses for blocked in self.config["blocklist_domains"]
        )

    def check_message(self, headers: dict[str, str], labels: list[str]) -> tuple[str, str]:
        if {"STARRED", "SENT", "DRAFT"}.intersection(labels):
            return "SAFE", "Protected Gmail label"
        if self.is_safe_sender(headers):
            return "SAFE", "Exact whitelist match"
        if self.is_blocked_sender(headers):
            return "CANDIDATE", "Exact blocklist match"
        subject = normalize_text(headers.get("subject", ""))
        for keyword in self.config["spam_phishing_keywords"]:
            if normalize_text(keyword) and normalize_text(keyword) in subject:
                return "CANDIDATE", "Subject rule match"
        for address in self._addresses(headers):
            if any(address.rsplit("@", 1)[1].endswith(tld.casefold()) for tld in self.config["botnet_suspicious_tlds"]):
                return "CANDIDATE", "Configured TLD rule match"
        return "LEGITIMATE", "No configured rule matched"

    def _message(self, message_id: str) -> tuple[dict[str, str], list[str]]:
        metadata = self.service.users().messages().get(
            userId="me", id=message_id, format="metadata",
            metadataHeaders=["From", "Return-Path", "Subject", "List-Unsubscribe", "List-Unsubscribe-Post"],
        ).execute()
        headers = {item["name"].casefold(): item["value"] for item in metadata.get("payload", {}).get("headers", [])}
        return headers, metadata.get("labelIds", [])

    def _iter_message_ids(self, query: str, maximum: int) -> Iterable[str]:
        page_token = None
        yielded = 0
        while yielded < maximum:
            result = self.service.users().messages().list(
                userId="me", q=query, maxResults=min(100, maximum - yielded), pageToken=page_token
            ).execute()
            messages = result.get("messages", [])
            for message in messages:
                yield message["id"]
                yielded += 1
            page_token = result.get("nextPageToken")
            if not page_token or not messages:
                return

    def _quarantine_label(self) -> str:
        if self._quarantine_label_id:
            return self._quarantine_label_id
        labels = self.service.users().labels().list(userId="me").execute().get("labels", [])
        for label in labels:
            if label.get("name") == LABEL_NAME:
                self._quarantine_label_id = label["id"]
                return self._quarantine_label_id
        label = self.service.users().labels().create(
            userId="me", body={"name": LABEL_NAME, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
        ).execute()
        self._quarantine_label_id = label["id"]
        return self._quarantine_label_id

    def _apply_action(self, message_id: str, action: str, confirm_permanent_delete: bool) -> str:
        if action == "quarantine":
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"addLabelIds": [self._quarantine_label()], "removeLabelIds": ["INBOX"]}
            ).execute()
            return "quarantined"
        if action == "trash":
            self.service.users().messages().trash(userId="me", id=message_id).execute()
            return "moved to trash"
        if action == "purge":
            if not self.config["allow_owner_purge"] or self.config["oauth_scope_mode"] != "owner_purge" or not confirm_permanent_delete:
                raise PermissionError("Permanent deletion requires allow_owner_purge=true, oauth_scope_mode=owner_purge, and --confirm-permanent-delete.")
            self.service.users().messages().delete(userId="me", id=message_id).execute()
            return "permanently deleted"
        raise ValueError(f"Unknown action: {action}")

    def sweep(self, action: str | None = None, confirm_permanent_delete: bool = False, query: str = "in:inbox") -> dict[str, int]:
        chosen_action = action or self.config["action_mode"]
        if chosen_action not in VALID_ACTIONS:
            raise ValueError("Unknown action mode.")
        counts = {"scanned": 0, "candidates": 0, "changed": 0, "errors": 0}
        for message_id in self._iter_message_ids(query, self.config["max_messages_per_folder"]):
            counts["scanned"] += 1
            try:
                headers, labels = self._message(message_id)
                verdict, reason = self.check_message(headers, labels)
                if verdict != "CANDIDATE":
                    continue
                counts["candidates"] += 1
                result = self._apply_action(message_id, chosen_action, confirm_permanent_delete)
                counts["changed"] += 1
                if self.config["logging"].get("include_message_metadata"):
                    log(f"{result}: {headers.get('from', '')[:80]} | {headers.get('subject', '')[:120]} | {reason}")
                else:
                    log(f"{result}: message={message_id} | {reason}")
            except Exception as error:
                counts["errors"] += 1
                log(f"message={message_id} was not changed: {error}")
        return counts

    def stop_cold(self, identifier: str, action: str | None, confirm_permanent_delete: bool) -> dict[str, int]:
        target_email = normalize_email(identifier)
        target_domain = normalize_domain(identifier)
        if target_email:
            key, value = "blocklist_senders", target_email
        elif target_domain:
            key, value = "blocklist_domains", target_domain
        else:
            raise ValueError("Provide one valid email address or domain. Gmail search operators are not accepted.")
        config = load_config()
        if value not in config[key]:
            config[key].append(value)
            save_config(config)
            self.config = config
        return self.sweep(action=action, confirm_permanent_delete=confirm_permanent_delete, query="in:anywhere")

    def audit(self, maximum: int | None = None, query: str = "in:inbox") -> dict[str, int]:
        counts: dict[str, int] = {"scanned": 0, "candidate": 0, "legitimate": 0, "safe": 0, "unsubscribe_candidates": 0, "errors": 0}
        for message_id in self._iter_message_ids(query, maximum or self.config["max_messages_per_folder"]):
            counts["scanned"] += 1
            try:
                headers, labels = self._message(message_id)
                verdict, reason = self.check_message(headers, labels)
                counts[verdict.casefold()] += 1
                if headers.get("list-unsubscribe"):
                    counts["unsubscribe_candidates"] += 1
                if self.config["logging"].get("include_message_metadata"):
                    print(f"[{verdict}] {headers.get('from', '')[:80]} | {headers.get('subject', '')[:120]} | {reason}")
                else:
                    print(f"[{verdict}] message={message_id} | {reason}")
            except Exception as error:
                counts["errors"] += 1
                log(f"message={message_id} could not be audited: {error}")
        return counts


def install_scheduler(config: dict[str, Any]) -> None:
    interval = config["sweep_interval_minutes"]
    purge_args = " --confirm-permanent-delete" if config["action_mode"] == "purge" and config["allow_scheduled_purge"] else ""
    if config["action_mode"] == "purge" and not config["allow_scheduled_purge"]:
        raise PermissionError("Scheduled purge is disabled. Set allow_scheduled_purge=true only after testing a local owner configuration.")
    if sys.platform != "win32":
        raise NotImplementedError("Automated scheduling is currently supported only on Windows. Run the script directly on other systems.")
    task_command = f'"{sys.executable}" "{Path(__file__).resolve()}" --once{purge_args}'
    result = subprocess.run(
        ["schtasks.exe", "/Create", "/TN", TASK_NAME, "/TR", task_command, "/SC", "MINUTE", "/MO", str(interval), "/F"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Task Scheduler rejected the task.")
    print(f"Installed {TASK_NAME}: every {interval} minutes.")


def uninstall_scheduler() -> None:
    if sys.platform != "win32":
        raise NotImplementedError("No scheduler is managed on this platform.")
    result = subprocess.run(["schtasks.exe", "/Delete", "/TN", TASK_NAME, "/F"], capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Task Scheduler could not remove the task.")
    print(f"Removed {TASK_NAME}.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Local, review-first inbox triage for Gmail.")
    parser.add_argument("--audit", action="store_true", help="Audit without changing mail.")
    parser.add_argument("--sweep", action="store_true", help="Apply the configured action to candidate messages.")
    parser.add_argument("--once", action="store_true", help="Run one configured sweep for Task Scheduler.")
    parser.add_argument("--action", choices=sorted(VALID_ACTIONS), help="Override the configured action for this run.")
    parser.add_argument("--confirm-permanent-delete", action="store_true", help="Required with owner-enabled purge mode.")
    parser.add_argument("--stop-cold", metavar="EMAIL_OR_DOMAIN", help="Add one validated sender or domain, then run an exact-match sweep.")
    parser.add_argument("--install-scheduler", action="store_true", help="Install the managed Windows task.")
    parser.add_argument("--uninstall-scheduler", action="store_true", help="Remove the managed Windows task.")
    parser.add_argument("--show-config", action="store_true", help="Show the active local configuration.")
    args = parser.parse_args()
    config = load_config()
    if args.show_config:
        print(json.dumps(config, indent=2, sort_keys=True))
        return 0
    if args.install_scheduler:
        install_scheduler(config)
        return 0
    if args.uninstall_scheduler:
        uninstall_scheduler()
        return 0
    engine = GuardianEngine(config=config)
    if args.stop_cold:
        result = engine.stop_cold(args.stop_cold, args.action, args.confirm_permanent_delete)
    elif args.sweep or args.once:
        result = engine.sweep(args.action, args.confirm_permanent_delete)
    else:
        result = engine.audit()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
