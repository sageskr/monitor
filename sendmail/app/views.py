#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
from app import app
from scripts import sendmail
from flask import request

@app.route("/")
def sendmail_index():
    """默认首页"""
    return "hello sendmail"

@app.route("/chk")
def chk_health():
    """存活检测"""
    return "ok"

@app.route("/mail")
def mail():
    '''发送邮件的主体逻辑'''
    mail_content = request.form["content"]
    mail_list = request.form["tos"]
    mail_subject = request.form['subject']
    mail_to_list  = mail_list.split(",")
    if sendmail.send_mail(mail_to_list,mail_subject,mail_content):
        return "ok"
    else:
        return "false"