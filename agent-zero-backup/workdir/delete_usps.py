import imaplib, re

with open('/a0/usr/workdir/fetch_email_batch.py') as f:
    content = f.read()

username = re.search(r'USERNAME = "(.+?)"', content).group(1)
password = re.search(r'PASSWORD = "(.+?)"', content).group(1)

mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login(username, password)
mail.select('INBOX')

status, data = mail.search(None, '(FROM "USPSInformeddelivery" SUBJECT "Daily Digest")')
if status == 'OK' and data[0]:
    ids = data[0].split()
    print(f'Found {len(ids)} matching email(s)')
    for msg_id in ids:
        result = mail.store(msg_id, '+X-GM-LABELS', '\\Trash')
        print(f'Trashed message {msg_id.decode()}: {result[0]}')
    mail.expunge()
    print('Done - email moved to trash')
else:
    print('No matching emails found')

mail.logout()
