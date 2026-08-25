# 🛡️ Gmail Guardian (v0.1.0)

> **Local-first inbox organization and heuristic phishing/spam quarantine engine for Gmail.**
> Built with least-privilege OAuth scopes, review-first safety controls, and zero third-party telemetry.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-15%20passed-brightgreen.svg)]()

---

![Inbox Guardian for Gmail](assets/social-preview.png)

---

![How the system eliminates spam](assets/how-the-system-eliminates-spam.png)

## Fair warning

This is an active personal inbox defence system, not a gentle inbox tidy-up. It can silently cold-block repeat hostile senders and permanently delete messages that meet the owner's configured botnet and spoofing rules. Start with audit mode, protect legitimate mail through allowlists, and test the rules before enabling destructive actions.

Only a verified sender and a verified provider path can be considered for unsubscribe. Unknown, spoofed, or suspicious mail receives no click, request, or reply. An actual unsubscribe tells a verified provider that the mailbox is active, which is why this path must never be used for unverified senders.

---

## ⚡ Core Technical Principles

1. **Least-Privilege Security**: Operates using `https://www.googleapis.com/auth/gmail.modify` by default (read, label, archive). Does not require full mailbox takeover scopes for standard quarantine operations.
2. **Quarantine by Default**: Flagged messages are tagged with the `Guardian/Quarantine` label and archived out of `INBOX`. Messages are preserved for review and never destroyed by default.
3. **Review-First Workflow**: Running the tool with no arguments defaults to `--audit` (dry-run) and outputs a structured JSON review file for inspection before taking action.
4. **Confirmation-Only Unsubscribe**: Displays verified `List-Unsubscribe` headers for manual review without automatically firing network requests to unverified senders.
5. **Unicode Normalization**: Uses `NFKD` normalization to canonicalize mathematical styled fonts (e.g. `𝐥𝐚𝐬𝐭 𝐫𝐞𝐦𝐢𝐧𝐝𝐞𝐫` ➔ `last reminder`) often used to circumvent simple keyword checks.
6. **Strict Input Sanitization**: Validates all email addresses and domains against strict RFC specifications; never interpolates raw input into search queries.

---

## 📋 Prerequisites

- **Python 3.9+**
- A **Gmail / Google Workspace account**
- A **Google Cloud OAuth 2.0 Desktop Client ID** (`credentials.json`)

---

## 🚀 Installation

### 1. Clone & Set Up Virtual Environment

#### **macOS / Linux:**
```bash
git clone https://github.com/Glenskii/Glenski-Toolkit.git
cd Glenski-Toolkit/skills/inbox-guardian-for-gmail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### **Windows (PowerShell):**
```powershell
git clone https://github.com/Glenskii/Glenski-Toolkit.git
cd Glenski-Toolkit/skills/inbox-guardian-for-gmail
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

### 2. Google Cloud OAuth Setup

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g. `Gmail-Guardian`).
3. Navigate to **APIs & Services > Library**, search for **Gmail API**, and click **Enable**.
4. Navigate to **APIs & Services > OAuth consent screen**:
   - Select User Type: **External** (or Internal for Workspace organizations).
   - Set App name and your support email.
   - Under **Test users**, add your own Gmail address.
5. Navigate to **APIs & Services > Credentials**:
   - Click **Create Credentials > OAuth client ID**.
   - Select Application type: **Desktop app**.
   - Download the credentials, rename the file to `credentials.json`, and place it in the project root directory.

---

### 3. Configuration

Initialize your local configuration:
```bash
# macOS / Linux:
cp config.example.json config.json

# Windows:
copy config.example.json config.json
```

Customize `config.json` with your business domains and whitelist rules:
```json
{
  "whitelist_domains": [
    "yourdomain.com",
    "google.com",
    "github.com",
    "linkedin.com"
  ],
  "whitelist_emails": [
    "partner@example.com"
  ],
  "blocklist_domains": [
    "unwanted-pitch.com"
  ],
  "quarantine_label_name": "Guardian/Quarantine"
}
```

---

## 💻 Usage & Workflows

### 1. Run an Inbox Audit (Default / Dry Run)
On first run, this opens your browser for Google OAuth using your own `credentials.json`. After approval, it saves your local `token.json`, inspects recent messages, prints classification decisions, and writes a review JSON file. It does not move, label, or delete mail:
```bash
python guardian.py
```
*Output: Generates `guardian_review_YYYYMMDD_HHMMSS.json`.*

### 2. Execute Quarantine from a Review File
Applies the `Guardian/Quarantine` label and archives flagged items:
```bash
python guardian.py --execute --review-file guardian_review_20260825_090000.json
```

### 3. Move Flagged Items to Trash (Optional)
```bash
python guardian.py --execute --review-file guardian_review_20260825_090000.json --trash
```

### 4. Review Legitimate Unsubscribe Headers
Inspects marketing emails with valid `List-Unsubscribe` headers for manual action (zero auto-clicks):
```bash
python guardian.py --review-unsub
```

### 5. Manage Whitelists & Blocklists
```bash
# Add a trusted domain to whitelist
python guardian.py --add-whitelist-domain "clientcompany.com"

# Add a trusted email
python guardian.py --add-whitelist-email "vip@example.com"

# Block a specific domain
python guardian.py --block-domain "unsolicited-coldoutreach.com"
```

---

## 🧪 Testing

Run the automated test suite:
```bash
pytest tests/ -v
```

---

## 🔒 Security & Privacy

For detailed information on our threat model, least-privilege scoping, and token revocation steps, see [SECURITY.md](SECURITY.md).

---

## 🤝 Contributing

Contributions are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and coding standards.

---

## 📄 License
Released under the [MIT License](LICENSE). Copyright (c) 2026 Glen E. Grant.
