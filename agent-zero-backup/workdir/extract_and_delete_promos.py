import imaplib, email, email.utils, json, re
from email.header import decode_header

def decode_str(s):
    if s is None:
        return ''
    decoded = decode_header(s)
    result = []
    for part, enc in decoded:
        if isinstance(part, bytes):
            result.append(part.decode(enc or 'utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

def get_text(msg):
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/plain':
                try:
                    body = part.get_payload(decode=True).decode(errors='replace')
                except:
                    pass
            elif ct == 'text/html' and not body:
                try:
                    html = part.get_payload(decode=True).decode(errors='replace')
                    body = re.sub(r'<[^>]+>', ' ', html)
                    body = re.sub(r'\s+', ' ', body).strip()
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode(errors='replace')
        except:
            pass
    return body[:3000]

mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login('tolu.a.shekoni@gmail.com', 'hrrg pbml cdlj ifhe')
mail.select('INBOX')

status, data = mail.search(None, '(SINCE 14-Apr-2026)')
all_uids = data[0].split()
print(f'Total UIDs: {len(all_uids)}')

newsletter_senders = ['noreply@medium.com', 'systemdesignone@substack.com']
promo_senders = [
    'noreply@medium.com', 'messages-noreply@linkedin.com', 'systemdesignone@substack.com',
    'shop@emails.macys.com', 'hello@e.roadtrippers.com', 'info@clubhousepediatrics.com',
    'newsletters-noreply@linkedin.com', 'seth@nocode.mba', 'marc@frontendmasters.com',
    'starbucks@m.starbucks.com', 'marketing@thexebec.com', 'noreply@skool.com',
    'homedepotcustomercare@mg.homedepot.com', 'groups-noreply@linkedin.com',
    'on@news.on.com', 'newsletters@coindesk.com', 'bytebytego@substack.com',
    'team@unstoppabledomains.com', 'info@medstarhealth.org',
    'pragmaticengineer+deepdives@substack.com', 'notifications-noreply@linkedin.com',
    'notifications@mail.ideabrowser.com', 'shop@beauty.sephora.com',
    'bestegg@mail.bestegg.com', 'support@email.masterclass.com',
    'special@email.projectmanagement.com', 'blockwareintelligence@substack.com',
    'jobalerts-noreply@linkedin.com', 'reply@ss.email.nextdoor.com',
    'team@datacamp.com', 'invitations@linkedin.com', 'email@promotion.overstock.com',
    'cal-8cma63isigziiyd@calendar.luma-mail.com', 'newsletter@email.hm.com',
    'marily-nika@courses.maven.com', 'kenhuangus@substack.com',
    'updates-noreply@linkedin.com', 'ruben@substack.com', 'aifordevelopers@substack.com',
    'mail@eg.expedia.com', 'bingo@patreon.com', 'causalinf+difference-in-differences@substack.com'
]

newsletter_emails = []
promo_uids = []

for uid in all_uids:
    status, msg_data = mail.fetch(uid, '(RFC822)')
    if status != 'OK':
        continue
    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)
    
    from_header = msg.get('From', '')
    from_addr = email.utils.parseaddr(from_header)[1].lower()
    subject = decode_str(msg.get('Subject', ''))
    
    if from_addr in newsletter_senders:
        body = get_text(msg)
        newsletter_emails.append({
            'uid': uid.decode(),
            'from': from_header,
            'from_addr': from_addr,
            'subject': subject,
            'body': body[:2000]
        })
        print(f'\n=== {from_addr} ===')
        print(f'Subject: {subject}')
        print(f'Body preview: {body[:1500]}')
        print('---')
    
    if from_addr in promo_senders:
        promo_uids.append(uid)

print(f'\n\nNewsletter emails found: {len(newsletter_emails)}')
print(f'Promo UIDs to delete: {len(promo_uids)}')

# Now delete all promos
if promo_uids:
    print(f'\nDeleting {len(promo_uids)} promo emails...')
    for uid in promo_uids:
        mail.store(uid, '+FLAGS', '\\Deleted')
    mail.expunge()
    print(f'Deleted {len(promo_uids)} promo emails successfully.')
else:
    print('No promo emails to delete.')

mail.logout()
print('Done.')
