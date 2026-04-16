#!/usr/bin/env python3
"""Auto-delete Fidelity marketing emails from Gmail inbox."""
import imaplib, sys

IMAP_HOST = 'imap.gmail.com'
USER = 'tolu.a.shekoni@gmail.com'
PASS = 'hrrg pbml cdlj ifhe'

BLOCKED_SENDERS = [
    '"mail.fidelity.com"',
    '"fidelityinvestments.com"',
]

def run():
    mail = imaplib.IMAP4_SSL(IMAP_HOST, 993)
    mail.login(USER, PASS)
    total_deleted = 0

    for sender in BLOCKED_SENDERS:
        for mailbox in ['"[Gmail]/All Mail"', 'INBOX']:
            try:
                mail.select(mailbox)
            except:
                continue
            s, d = mail.search(None, 'FROM', sender)
            if s != 'OK' or not d[0]:
                continue
            ids = d[0].split()
            if not ids:
                continue
            print(f'Found {len(ids)} emails from {sender} in {mailbox}')
            for mid in ids:
                s, _ = mail.store(mid, '+X-GM-LABELS', '\\Trash')
                if s == 'OK':
                    total_deleted += 1
            mail.expunge()

    mail.logout()
    print(f'Deleted {total_deleted} Fidelity marketing emails')
    return total_deleted

if __name__ == '__main__':
    run()
