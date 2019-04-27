#!/usr/bin/env python

import email
import os
import smtplib
import subprocess
from imapclient import IMAPClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
 
DEBUG = True
 
HOSTNAME = 'imap.gmail.com'
USERNAME = 'username'
PASSWORD = 'password'
MAILBOX = 'Inbox'
sender = "username@gmail.com"
receiver = "recipient1@gmail.com,recipient2@gmail.com"

NEWMAIL_OFFSET = 0   # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 30 # check mail every 30 seconds
prevHour = int( time.strftime('%H'))

server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
server.login(USERNAME, PASSWORD)

def loop():

    hour = int( time.strftime('%H'))
    global prevHour

    if hour == 00:
        print ("Its midnight!")
        hour = 24

    if (hour - prevHour) == 1:
        print ('Hour= ' + str(hour))
        print ('prevHour= ' + str(prevHour))
        global server
        print ('Renewing session...')
        prevHour = hour
        if hour == 24:
            prevHour = 00
        server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
        server.login(USERNAME, PASSWORD)



#    if DEBUG:
        #print('Logging in as ' + USERNAME)
        #select_info = server.select_folder(MAILBOX)
        #print('%d messages in INBOX' % select_info['EXISTS'])
 
    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])
 
    if DEBUG:
        print "You have", newmails, "new emails!"
        print time.strftime("%Y-%m-%d %H:%M:%S\n")
#        print str(hour) + " " + str(prevHour)

    if newmails > NEWMAIL_OFFSET:
        server.select_folder(MAILBOX, readonly = False)
        email_ids = server.search(['UNSEEN'])
        print email_ids
        apply_lbl_msg = server.copy(email_ids, 'Commands')        
        print apply_lbl_msg
        if apply_lbl_msg == None or apply_lbl_msg == '1':
            print "Deleting command..."
            server.delete_messages(email_ids)
            server.expunge()

        print "Processing images..."
        execfile("copyimages.py")
        image1_data = open("zoneminder/images/1/camera1.jpg", "rb").read()
        image2_data = open("zoneminder/images/2/camera2.jpg", "rb").read()
        image3_data = open("zoneminder/images/3/camera3.jpg", "rb").read()
        image4_data = open("zoneminder/images/4/camera4.jpg", "rb").read()
        image5_data = open("zoneminder/images/5/camera5.jpg", "rb").read()

        print "Constructing e-mail..."
        message = MIMEMultipart()
        message['Subject'] = "Camera Capture"
        message['From'] = sender
        message['To'] = receiver
        text = "Camera Capture - " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        html = '<!DOCTYPE html>\n<html>\n<head></head>\n<body>\n</body>\n</html>\n'
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        message.attach(part1)
        message.attach(part2)
        image1 = MIMEImage(image1_data, name="Camera1")
        image2 = MIMEImage(image2_data, name="Camera2")
        image3 = MIMEImage(image3_data, name="Camera3")
        image4 = MIMEImage(image4_data, name="Camera4")
        image5 = MIMEImage(image5_data, name="Camera5")
        message.attach(image1)
        message.attach(image2)
        message.attach(image3)
        message.attach(image4)
        message.attach(image5)

        try:
           smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
           smtpObj.ehlo()
           smtpObj.starttls()
           smtpObj.ehlo()
           smtpObj.login(sender, 'password')
           smtpObj.sendmail(sender, receiver.split(","), message.as_string())         
           smtpObj.quit()           
           print "Successfully sent email"
        except smtplib.SMTPException:
           print "Error: unable to send email"

     
    time.sleep(MAIL_CHECK_FREQ)
 
if __name__ == '__main__':
    try:
        print 'Press Ctrl-C to quit.'
        while True:
            loop()
    finally:
        print 'Complete'
