#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
import pub
import config
import MySQLdb
from os import popen as ctl


def mysql_conn():
    if config.DB_passwd:
        conn = MySQLdb.Connect(host=config.DB_host, port=config.DB_port, user=config.DB_user, passwd=config.DB_passwd)
    else:
        conn = MySQLdb.Connect(host=config.DB_host, port=config.DB_port, user=config.DB_user)
    cursor =  conn.cursor()
    return cursor


def get_mysql_status():
    my_cursor = mysql_conn()
    qps_cmd = "show  global  status like 'Question%';"
    my_cursor.execute(qps_cmd)
    cur_counter = my_cursor.fetchall()[0][1]
    tps_cmd_commit = "show global status like 'Com_commit'; "
    my_cursor.execute(tps_cmd_commit)
    cur_commit_counter = my_cursor.fetchall()[0][1]
    tps_cmd_rollback = "show global status like 'Com_rollback';"
    my_cursor.execute(tps_cmd_rollback)
    cur_rollback_counter = my_cursor.fetchall()[0][1]
    tps_counter = cur_rollback_counter + cur_commit_counter
    return cur_counter, tps_counter


def get_delay_time():
    if config.DB_passwd:
        delay_cmd = "mysql -u%s -p%s -h%s -P%d -e 'show slave status;'" % (config.DB_user, config.DB_passwd, config.DB_host, config.DB_port)
    else:
        delay_cmd = "mysql -u%s  -h%s -P%d -e 'show slave status;'" % (config.DB_user, config.DB_host, config.DB_port)
    slave_status = ctl(delay_cmd).readlines()
    if len(slave_status) == 2:
        delay_position = slave_status[0].split("\t").index("Seconds_Behind_Master")
        delay_time = slave_status[1].split("\t")[delay_position]
    else:
        delay_time = 0
    return delay_time


def main():
    cur_counter, tps_counter = get_mysql_status()
    delay_time = get_delay_time()
    push_date = pub.P_data()
    push_date.add(metric="Question", value=cur_counter, tag="srv=mysql")
    push_date.add(metric="QPS", value=cur_counter, tag="srv=mysql", counterType="COUNTER")
    push_date.add(metric="Transaction", value=tps_counter, tag="srv=mysql")
    push_date.add(metric="TPS", value=tps_counter, tag="srv=mysql", counterType="COUNTER")
    push_date.add(metric="Seconds_Behind_Master", value=delay_time, tag="srv=mysql")
    push_date.push()


if __name__ == "__main__":
    main()