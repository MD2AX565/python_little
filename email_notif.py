#!/usr/bin/python
# -*- coding: UTF-8 -*-
#file email_notif.py

import smtplib
import sys
from datetime import datetime

txtparam=sys.argv[0]
fromaddr = 'YOURCOMP <mail@yandex.ru>'
toaddr = 'Administrator <YOUR@MAIL.com>'
subj = 'Notification from YOURCOMP'
date = datetime.now()
msg_tx1 = 'Hi YOURNAME!\n\n ' + 'Your "COMPNAME" is ON at:'
msg_tx2 = '__________________\n' + 'Have a nice day,\n' + 'Your COMPNAME'
msg = "From: %s\nTo: %s\nSubject: %s\n\n%s\n%s:%s:%s,\t%s-%s-%s\n\n%s"  % ( fromaddr, toaddr, subj, msg_tx1, date.hour, date.minute, date.second, date.day, date.month, date.year, msg_tx2 )

username = 'mail@yandex.ru'
password = 'passwd'

server = smtplib.SMTP_SSL('smtp.yandex.ru:465')  #server = smtplib.SMTP('smtp.gmail.com:587')
server.set_debuglevel(1);                        #server.set_debuglevel(1);
                                                 #server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddr, msg)
server.quit()
