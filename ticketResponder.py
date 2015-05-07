import imaplib
import email
import smtplib
import time
import sys
import json
from pprint import pprint

if len(sys.argv) < 2:
    print "Usage: python emailResponder.py <config_file.json>"
    sys.exit()

with open(sys.argv[1]) as configFile:
    config = json.load(configFile)

senders = []

def notifyMe(username, to, smtpserver):
    body = ''
    header = 'To: '+to+'\n' + 'From: Auto Responder <'+to+'>\n' + 'Subject: Auto-response sent!\n'
    message = header + '\n' + body + '\n\n'
    smtpserver.sendmail(username, to, message)

def sendClaimResponse(config, to, subject):
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(config["username"], config["password"])
    header = 'To:' + to + '\n' + 'From: '+config["name"]+' <'+config["fromEmail"]+'>\n' + 'Subject:'+subject+'\n'
    message = header + '\n' + config["responseMessage"] + '\n\n'
    smtpserver.sendmail(config["username"], to, message)
    if "notificationEmail" in config:
        notifyMe(config["username"], config["notificationEmail"], smtpserver)
    smtpserver.close()

def checkForEmails(config):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(config["username"], config["password"])
    #mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox") # connect to inbox.
    result, data = mail.uid('search', None, '(HEADER Subject "'+config["searchString"]+'" UNSEEN)') # search and return uids instead
#    print str(result)
#    print str(data)
    if len(data) > 0 and len(data[0]) > 0:
        print "New message found..."
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
         
        print email_message['To']
     
        sender = email.utils.parseaddr(email_message['From']) 
        subject = email_message.get("Subject")
        if sender in senders:
            print "Ignoring claimed email from %s,%s..."%sender
        elif subject.startswith("Re:"):
            print "Ignoring response email..."
        else:
            print "Sending claim response to:"
            print sender
            senders.append(sender)
            sendClaimResponse(config, sender[1], "Re: "+subject)
    mail.close()
    mail.logout()

    
while True:
    checkForEmails(config)
    time.sleep(10)
