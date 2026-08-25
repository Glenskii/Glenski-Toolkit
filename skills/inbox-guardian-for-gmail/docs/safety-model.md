# Safety Model

## Purpose

Inbox Guardian helps a mailbox owner apply rules they understand. It does not decide whether an email is malicious. A candidate means that one configured rule matched.

## Decision order

1. Messages labelled Starred, Sent, or Draft are protected.
2. Exact allowlisted email addresses and domains are protected.
3. Exact blocked email addresses and domains become candidates.
4. Subject and configured top-level-domain rules can create candidates.
5. Everything else is reported as legitimate for this limited rule set.

Subdomains match a configured domain. Lookalike domains do not. For example, `mail.example.com` matches `example.com`, while `example.com.bad` does not.

## Actions

Quarantine is the default action. It preserves the message while moving it out of the Inbox. Trash remains reversible through Gmail. Purge is not a public default because it is irreversible.

The owner must enable purge in local configuration, select the owner-purge OAuth mode, and supply the confirmation flag on the command. Scheduled purge requires a fourth local setting.

## Data handling

The utility stores its OAuth token, configuration, and log beside the script. These files can expose mailbox access or mail metadata. Keep them out of version control and support requests.

Message subject and sender logging is off by default. An owner may enable it locally when troubleshooting, then should protect or remove the resulting log.

## Unsubscribe boundary

`List-Unsubscribe` headers are treated as a review signal. The utility does not follow them, call them, or send a one-click unsubscribe request. A header can be misleading or hostile.

## Testing boundary

The bundled tests check decision rules with a fake Gmail service. They do not prove that OAuth, Gmail label operations, Task Scheduler, or a real mailbox will behave as expected. Test on a sacrificial mailbox before enabling scheduled changes.
