import imaplib
import time
import sys

IMAP_HOST = 'imap.gmail.com'
IMAP_PORT = 993
USER = 'tolu.a.shekoni@gmail.com'
PASS = 'hrrg pbml cdlj ifhe'

BATCH_SIZE = 50
SEARCH_TERMS = ['"vanguard"', '"e-vanguard.com"']

total_deleted = 0

def connect():
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(USER, PASS)
    return mail

for search_term in SEARCH_TERMS:
    print(f"\n=== Searching for emails FROM {search_term} ===")
    batch_count = 0

    while True:
        try:
            mail = connect()
            mail.select('INBOX')
            status, results = mail.search(None, 'FROM', search_term)

            if status != 'OK' or not results[0]:
                print(f"  No more emails found for {search_term}")
                mail.logout()
                break

            msg_ids = results[0].split()
            chunk = msg_ids[:BATCH_SIZE]
            print(f"  Found {len(msg_ids)} total, processing batch of {len(chunk)}")

            deleted_in_batch = 0
            for mid in chunk:
                try:
                    mail.store(mid, '+X-GM-LABELS', '\\Trash')
                    mail.store(mid, '+FLAGS', '\\Deleted')
                    deleted_in_batch += 1
                except Exception as e:
                    print(f"    Error deleting {mid}: {e}")

            mail.expunge()
            mail.logout()

            batch_count += 1
            total_deleted += deleted_in_batch
            print(f"  Batch {batch_count}: deleted {deleted_in_batch} emails (running total: {total_deleted})")

            if deleted_in_batch < BATCH_SIZE:
                print(f"  Finished {search_term} - fewer than batch size deleted")
                break

            time.sleep(2)

        except Exception as e:
            print(f"  Connection error: {e}")
            time.sleep(3)
            continue

print(f"\n{'='*50}")
print(f"TOTAL Vanguard emails deleted: {total_deleted}")
print(f"{'='*50}")
