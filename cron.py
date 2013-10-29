#! /usr/bin/env python

"""
cron.py

Set this up as a cron to poll the email account for new picture attachments.

Logs in to IMAP server, searches for all unseen/unread emails, parses them for 
an attachment and stores them, then marks the email as read.
"""

from konf import Konf
conf = Konf()

import imaplib, email, os

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(conf.gmail, conf.gpass)
m.select("inbox")

resp, items = m.search(None, "(UNSEEN)")
ids = items[0]
id_list = ids.split()

for id in id_list:
    resp, data = m.fetch(id, "(RFC822)")
    body = data[0][1]
    mail = email.message_from_string(body)
    
    if mail.get_content_maintype() != 'multipart':
        continue
    
    print "[%s]: %s" % (mail["From"], mail["Subject"])
    
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        
        filename = part.get_filename()
        counter = 1
        
        if not filename:
            filename = 'part-%03dbin' % (counter)
            counter += 1
        
        att_path = os.path.join("%s/templates/bootstrap/img/wedding" % os.getcwd(), filename)
        
        if not os.path.isfile(att_path):
            with open(att_path, "wb") as fp:
                fp.write(part.get_payload(decode=True))
    
    m.store(id, '+FLAGS', '\Seen')
