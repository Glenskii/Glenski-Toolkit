# Gmail Guardian (v0.1.0)

> A local tool that cleans spam, stops spoofed mail, and quarantines suspicious messages in Gmail.
> It runs on your own computer, uses minimal Google permissions, and never sends your data to third parties.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-19%20passed-brightgreen.svg)]()

---

## What This Tool Does

Gmail Guardian helps you take back control of your inbox. It targets persistent spam, fake security warnings, and spoofed senders while protecting your genuine contacts.

Key features include:

1. **Minimal Permissions**: The tool requests only the `gmail.modify` permission by default. It can read, label, and archive messages without taking full control of your Google account.
2. **Quarantine by Default**: Flagged messages receive the `Guardian/Quarantine` label and move out of your Inbox. You can review and restore any message at any time in Gmail.
3. **Automatic Relay Learning**: When the tool detects spam, it checks the hidden sending server address and automatically adds that domain to your blocklist.
4. **Trusted Contact Protection**: It scans your Sent and Starred messages to build a local list of trusted people. Emails from these contacts are never blocked or moved.
5. **Visual Control Dashboard**: You can open a simple, clear status page in your web browser to see what was caught, view recent activity, and check your rules.
6. **Review Mode by Default**: When you run the tool without extra options, it performs an audit. It writes a review file so you can inspect proposed actions before anything changes.
7. **Safe Unsubscribe Checks**: It lists valid unsubscribe links for you to review manually. It never clicks links automatically, which prevents spammers from confirming that your address is active.
8. **Font Normalization**: Spammers often use fancy math symbols or bold fonts to sneak past standard filters. The tool converts these styled characters back into standard text before scanning.

---

## Requirements

- Python 3.9 or higher
- A personal Gmail or Google Workspace account
- A free Google Cloud OAuth client credentials file (`credentials.json`)

---

## Installation and Setup

### 1. Download and Set Up

#### On macOS and Linux:
```bash
git clone https://github.com/Glenskii/Glenski-Toolkit.git
cd Glenski-Toolkit/skills/inbox-guardian-for-gmail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp config.example.json config.json
```

#### On Windows (PowerShell):
```powershell
git clone https://github.com/Glenskii/Glenski-Toolkit.git
cd Glenski-Toolkit\skills\inbox-guardian-for-gmail
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
copy config.example.json config.json
```

---

### 2. Google Cloud Setup (Takes About 2 Minutes)

To allow the script to connect to your Gmail:

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project named `Gmail-Guardian`.
3. In the left menu, open **APIs & Services**, select **Library**, search for **Gmail API**, and click **Enable**.
4. Open **APIs & Services**, select **OAuth consent screen**:
   - Choose **External** (or Internal for Workspace organizations).
   - Enter an app name and your email address.
   - Under **Test users**, add your Gmail address.
5. Open **APIs & Services**, select **Credentials**:
   - Click **Create Credentials** and choose **OAuth client ID**.
   - Select **Desktop app** as the application type.
   - Download the file, rename it to `credentials.json`, and place it in this project folder.

---

## How to Use the Tool

### 1. Open the Visual Dashboard
To generate and view your status report in your web browser:
```bash
python guardian.py --dashboard
```

### 2. Index Your Trusted Contacts
Scan your Sent and Starred messages to register your frequent contacts:
```bash
python guardian.py --seed-reputation
```

### 3. Print a 24-Hour Summary
To see a quick one-line summary in your terminal:
```bash
python guardian.py --summary
```

### 4. Run an Inbox Audit (Dry Run)
Inspect your recent emails, view classifications, and write a review file:
```bash
python guardian.py
```
This generates a file named `guardian_review_YYYYMMDD_HHMMSS.json`.

### 5. Apply Quarantine from a Review File
Move flagged items to the `Guardian/Quarantine` label based on your audit:
```bash
python guardian.py --execute --review-file guardian_review_20260826_080000.json
```

### 6. Move Flagged Items to Trash
If you prefer moving flagged items directly to Trash:
```bash
python guardian.py --execute --review-file guardian_review_20260826_080000.json --trash
```

### 7. Review Legitimate Unsubscribe Headers
Display messages that contain standard unsubscribe headers:
```bash
python guardian.py --review-unsub
```

---

## Automated Background Schedule (Sleep-Safe)

You can set up your operating system to run quick sweeps automatically without keeping a program open in the background. This allows your monitors and laptop screens to sleep normally.

### Install the Scheduled Task:
```bash
python guardian.py --install-scheduler
```
- On Windows, this creates a task in Windows Task Scheduler.
- On macOS and Linux, this adds an entry to your user crontab.

### Remove the Scheduled Task:
```bash
python guardian.py --uninstall-scheduler
```

---

## Running Tests

To verify that the rules and functions pass all unit tests:
```bash
pytest tests/ -v
```

---

## Security and Privacy

All message processing and rule checks happen directly on your computer. Your emails, tokens, and configuration files are never sent to external servers. For technical details on the security model, see [SECURITY.md](SECURITY.md).

---

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Glen E. Grant.
