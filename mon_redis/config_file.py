#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
#redis服务器
redis_server = "127.0.0.1"
#redis port
port = '6379'
#redis user
redis_passwd = ''
#redis-cli
redis_ctl = "/usr/local/bin/redis-cli"
#mon_config
#监控项目以及上报数据类型
mon_status = {
    "connected_clients" : "GAUGE",
    "used_memory" : "GAUGE",
    "instantaneous_ops_per_sec" : "GAUGE",
    "instantaneous_input_kbps" : "GAUGE",
    "instantaneous_output_kbps" : "GAUGE",
    "rejected_connections" : "COUNTER",
    "expired_keys" : "COUNTER",
    "evicted_keys" : "COUNTER",
    "keyspace_hits" : "COUNTER",
    "keyspace_misses": "COUNTER",
}



