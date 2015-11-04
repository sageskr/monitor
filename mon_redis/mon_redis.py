#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
import commands
import pub
from config_file import *

def out_check_status():
    dict_result = {}
    '''检查状态，并把可以汇报的值汇总成字典返回'''
    check_cmd = "%s -h %s -p %s info" %(redis_ctl,redis_server,port)
    if redis_passwd not in [None,""]:
        check_cmd = check_cmd + " -a %s" % (redis_passwd,)
    info = commands.getoutput(check_cmd)
    info_split = info.split(u"\r\n")
    for _info in _info_split:
        """这里取巧，因为falcon无法上报非数字的值，因此把非数字结果的都抛弃了"""
        _info_split = _info.split(":")
        if len(_info_split) == 2:
            try:
                dict_result[_info_split[0]] = float(_info_split[1])
            except ValueError:
                continue
    return dict_result


def main():
    push_date = pub.P_data()
    redis_status = out_check_status()
    for mon_key,mon_counterType in mon_status:
        mon_tags="srv=redis,mon=%s" %(mon_key)
        mon_value = redis_status[mon_key]
        push_date(metric=mon_key,value=mon_value,tag=mon_tags)
    push_date.push()

