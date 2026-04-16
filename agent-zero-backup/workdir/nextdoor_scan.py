#!/usr/bin/env python3
"""Scan all Nextdoor emails, summarize locally relevant ones, then delete all."""
import imaplib
import email
from email.header import decode_header
import re
import json
import sys

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
USERNAME = "tolu.a.shekoni@gmail.com"
PASSWORD = "hrrg pbml cdlj ifhe"

# Keywords for local relevance
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
]

JUNK_PATTERNS = [
    "trending posts", "popular posts", "digest",
    "see what", "your neighbors",
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
    """Extract full text body from email."""
    bodies = []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    text = payload.decode(charset, errors="replace")
                    bodies.append(text)
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
                text = payload.decode(charset, errors="replace")
                bodies.append(text)
        except Exception:
            pass
    return "\n".join(bodies)


def is_locally_relevant(subject, body):
    """Check if email content is relevant to local area."""
    combined = (subject + " " + body).lower()
    
    # Direct location matches are always relevant
    if "smallwood" in combined or "monmouth heights" in combined:
        return True
    
    # Check if it's from local area + has relevant keywords
    local_area = any(kw in combined for kw in ["manalapan", "freehold", "marlboro"])
    relevant_topic = any(kw in combined for kw in LOCAL_KEYWORDS)
    
    if local_area and relevant_topic:
        return True
    
    # Strong safety keywords regardless of area
    strong_safety = [
        "crime alert", "break in", "break-in", "burglary",
        "armed robbery", "shooting", "stabbing",
        "sex offender", "child luring", "abduction",
    ]
    if any(kw in combined for kw in strong_safety):
        return True
    
    return False


def extract_post_author(body):
    """Try to extract the post author from Nextdoor email."""
    # Common patterns in Nextdoor emails
    patterns = [
        r"([A-Z][a-z]+ [A-Z][a-z]+)\s*(?:posted|wrote|said|commented|replied)",
        r"(?:from|by)\s+([A-Z][a-z]+ [A-Z][a-z]+)",
        r"^([A-Z][a-z]+ [A-Z][a-z]+)\s*$",
    ]
    for pattern in patterns:
        m = re.search(pattern, body, re.MULTILINE)
        if m:
            return m.group(1)
    return None


def main():
    print("Connecting to Gmail IMAP...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(USERNAME, PASSWORD)
    mail.select("INBOX")

    # Search for all Nextdoor emails
    print("Searching for Nextdoor emails...")
    status, messages = mail.search(None, '(FROM "nextdoor")')
    if status != "OK":
        print("ERROR: search failed")
        mail.logout()
        return

    all_ids = messages[0].split()
    total = len(all_ids)
    print(f"Found {total} Nextdoor emails")

    if total == 0:
        print("No Nextdoor emails found. Done.")
        mail.logout()
        return

    # Process in batches to avoid timeout
    relevant_posts = []
    all_ids_str = [mid.decode() for mid in all_ids]
    
    # Fetch and analyze each email
    print(f"\nScanning {total} emails for local relevance...\n")
    
    for i, msg_id in enumerate(all_ids):
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
                    
                    body = get_full_body(msg)
                    body_clean = body[:2000]  # Limit body for analysis
                    
                    if is_locally_relevant(subject, body_clean):
                        author = extract_post_author(body_clean)
                        # Get a meaningful snippet
                        snippet = body_clean.replace("\n", " ").strip()[:500]
                        relevant_posts.append({
                            "date": date_formatted,
                            "subject": subject,
                            "from": from_h,
                            "author": author,
                            "snippet": snippet,
                        })
                        print(f"  ✓ RELEVANT: [{date_formatted}] {subject[:80]}")
                    
                    if (i + 1) % 50 == 0:
                        print(f"  ... scanned {i + 1}/{total}")
        except Exception as e:
            print(f"  Error on email {i+1}: {e}")
            continue

    print(f"\n=== SCAN COMPLETE ===")
    print(f"Total Nextdoor emails: {total}")
    print(f"Locally relevant: {len(relevant_posts)}")
    
    # Output summary
    if relevant_posts:
        print("\n" + "="*60)
        print("LOCALLY RELEVANT NEXTDOOR POSTS")
        print("="*60)
        for i, post in enumerate(relevant_posts, 1):
            print(f"\n--- Post #{i} ---")
            print(f"Date: {post['date']}")
            print(f"Subject: {post['subject']}")
            if post['author']:
                print(f"Author: {post['author']}")
            print(f"Snippet: {post['snippet'][:400]}")
    else:
        print("\nNo locally relevant Nextdoor posts found.")

    # Save results to JSON for reference
    results = {
        "total_nextdoor_emails": total,
        "locally_relevant_count": len(relevant_posts),
        "relevant_posts": relevant_posts,
        "ids_to_delete": all_ids_str
    }
    with open("/a0/usr/workdir/nextdoor_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to /a0/usr/workdir/nextdoor_results.json")

    # Now delete ALL Nextdoor emails
    print(f"\nDeleting all {total} Nextdoor emails...")
    deleted = 0
    failed = 0
    for msg_id in all_ids:
        try:
            # Move to trash (Gmail-specific)
            status, _ = mail.store(msg_id, '+X-GM-LABELS', '\\Trash')
            if status != 'OK':
                # Fallback: mark as deleted
                mail.store(msg_id, '+FLAGS', '\\Deleted')
            deleted += 1
            if deleted % 50 == 0:
                print(f"  Deleted {deleted}/{total}")
        except Exception as e:
            print(f"  Failed to delete {msg_id}: {e}")
            failed += 1
    
    mail.expunge()
    mail.logout()
    
    print(f"\n=== DELETION COMPLETE ===")
    print(f"Deleted: {deleted}")
    print(f"Failed: {failed}")
    print("Done!")


if __name__ == "__main__":
    main()
