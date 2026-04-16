#!/usr/bin/env python3
import imaplib, email, json, re
from email.header import decode_header
from email.utils import parsedate_to_datetime

IMAP_HOST = 'imap.gmail.com'
USER = 'tolu.a.shekoni@gmail.com'
PASS = 'hrrg pbml cdlj ifhe'
TRACKER = '/a0/usr/workdir/email_review_tracker.json'
OUTPUT = '/a0/usr/workdir/email_batch_current.md'

def dh(raw):
    parts = decode_header(raw or '')
    r = []
    for p, c in parts:
        r.append(p.decode(c or 'utf-8', errors='replace') if isinstance(p, bytes) else p)
    return ''.join(r)

def snippet(msg, n=300):
    t = ''
    for part in msg.walk():
        ct = part.get_content_type()
        if ct == 'text/plain' and not t:
            try:
                t = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
            except: pass
        elif ct == 'text/html' and not t:
            try:
                h = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                t = re.sub(r'<[^>]+>', ' ', h)
            except: pass
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n] + ('...' if len(t) > n else '')

def has_att(msg):
    for p in msg.walk():
        if 'attachment' in str(p.get('Content-Disposition', '')): return True
    return False

mail = imaplib.IMAP4_SSL(IMAP_HOST, 993)
mail.login(USER, PASS)
mail.select('"[Gmail]/All Mail"')

# Step 1: Delete batch 7 (emails 281-291)
print('=== Deleting batch 7 (emails 281-291) ===')
with open(TRACKER) as f:
    tr = json.load(f)

s, d = mail.search(None, 'ALL')
all_ids = d[0].split()
print(f'Total emails: {len(all_ids)}')

# Positions 281-291 are indices 280-290 (0-based)
delete_ids = all_ids[280:291]
print(f'Deleting {len(delete_ids)} emails...')
deleted = 0
for mid in delete_ids:
    s, _ = mail.store(mid, '+X-GM-LABELS', '\\Trash')
    if s == 'OK':
        deleted += 1
mail.expunge()
print(f'Trashed {deleted} emails')

# Update tracker - offset goes back to 281 since we deleted from there
tr['emails_deleted'] += deleted
tr['total_emails'] = len(all_ids) - deleted
tr['current_offset'] = 281
print(f'Updated: deleted={tr["emails_deleted"]}, total={tr["total_emails"]}')

# Step 2: Fetch next batch
print('\n=== Fetching batch 8 ===')

# Re-fetch all_ids after deletion
s, d = mail.search(None, 'ALL')
all_ids = d[0].split()
tr['total_emails'] = len(all_ids)
print(f'New total: {len(all_ids)}')

offset = tr['current_offset']
bz = tr['batch_size']
end = offset + bz
batch = all_ids[offset-1:end]
print(f'Fetching emails {offset}-{offset+len(batch)-1} ({len(batch)} emails)')

results = []
for i, mid in enumerate(batch):
    s, d = mail.fetch(mid, '(RFC822)')
    if s != 'OK': continue
    msg = email.message_from_bytes(d[0][1])
    subj = dh(msg.get('Subject', ''))
    frm = dh(msg.get('From', ''))
    to = dh(msg.get('To', ''))
    try:
        dt = parsedate_to_datetime(msg.get('Date', '')).strftime('%Y-%m-%d %H:%M')
    except:
        dt = msg.get('Date', 'Unknown')
    snip = snippet(msg)
    att = has_att(msg)
    results.append({'num': offset+i, 'subject': subj, 'from': frm, 'to': to, 'date': dt, 'snippet': snip, 'attachments': att})
    print(f'  [{offset+i}] {dt} | {frm[:40]} | {subj[:60]}')

# Write output
with open(OUTPUT, 'w') as f:
    f.write(f'# Email Batch {tr["batches_reviewed"]+1} (emails {offset}-{offset+len(batch)-1})\n\n')
    for r in results:
        f.write(f'## Email #{r["num"]}\n')
        f.write(f'| Field | Value |\n|---|---|\n')
        f.write(f'| **From** | {r["from"]} |\n')
        f.write(f'| **To** | {r["to"]} |\n')
        f.write(f'| **Subject** | {r["subject"]} |\n')
        f.write(f'| **Date** | {r["date"]} |\n')
        f.write(f'| **Attachments** | {"Yes" if r["attachments"] else "No"} |\n')
        f.write(f'\n> {r["snippet"]}\n\n---\n\n')

# Update tracker
tr['current_offset'] = end
tr['batches_reviewed'] += 1
tr['emails_reviewed'] += len(batch)
with open(TRACKER, 'w') as f:
    json.dump(tr, f, indent=2)

print(f'\nDone. Next offset: {end}. Reviewed: {tr["emails_reviewed"]}. Deleted total: {tr["emails_deleted"]}')
mail.logout()
