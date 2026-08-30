# Windows Background Service

This is the full public GitHub build. It can run a local Inbox Guardian sweep every 15 minutes without a command window or focus change.

The task does not prevent the display from sleeping. Windows must be awake for a scheduled run to happen.

## Before You Install

1. Complete `python guardian.py --setup`.
2. Run one manual audit and inspect the resulting review file.
3. Open `config.json` and choose the service action you want.

The default `scheduled_service` action is `quarantine`. It labels and archives messages that match your active rules. It does not delete mail.

```json
"scheduled_service": {
  "action": "quarantine",
  "queries": ["in:inbox"],
  "max_messages_per_query": 50,
  "refresh_dashboard": true,
  "purge_blocklisted_messages": false
}
```

Use `"action": "trash"` to move matching messages to Gmail Trash instead. Gmail keeps Trash items recoverable for its normal retention period.

`"action": "purge"` is an owner-only mode for repeat botnet sources already in your explicit blocklist. Set `"purge_blocklisted_messages": true` as well. Purge skips keyword-only and suspicious-TLD matches. It permanently removes only messages that still match a direct blocklist rule.

## Install the Silent Task

From PowerShell in the skill folder:

```powershell
.\scripts\install-windows-task.ps1
```

The installer registers `InboxGuardianService`. It starts `wscript.exe`, which launches the virtual-environment `pythonw.exe` with no visible terminal window.

To use another interval:

```powershell
.\scripts\install-windows-task.ps1 -IntervalMinutes 30
```

To remove it:

```powershell
.\scripts\install-windows-task.ps1 -Uninstall
```

## Verify Without Changing Mail

Run the service once after setup with the default quarantine action disabled in your local rules, or run an audit instead:

```powershell
python guardian.py --audit
```

Then confirm the task exists:

```powershell
Get-ScheduledTask -TaskName InboxGuardianService
```

The service records local activity in `guardian_stats.json`, updates the local dashboard when configured, and writes operational messages to `guardian.log`. Those files stay on the computer and are excluded from Git.
