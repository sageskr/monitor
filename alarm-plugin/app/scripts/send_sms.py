#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
import requests
import time
import MySQLdb
#req_url_e 为error错误接口,请填写贵公司的接口地址
req_url_e = ""
#req_url_n 为normal接口,填写贵公司的接口地址
req_url_n = ""
DB_HOST="1.1.1.1"
DB_PORT=3307
DB_USER='test'
DB_PASS='test'

def sql_cursor():
    conn = MySQLdb.Connect(host=DB_HOST,port=DB_PORT,user=DB_USER,passwd=DB_PASS)
    cursor = conn.cursor()
    return cursor

def host2ip(hostname):
    sqlcursor = sql_cursor()
    sql_cmd = "select ip from falcon_portal.host where hostname='%s' order by update_at desc limit 1;" % (hostname,)
    chk = sqlcursor.execute(sql_cmd)
    if chk > 0:
        ip = sqlcursor.fetchone()[0]
    else:
        ip = ".".join(hostname.split('-')[0:3])
    return ip


def send_sms(phone, hostname,content):
    sms_time = time.strftime("%H:%M",time.localtime(time.time()))
    ip = host2ip(hostname)
    requests_url = req_url_e.format(phone, sms_time, ip, content)
    requests.get(requests_url)

def send_sms_normal(phone,hostname,content):
    sms_time = time.strftime("%H:%M",time.localtime(time.time()))
    ip = host2ip(hostname)
    requests_url = req_url_n.format(phone, sms_time, ip, content)
    requests.get(requests_url)

