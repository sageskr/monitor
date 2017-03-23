#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
import xml.etree.cElementTree as ET
import json
import time
import requests
print time.time()
headers = {"Accept" : "application/json", "Accept-Encoding" : "gzip, deflate, sdch", "Cache-Control": "no-cache", "Pragma" : "no-cache", "Upgrade-Insecure-Requests" : "1", "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}
ret = requests.get("http://10.120.18.23:5000/api/v0.1/pg/dump_pools_json", headers = headers)
r_xml =  ret.json()
pg_stat = r_xml['output']
print pg_stat[8]['stat_sum']['num_objects']
for _pg in pg_stat:
    pass
# status_num = pg_stat['stat_sum']
# print status_num
# for k,v in status_num.items():
#     print k,v