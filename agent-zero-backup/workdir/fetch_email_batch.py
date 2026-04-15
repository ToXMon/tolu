#!/usr/bin/env python3
"""Fetch a batch of oldest emails and format for review."""
import imaplib
import email
from email.header import decode_header
import json
import os
import re

TRACKER_PATH = "/a0/usr/workdir/email_review_tracker.json"
OUTPUT_PATH = "/a0/usr/workdir/email_batch_current.md"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
USERNAME = "tolu.a.shekoni@gmail.com"
PASSWORD = "hrrg pbml cdlj ifhe"


def decode_str(s):
    if not s:
        return "(none)"
    try:
        parts = decode_header(s)
        decoded = []
        for part, charset in parts:
            if isinstance(part, bytes):
                decoded.append(part.decode(charset or "utf-8", errors="replace"))
            else:
                decoded.append(part)
        return "".join(decoded)
    except Exception:
        return str(s)


def get_body_snippet(msg, max_chars=300):
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    text = payload.decode(charset, errors="replace")
                    return text[:max_chars].strip()
                except Exception:
                    pass
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/html":
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    text = payload.decode(charset, errors="replace")
                    text = re.sub(r"<[^>]+>", " ", text)
                    text = re.sub(r"\s+", " ", text)
                    return text[:max_chars].strip()
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                text = payload.decode(charset, errors="replace")
                return text[:max_chars].strip()
        except Exception:
            pass
    return "(no preview available)"


def get_attachments(msg):
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            cd = part.get("Content-Disposition", "")
            if "attachment" in cd:
                fn = part.get_filename()
                if fn:
                    attachments.append(decode_str(fn))
    return attachments


def main():
    with open(TRACKER_PATH, "r") as f:
        tracker = json.load(f)

    offset = tracker["current_offset"]
    batch_size = tracker["batch_size"]

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(USERNAME, PASSWORD)
    mail.select("INBOX")

    status, messages = mail.search(None, "ALL")
    all_ids = messages[0].split()
    total = len(all_ids)

    end = min(offset + batch_size - 1, total)
    batch_ids = all_ids[offset - 1 : end]

    if not batch_ids:
        print("No more emails to review!")
        mail.logout()
        return

    results = []
    for i, msg_id in enumerate(batch_ids):
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        if status != "OK":
            continue
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                raw_email = response_part[1]
                msg = email.message_from_bytes(raw_email)
                msg_num = offset + i
                subject = decode_str(msg.get("Subject", ""))
                from_h = decode_str(msg.get("From", ""))
                to_h = decode_str(msg.get("To", ""))
                date_h = msg.get("Date", "")
                cc_h = decode_str(msg.get("Cc", ""))
                try:
                    parsed_date = email.utils.parsedate_to_datetime(date_h)
                    date_formatted = parsed_date.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    date_formatted = date_h
                snippet = get_body_snippet(msg)
                attachments = get_attachments(msg)
                flags_str = msg_data[0][0].decode("utf-8", errors="ignore") if isinstance(msg_data[0][0], bytes) else str(msg_data[0][0])
                is_read = "\\Seen" in flags_str
                results.append(
                    {
                        "num": msg_num,
                        "imap_id": msg_id.decode(),
                        "subject": subject,
                        "from": from_h,
                        "to": to_h,
                        "cc": cc_h,
                        "date": date_formatted,
                        "snippet": snippet,
                        "attachments": attachments,
                        "is_read": is_read,
                    }
                )

    mail.logout()

    lines = []
    lines.append(f"# Email Review Batch #{tracker['batches_reviewed'] + 1}")
    lines.append("")
    lines.append(f"**Emails {offset} to {end} of {total}** | Reviewed so far: {tracker['emails_reviewed']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, r in enumerate(results):
        lines.append(f"## {i + 1}. {r['subject']}")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|---|---|")
        lines.append(f"| Date | {r['date']} |")
        lines.append(f"| From | {r['from']} |")
        lines.append(f"| To | {r['to'][:80]} |")
        if r["cc"]:
            lines.append(f"| CC | {r['cc'][:80]} |")
        if r["attachments"]:
            lines.append(f"| Attachments | {', '.join(r['attachments'])} |")
        lines.append(f"| Read | {'Yes' if r['is_read'] else 'No'} |")
        lines.append(f"| MSG# | {r['num']} |")
        lines.append("")
        snippet_clean = r["snippet"].replace("|", "").replace("\n", " ")[:250]
        lines.append(f"> {snippet_clean}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Your Actions")
    lines.append("Reply with which emails to **KEEP** or **DELETE**.")
    lines.append("Examples: `delete all`, `keep 3 5 7`, `delete 1 2 4 6 8 9 10`, `keep all`, `skip`")
    lines.append("")

    output = "\n".join(lines)

    with open(OUTPUT_PATH, "w") as f:
        f.write(output)

    tracker["current_offset"] = end + 1
    with open(TRACKER_PATH, "w") as f:
        json.dump(tracker, f, indent=2)

    print(output)


if __name__ == "__main__":
    main()
