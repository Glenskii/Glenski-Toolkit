# Inbox Guardian for Gmail™

Inbox Guardian is a local tool for people who want a cleaner Gmail inbox without handing mailbox access to a third party. It checks message metadata against rules you control, then reports, quarantines, trashes, or, when deliberately enabled by the owner, permanently removes matching messages.

It is built for a personal mailbox. It does not claim to prove that a message is malicious or that a sender is forged.

Gmail™ is a trademark of Google LLC. This project is not affiliated with or endorsed by Google.

## What it does

- Audits a bounded set of messages without changing mail.
- Uses exact email and domain matching for allowlists and blocklists.
- Creates a `Guardian/Quarantine` label for review-first cleanup.
- Can move a confirmed candidate to Trash.
- Retains an owner-only permanent-purge option for mailboxes where Trash is not a workable holding area.
- Detects `List-Unsubscribe` headers during an audit without sending a request.
- Can install one managed Windows Task Scheduler task after local testing.

## What it does not do

- It does not automatically unsubscribe from mailings.
- It does not assess SPF, DKIM, DMARC, malware, phishing sites, or account compromise.
- It does not guarantee that every detected message is unwanted.
- It does not scan more mail than `max_messages_per_folder` in one run.
- It does not support macOS or Linux scheduling in this release.

## Install

Create a folder outside any public repository. Copy this skill folder into it, then create a virtual environment.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item config.example.json config.json
```

Create your own Google OAuth desktop-client file and save it locally as `credentials.json`. Run the first audit to complete the browser consent flow.

```powershell
python guardian.py --audit
```

`credentials.json`, `token.json`, `config.json`, and `guardian.log` are private local files. Do not commit, upload, email, or include them in support requests.

## Choose a mode

Start with an audit. It prints counts and does not alter Gmail.

```powershell
python guardian.py --audit
```

The standard cleanup mode quarantines candidates.

```powershell
python guardian.py --sweep
```

To use Gmail Trash instead:

```powershell
python guardian.py --action trash --sweep
```

The permanent-purge option is for the mailbox owner only. First set both `allow_owner_purge` to `true` and `oauth_scope_mode` to `"owner_purge"` in the local `config.json`. This asks Google for the wider permanent-delete scope when you next authorize. Then use both flags below.

```powershell
python guardian.py --action purge --sweep --confirm-permanent-delete
```

The utility refuses to purge when either safeguard is missing.

## Block one sender or domain

`--stop-cold` accepts one valid email address or DNS domain. It does not accept Gmail search operators, and it applies exact parsed sender matching before acting.

```powershell
python guardian.py --stop-cold nuisance@example.com
python guardian.py --stop-cold example.net
```

The selected action is still controlled by `action_mode` or `--action`. Review with `--audit` first.

## Unsubscribe review

The audit count includes messages with a `List-Unsubscribe` header. That is a review signal only. Do not automate outgoing unsubscribe requests from this tool. A misleading or hostile header can cause unwanted network activity or disclose that an address is active.

## Scheduling on Windows

After several successful audit or quarantine runs, install the managed task.

```powershell
python guardian.py --install-scheduler
```

The task runs `--once` at the configured interval. This release does not claim that every Windows power configuration will behave the same way. Test it on the machine that will run it, especially if displays or sleep behavior matter.

To remove only this managed task:

```powershell
python guardian.py --uninstall-scheduler
```

Scheduled purging is disabled by default. It requires both `action_mode: "purge"` and `allow_scheduled_purge: true` in the local configuration.

## Privacy and permissions

The tool requests the Gmail API `gmail.modify` scope. Google classifies this as a restricted scope. It can read and modify messages, but it cannot use the immediate permanent-delete endpoint. The optional purge action is therefore not available under this public build's default scope.

For a local owner who genuinely needs permanent deletion, use a separate private configuration and accept the wider `mail.google.com` scope only after reviewing Google's current requirements. Do not turn that mode on in a public distribution.

## Tests

```powershell
python -m unittest discover -s tests -v
```

The tests use a fake Gmail service. They do not access a mailbox or require OAuth credentials.

## License

CC BY 4.0. See [LICENSE](LICENSE).
