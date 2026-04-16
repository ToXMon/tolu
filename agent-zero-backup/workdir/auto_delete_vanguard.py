import imaplib
import time

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
    while True:
        try:
            mail = connect()
            mail.select('INBOX')
            status, results = mail.search(None, 'FROM', search_term)

            if status != 'OK' or not results[0]:
                mail.logout()
                break

            msg_ids = results[0].split()
            chunk = msg_ids[:BATCH_SIZE]

            deleted_in_batch = 0
            for mid in chunk:
                try:
                    mail.store(mid, '+X-GM-LABELS', '\\Trash')
                    mail.store(mid, '+FLAGS', '\\Deleted')
                    deleted_in_batch += 1
                except Exception as e:
                    print(f"Error deleting {mid}: {e}")

            mail.expunge()
            mail.logout()

            total_deleted += deleted_in_batch
            print(f"Deleted {deleted_in_batch} emails for {search_term} (total: {total_deleted})")

            if deleted_in_batch < BATCH_SIZE:
                break
            time.sleep(2)

        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(3)
            continue

print(f"Vanguard auto-delete complete. Total: {total_deleted}")
