# Security and Privacy Policy

## Privacy Statement

Gmail Guardian is local software that runs entirely on your own computer.
- All email analysis, rule checking, and token management happen on your machine.
- No analytics, logs, or email contents are sent to external services or third-party servers.
- The tool communicates only with the official Google Gmail API at `https://gmail.googleapis.com` using your own Google Cloud credentials.

---

## Security Model and Design Rules

### 1. Header Analysis
Spam messages often change the visible sender name to imitate trusted brands while sending from unrelated servers. Gmail Guardian inspects both the visible `From:` header and the hidden `Return-Path:` address to determine where the email actually came from.

### 2. Protection for Legitimate Contacts
To avoid quarantining important messages, the tool applies a clear order of checks:
1. **Protected Mail**: Any message that you star, send, or save as a draft is always marked safe.
2. **Whitelist Priority**: Any sender address or domain in your allowed list always takes priority over keyword filters.
3. **Reputation Tracking**: The tool keeps a local record of people you email. Verified contacts are never quarantined.
4. **Audit First**: The default action is an audit dry-run. It writes a review file so you can verify results before any labels change.

### 3. Minimal Access Permissions
By default, the tool requests only the `https://www.googleapis.com/auth/gmail.modify` permission. This allows reading message headers, adding the quarantine label, and removing the inbox label. It does not request administrative access over your Google account.

---

## How to Revoke Access

If you ever wish to disconnect the tool from your Google account:
1. Visit your [Google Account Third-Party Access Page](https://myaccount.google.com/permissions).
2. Find the application name you created in Google Cloud (for example, `Gmail-Guardian`).
3. Click **Remove Access**.
4. Delete the local `token.json` file from your project folder.
