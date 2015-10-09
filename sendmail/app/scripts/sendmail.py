#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
from email.mime.text import MIMEText
import smtplib, mimetypes
from app import config
def send_mail(to_list,sub,content):
  msg = MIMEText(content,_subtype='html',_charset='utf-8')
  msg['Subject'] = sub
  msg['From'] = config.MailFrom
  msg['To'] = ";".join(to_list)
  try:
    s = smtplib.SMTP()
    s.connect(config.StmpSrv)
    s.login(config.MailUser, config.MailUserPasswd)
    s.sendmail(config.MailFrom, to_list, msg.as_string())
    s.close()
    return True
  except Exception, e:
    print str(e)
    return False