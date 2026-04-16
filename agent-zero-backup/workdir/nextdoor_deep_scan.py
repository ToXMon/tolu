#!/usr/bin/env python3
"""Search all Gmail folders for Nextdoor emails, summarize relevant, delete all."""
import imaplib
import email
from email.header import decode_header
import re
import json

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
USERNAME = "tolu.a.shekoni@gmail.com"
PASSWORD = "hrrg pbml cdlj ifhe"

LOCAL_KEYWORDS = [
    "smallwood", "monmouth heights", "freehold", "manalapan",
    "crime", "safety", "police", "fire", "emergency",
    "road", "street", "traffic", "construction", "paving",
    "school", "marlboro", "township",
    "water", "power", "outage", "sewer",
    "pest", "wildlife", "coyote", "bear", "deer", "tick", "mosquito",
    "flood", "storm", "hurricane", "snow", "weather",
    "theft", "burglar", "suspicious", "scam", "fraud",
    "package", "delivery", "amazon", "stolen",
    "lost pet", "found pet", "dog", "cat", "missing",
    "yard sale", "garage sale", "recommend", "contractor",
    "restaurant", "event", "community", "meeting", "town",
    "development", "zoning", "ordinance", "HOA",
    "speed", "accident", "closure", "detour",
    "covid", "health", "vaccine", "hospital",
    "property", "tax", "assessment",
    "shoprite", "shop rite", "grocery", "store",
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

def get_full_body(msg):
    bodies = []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    bodies.append(payload.decode(charset, errors="replace"))
                except Exception:
                    pass
        if not bodies:
            for part in msg.walk():
                ct = part.get_content_type()
                if ct == "text/html":
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or "utf-8"
                        text = payload.decode(charset, errors="replace")
                        text = re.sub(r"<[^>]+>", " ", text)
                        text = re.sub(r"\s+", " ", text)
                        bodies.append(text)
                    except Exception:
                        pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                bodies.append(payload.decode(charset, errors="replace"))
        except Exception:
            pass
    return "\n".join(bodies)

def is_locally_relevant(subject, body):
    combined = (subject + " " + body).lower()
    if "smallwood" in combined or "monmouth heights" in combined:
        return True
    local_area = any(kw in combined for kw in ["manalapan", "freehold", "marlboro"])
    relevant_topic = any(kw in combined for kw in LOCAL_KEYWORDS)
    if local_area and relevant_topic:
        return True
    strong_safety = [
        "crime alert", "break in", "break-in", "burglary",
        "armed robbery", "shooting", "stabbing",
        "sex offender", "child luring", "abduction",
    ]
    if any(kw in combined for kw in strong_safety):
        return True
    return False

def extract_post_author(body):
    patterns = [
        r"([A-Z][a-z]+ [A-Z][a-z]+)\s*(?:posted|wrote|said|commented|replied)",
        r"(?:from|by)\s+([A-Z][a-z]+ [A-Z][a-z]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, body, re.MULTILINE)
        if m:
            return m.group(1)
    lines = body.split("\n")
    for line in lines:
        line = line.strip()
        if re.match(r"^[A-Z][a-z]+ [A-Z][a-z]+$", line):
            return line
    return None

def main():
    print("Connecting to Gmail IMAP...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(USERNAME, PASSWORD)

    folders_to_search = [
        "INBOX",
        "[Gmail]/All Mail",
        "[Gmail]/Spam",
        "[Gmail]/Trash",
    ]

    all_nextdoor = {}  # folder -> list of IDs
    relevant_posts = []

    for folder_name in folders_to_search:
        try:
            status, _ = mail.select('"' + folder_name + '"', readonly=True)
            if status != "OK":
                continue
            status, messages = mail.search(None, '(OR FROM "nextdoor" SUBJECT "nextdoor")')
            if status != "OK" or not messages[0]:
                print(f"{folder_name}: 0 Nextdoor emails")
                continue
            ids = messages[0].split()
            all_nextdoor[folder_name] = ids
            print(f"{folder_name}: {len(ids)} Nextdoor emails")

            for i, msg_id in enumerate(ids):
                try:
                    status, msg_data = mail.fetch(msg_id, "(RFC822)")
                    if status != "OK":
                        continue
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            raw_email = response_part[1]
                            msg = email.message_from_bytes(raw_email)
                            subject = decode_str(msg.get("Subject", ""))
                            from_h = decode_str(msg.get("From", ""))
                            date_h = msg.get("Date", "")
                            try:
                                parsed_date = email.utils.parsedate_to_datetime(date_h)
                                date_formatted = parsed_date.strftime("%Y-%m-%d")
                            except Exception:
                                date_formatted = date_h[:20]

                            body = get_full_body(msg)[:2000]

                            if is_locally_relevant(subject, body):
                                author = extract_post_author(body)
                                snippet = body.replace("\n", " ").strip()[:500]
                                relevant_posts.append({
                                    "date": date_formatted,
                                    "subject": subject,
                                    "from": from_h,
                                    "author": author,
                                    "snippet": snippet,
                                    "folder": folder_name,
                                })
                                print(f"  RELEVANT: [{date_formatted}] {subject[:80]}")

                            if (i + 1) % 25 == 0:
                                print(f"  ... scanned {i + 1}/{len(ids)} in {folder_name}")
                except Exception as e:
                    print(f"  Error scanning email in {folder_name}: {e}")
        except Exception as e:
            print(f"{folder_name}: Error - {e}")

    print(f"\n{'='*60}")
    print("SCAN COMPLETE")
    print(f"{'='*60}")
    total_all = sum(len(v) for v in all_nextdoor.values())
    print(f"Total Nextdoor emails across all folders: {total_all}")
    print(f"Locally relevant posts: {len(relevant_posts)}")

    if relevant_posts:
        print(f"\n{'='*60}")
        print("LOCALLY RELEVANT NEXTDOOR POSTS")
        print(f"{'='*60}")
        for i, post in enumerate(relevant_posts, 1):
            print(f"\n--- Post #{i} ---")
            print(f"Date: {post['date']}")
            print(f"Subject: {post['subject']}")
            if post.get('author'):
                print(f"Author: {post['author']}")
            print(f"Folder: {post['folder']}")
            print(f"Snippet: {post['snippet'][:400]}")

    # Save results
    results = {
        "total_nextdoor_emails": total_all,
        "locally_relevant_count": len(relevant_posts),
        "relevant_posts": relevant_posts,
        "all_folders": {k: [x.decode() for x in v] for k, v in all_nextdoor.items()},
    }
    with open("/a0/usr/workdir/nextdoor_deep_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to /a0/usr/workdir/nextdoor_deep_results.json")

    # DELETE ALL Nextdoor emails from all folders
    print(f"\n{'='*60}")
    print("DELETING ALL NEXTDOOR EMAILS")
    print(f"{'='*60}")
    total_deleted = 0
    total_failed = 0

    for folder_name, ids in all_nextdoor.items():
        if not ids:
            continue
        print(f"\nDeleting {len(ids)} from {folder_name}...")
        try:
            status, _ = mail.select('"' + folder_name + '"')
            if status != "OK":
                print(f"  Could not select {folder_name} for deletion")
                continue
            for msg_id in ids:
                try:
                    # Gmail: move to trash
                    st, _ = mail.store(msg_id, '+X-GM-LABELS', '\\Trash')
                    if st != 'OK':
                        mail.store(msg_id, '+FLAGS', '\\Deleted')
                    total_deleted += 1
                except Exception as e:
                    print(f"  Failed to delete {msg_id}: {e}")
                    total_failed += 1
            mail.expunge()
            print(f"  Deleted {len(ids)} from {folder_name}")
        except Exception as e:
            print(f"  Error deleting from {folder_name}: {e}")

    mail.logout()
    print(f"\nDELETION COMPLETE: {total_deleted} deleted, {total_failed} failed")

if __name__ == "__main__":
    main()
