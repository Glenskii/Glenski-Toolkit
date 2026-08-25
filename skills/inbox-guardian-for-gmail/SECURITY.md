# 🔒 Security & Privacy Policy

## Privacy Statement
**Gmail Guardian is 100% local-first software.**
- All processing, classification, and OAuth token management occurs strictly on your local machine.
- Zero analytics, telemetry, or email contents are transmitted to any third-party servers.
- The software communicates solely with the official Google Gmail API (`https://gmail.googleapis.com`) using your own personal Google Cloud OAuth client.

---

## Threat Model & Design Principles

### 1. Header Spoofing & Phishing Detection
- Modern email scams frequently manipulate the RFC 2822 `From:` display name to impersonate trusted brands or users while routing from disposable, unauthorized SMTP relays.
- Gmail Guardian inspects both the visible display header and the raw envelope `Return-Path` to ensure accurate domain extraction.

### 2. False-Positive Prevention (Precedence Hierarchy)
To prevent accidental quarantine of legitimate correspondence:
1. **User Protection**: Any email marked `STARRED` or found in `SENT`/`DRAFT` is unconditionally marked `SAFE`.
2. **Whitelist Priority**: Matches against your `whitelist_domains` or `whitelist_emails` always take precedence over spam keywords or TLD rules.
3. **Review-First Default**: The system operates in `--audit` mode by default, writing a structured review file for inspection before any label modification occurs.

### 3. Least-Privilege OAuth Scopes
- By default, Gmail Guardian requests only `https://www.googleapis.com/auth/gmail.modify`.
- This permission allows reading headers, applying the `Guardian/Quarantine` label, and archiving messages out of `INBOX`.
- It does **not** request administrative domain-level privileges.

---

## Token Revocation & Deauthorization

If you ever wish to revoke Gmail Guardian's access to your Google account:
1. Go to your [Google Account Permissions Dashboard](https://myaccount.google.com/permissions).
2. Locate the app named according to your Google Cloud project (e.g. `Gmail Guardian`).
3. Click **Remove Access**.
4. Delete the local `token.json` file from your project directory.
