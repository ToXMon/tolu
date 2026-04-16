#!/usr/bin/env python3
import imaplib

IMAP_HOST = 'imap.gmail.com'
USER = 'tolu.a.shekoni@gmail.com'
PASS = 'hrrg pbml cdlj ifhe'

mail = imaplib.IMAP4_SSL(IMAP_HOST, 993)
mail.login(USER, PASS)
mail.select('