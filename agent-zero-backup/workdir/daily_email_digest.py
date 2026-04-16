#!/usr/bin/env python3
"""Daily Email Digest — fetches last 24h of emails, classifies using
memory-palace domain rules, auto-deletes spam, and produces a summary."""

import imaplib
import email
import json
import re
import os
import sys
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta
from collections import Counter, defaultdict

# === Configuration ===
IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
USERNAME = "tolu.a.shekoni@gmail.com"
PASSWORD = "hrrg pbml cdlj ifhe"
DOMAIN_RULES_PATH = "/a0/usr/workdir/memory-palace/wings/technical/rooms/email-domain-rules.md"
OUTPUT_PATH = "/a0/usr/workdir/daily_email_digest.md"

# === Domain Rules (loaded from memory palace) ===
AUTO_DELETE_DOMAINS = [
    "adultfriendfinder.com",
    "sexmatchbook.com",
    "eroticads.com",
    "bumoftheday.net",
    "noreply@youtube.com",
    "plus.google.com",
    "InsideApple.Apple.com",
    "News@InsideApple.Apple.com",
]

PROMO_DOMAINS = [
    "medium.com",
    "masterclass.com",
    "adidas.com",
    "roadtrippers.com",
    "expedia.com",
    "coach.com",
    "moneylion.com",
    "beehiiv.com",
    "bestegg.com",
    "upgrade.com",
    "projectmanagement.com",
    "simplydigital.gr",
    "linkedin.com",
    "glassdoor.com",
    "indeed.com",
    "discord.com",
    "instagram.com",
    "e.upgrade.com",
    "iemail.moneylion.com",
    "mail.bestegg.com",
    "email.bestegg.com",
    "macys.com",
    "emails.macys.com",
    "sephora.com",
    "beauty.sephora.com",
    "homedepot.com",
    "mg.homedepot.com",
    "m.starbucks.com",
    "thexebec.com",
    "overstock.com",
    "promotion.overstock.com",
    "hm.com",
    "email.hm.com",
    "celebritycruises.com",
    "email.celebritycruises.com",
    "on.com",
    "news.on.com",
    "substack.com",
    "nocode.mba",
    "frontendmasters.com",
    "datacamp.com",
    "unstoppabledomains.com",
    "clubhousepediatrics.com",
    "medstarhealth.org",
    "skool.com",
    "coindesk.com",
    "ideabrowser.com",
    "mail.ideabrowser.com",
    "maven.com",
    "courses.maven.com",
    "luma-mail.com",
    "thecut.co",
    "nextdoor.com",
]

IMPORTANT_DOMAINS = [
    ".edu",
    ".gov",
    "bofa.com",
    "bankofamerica.com",
    "wellsfargo.com",
    "chase.com",
    "americanexpress.com",
    "github.com",
    "microsoft.com",
]

IMPORTANT_SUBJECT_KEYWORDS = [
    "statement", "invoice", "receipt", "confirmation",
    "verification", "password", "security", "alert",
    "urgent", "interview", "offer", "contract",
    "agreement", "lease",
]

AUTOMATED_PATTERNS = [
    "noreply", "no-reply", "newsletter", "mailer",
    "mailer-daemon", "notification", "donotreply",
    "notifications@", "news@", "updates@",
    "shop@", "team@", "info@", "support@",
    "marketing@", "special@", "email@",
]


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
    text = ""
    for part in msg.walk():
        ct = part.get_content_type()
        if ct == "text/plain" and not text:
            try:
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                text = payload.decode(charset, errors="replace")
            except Exception:
                pass
        elif ct == "text/html" and not text:
            try:
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                html = payload.decode(charset, errors="replace")
                text = re.sub(r"<[^>]+>", " ", html)
            except Exception:
                pass
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars] + ("..." if len(text) > max_chars else "")


def get_attachments(msg):
    att = []
    for part in msg.walk():
        cd = str(part.get("Content-Disposition", ""))
        if "attachment" in cd:
            fn = part.get_filename()
            if fn:
                att.append(decode_str(fn))
    return att


def classify_email(from_addr, subject, has_attachments):
    """Classify an email into: auto_delete, promo, important, personal, uncategorized"""
    from_lower = (from_addr or "").lower()
    subject_lower = (subject or "").lower()

    # 1. Auto-delete check
    for domain in AUTO_DELETE_DOMAINS:
        if domain.lower() in from_lower:
            return "auto_delete"

    # 2. Important check (specific patterns first)
    for kw in IMPORTANT_SUBJECT_KEYWORDS:
        if kw in subject_lower:
            return "important"
    for domain in IMPORTANT_DOMAINS:
        if domain.lower() in from_lower:
            return "important"
    # Security/account alerts
    security_kws = ["security alert", "account recovered", "new sign-in",
                    "verify your email", "new login", "domain registered",
                    "invoice", "webhook"]
    for kw in security_kws:
        if kw in subject_lower:
            return "important"
    # Google/Apple account alerts
    if "accounts.google.com" in from_lower or "notify.cloudflare.com" in from_lower:
        if any(kw in subject_lower for kw in ["alert", "security", "recovery", "verify"]):
            return "important"
    if has_attachments:
        return "important"

    # 3. Promo check (before personal to catch named-sender promos)
    for domain in PROMO_DOMAINS:
        if domain.lower() in from_lower:
            return "promo"

    # 4. Personal check (not automated)
    is_automated = any(p in from_lower for p in AUTOMATED_PATTERNS)
    if not is_automated:
        return "personal"

    # 5. Everything else
    return "uncategorized"


def main():
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(USERNAME, PASSWORD)
    mail.select("INBOX")

    # Search for emails from last 24 hours
    since_date = (datetime.now() - timedelta(hours=24)).strftime("%d-%b-%Y")
    status, results = mail.search(None, f"SINCE {since_date}")
    msg_ids = results[0].split() if results[0] else []

    if not msg_ids:
        print("No new emails in the last 24 hours.")
        mail.logout()
        return

    print(f"Found {len(msg_ids)} emails since {since_date}")

    # Classify all emails
    classified = {
        "auto_delete": [],
        "promo": [],
        "important": [],
        "personal": [],
        "uncategorized": [],
    }
    promo_counter = Counter()
    auto_delete_counter = Counter()

    for msg_id in msg_ids:
        try:
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                continue
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    raw = response_part[1]
                    msg = email.message_from_bytes(raw)
                    from_h = decode_str(msg.get("From", ""))
                    subject = decode_str(msg.get("Subject", ""))
                    date_h = msg.get("Date", "")
                    try:
                        dt = parsedate_to_datetime(date_h).strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        dt = date_h
                    snippet = get_body_snippet(msg)
                    attachments = get_attachments(msg)

                    # Extract email address from From
                    if "<" in from_h:
                        addr = from_h.split("<")[1].split(">")[0].strip().lower()
                    else:
                        addr = from_h.strip().lower()

                    category = classify_email(addr, subject, bool(attachments))

                    email_data = {
                        "imap_id": msg_id.decode(),
                        "from": from_h,
                        "addr": addr,
                        "subject": subject,
                        "date": dt,
                        "snippet": snippet,
                        "attachments": attachments,
                    }

                    classified[category].append(email_data)

                    if category == "promo":
                        promo_counter[addr] += 1
                    elif category == "auto_delete":
                        auto_delete_counter[addr] += 1
        except Exception as e:
            continue

    # Auto-delete spam
    auto_deleted = 0
    if classified["auto_delete"]:
        for em in classified["auto_delete"]:
            try:
                mail.store(em["imap_id"].encode(), "+X-GM-LABELS", "\\Trash")
                auto_deleted += 1
            except Exception:
                pass
        mail.expunge()

    mail.logout()

    # Build digest
    today = datetime.now().strftime("%A, %B %d, %Y")
    lines = []
    lines.append(f"# Daily Email Digest — {today}")
    lines.append("")
    lines.append(f"**{len(msg_ids)} emails received** | "
                f"{auto_deleted} auto-deleted | "
                f"{len(classified['promo'])} promo | "
                f"{len(classified['important'])} important | "
                f"{len(classified['personal'])} personal")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Important emails
    if classified["important"]:
        lines.append(f"## Warning Action Needed ({len(classified['important'])})")
        lines.append("")
        for i, em in enumerate(classified["important"], 1):
            lines.append(f"### {i}. {em['subject']}")
            lines.append("")
            lines.append("| Field | Value |")
            lines.append("|---|---|")
            lines.append(f"| Date | {em['date']} |")
            lines.append(f"| From | {em['from']} |")
            if em["attachments"]:
                lines.append(f"| Attachments | {', '.join(em['attachments'])} |")
            lines.append("")
            snip_clean = em["snippet"].replace("|", "").replace("\n", " ")[:200]
            lines.append(f"> {snip_clean}")
            lines.append("")
    else:
        lines.append("## Warning Action Needed")
        lines.append("None today!")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Personal emails
    if classified["personal"]:
        lines.append(f"## Personal Emails ({len(classified['personal'])})")
        lines.append("")
        for i, em in enumerate(classified["personal"], 1):
            lines.append(f"### {i}. {em['subject']}")
            lines.append("")
            lines.append("| Field | Value |")
            lines.append("|---|---|")
            lines.append(f"| Date | {em['date']} |")
            lines.append(f"| From | {em['from']} |")
            if em["attachments"]:
                lines.append(f"| Attachments | {', '.join(em['attachments'])} |")
            lines.append("")
            snip_clean = em["snippet"].replace("|", "").replace("\n", " ")[:200]
            lines.append(f"> {snip_clean}")
            lines.append("")
    else:
        lines.append("## Personal Emails")
        lines.append("None today.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Promo summary
    if promo_counter:
        lines.append(f"## Promo/Newsletter Summary ({len(classified['promo'])} from {len(promo_counter)} senders)")
        lines.append("")
        lines.append("| Sender | Count |")
        lines.append("|---|---|")
        for sender, count in promo_counter.most_common():
            lines.append(f"| {sender} | {count} |")
        lines.append("")
    else:
        lines.append("## Promo/Newsletter Summary")
        lines.append("None today.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Auto-delete summary
    if auto_delete_counter:
        lines.append(f"## Auto-Deleted ({auto_deleted} emails)")
        lines.append("")
        lines.append("| Sender | Count |")
        lines.append("|---|---|")
        for sender, count in auto_delete_counter.most_common():
            lines.append(f"| {sender} | {count} |")
        lines.append("")

    # Uncategorized
    if classified["uncategorized"]:
        lines.append("---")
        lines.append("")
        lines.append(f"## Uncategorized ({len(classified['uncategorized'])})")
        lines.append("")
        for i, em in enumerate(classified["uncategorized"], 1):
            lines.append(f"{i}. **{em['subject']}** — {em['from']} ({em['date']})")
            snip_clean = em["snippet"].replace("|", "").replace("\n", " ")[:150]
            lines.append(f"   > {snip_clean}")
            lines.append("")

    output = "\n".join(lines)

    with open(OUTPUT_PATH, "w") as f:
        f.write(output)

    print(output)
    print(f"\nDigest saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
