#!/bin/env python
#-*- encoding:utf-8 -*-
#公共的信息集合为一个文件
import requests
from time import time
import json
push_path = "127.0.0.1:1988"

class P_data(object):
    '''聚合成一个类，用于操作欲上传的内容'''
    def __init__(self):
        self.result = []
        self.Endpoint = get_endpoint()
        self.ts = int(time())

    def add(self,metric,value,tag,counterType="GAUGE",step=60):
        self.result.append({
            "endpoint" : self.Endpoint,
            "metric": metric,
            "timestamp" : self.ts,
            "step": step,
            "value": value,
            "counterType": counterType,
            "tags": tag,
        })
    def get(self):
        return self.result
    def out(self):
        return json.dumps(self.result)
    def push(self):
        r = requests.post("http://%s/v1/push" % (push_path,), data=self.out())

def get_endpoint():
    from socket import gethostname
    return gethostname()