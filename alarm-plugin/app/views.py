#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
from app import app
from scripts import send_sms
from flask import request
import re

@app.route('/')
def hello_world():
    return 'Hello World!\n'

@app.route("/sms", methods=["POST","GET"])
def sms():
    sms_message = request.form['content']
    sms_phone_list = request.form['tos']
    sms_host = re.sub("(\[|\])","",re.findall("(\[\]|\[[^\]]+])",sms_message)[0])
    sms_content = re.sub("(\[|\])","",re.findall("(\[\]|\[[^\]]+])",sms_message)[1])
    sms_status = re.sub("(\[|\])","",re.findall("(\[\]|\[[^\]]+])",sms_message)[2])
    sms_content = unicode(sms_content).encode("utf-8")
    phonelist = sms_phone_list.split(",")
    if len(phonelist) == 1:
        if sms_status != "OK":
            send_sms.send_sms(str(sms_phone_list), sms_host, sms_content)
        else:
            send_sms.send_sms_normal(str(sms_phone_list), sms_host, sms_content)
    elif len(phonelist) > 1:
        if sms_status != "OK":
            for phonenum in phonelist:
                send_sms.send_sms(str(phonenum),sms_host,sms_content)
        else:
            for phonenum in phonelist:
                send_sms.send_sms_normal(str(phonenum),sms_host,sms_content)
    return "ok"
