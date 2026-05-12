# Email Session SMTP Failure Fallback

- Date observed: 2026-05-11
- Context: Email-session `response` tool attempted SMTP delivery and failed twice with `OSError: [Errno 101] Network is unreachable`.
- Working fallback: `notify_user` out-of-band notification succeeded.
- Operating rule: In the same session, avoid retrying `response` unless the user explicitly asks for another email attempt. Do not send repeated `notify_user` messages when there is no new user instruction.
- Related task: Google Flights alert for Newark/New York to Jackson, June 2026. User was asked whether to track, compare, search alternatives, or ignore.
