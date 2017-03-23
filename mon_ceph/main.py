#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
import ConfigParser
import requests
import json
import time
import threading

#导入基准变量
cf = ConfigParser.ConfigParser()
cf.read("./ceph_config")
ceph_api  = cf.get("global", "ceph_api")
recv_api = cf.get("global", "rec_path")
ceph_name = cf.get("global", "ceph_name")
r_header = {"Accept" : "application/json", "Accept-Encoding" : "gzip, deflate, sdch", "Cache-Control": "no-cache", "Pragma" : "no-cache", "Upgrade-Insecure-Requests" : "1", "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}

def post_data_2_kairosdb(postdata):
    print recv_api,
    r = requests.post(recv_api, data=postdata)
    print r.status_code


class ceph_get(object):
    def __init__(self):
        pass
        self.osd_status = "osd/tree"

    def get_osd_status(self, cur_time=int(time.time()),round_time=30):
        '''采集osd的状态，平均上传时间30s'''
        _count_time = cur_time
        if _count_time % round_time != 0:
            pass
        else:
            _osd_status = "%s%s" % (ceph_api, self.osd_status)
            #print _osd_status
            ret = requests.get(_osd_status , headers = r_header)
            ret_body = ret.json()
            post_data = []
            for _osd in ret_body['output']["nodes"]:
                if _osd["type"] == "osd":
                    if _osd["status"] == "up":
                        _osd_value = 1
                    else:
                        _osd_value = 0
                    _tmp_data = {
                        "name": "osd_status",
                        "timestamp": _count_time * 1000,
                        "type": "long",
                        "value": _osd_value,
                        "tags":{"ceph_group": ceph_name, "osd": _osd["name"]},
                        "ttl":round_time
                    }
                    post_data.append(_tmp_data)
            p = json.dumps(post_data)
            post_data_2_kairosdb(p)

    def get_ceph_status(self,cur_time=int(time.time()), round_time=1):
        '''获取mon节点以及磁盘写入情况'''
        _count_time = cur_time
        if _count_time % round_time != 0:
            pass
        else:
            post_data = []
            _ceph_status = "%sstatus" % (ceph_api,)
            ret = requests.get(_ceph_status, headers = r_header)
            ret_body = ret.json()
            ###写入速度
            post_data.append({
                        "name": "ceph_write_bytes_sec",
                        "timestamp": _count_time * 1000,
                        "type": "long",
                        "value": ret_body['output']['pgmap']["write_bytes_sec"],
                        "tags":{"ceph_group": ceph_name },
                    })
            ###读取速度
            post_data.append({
                "name": "ceph_read_bytes_sec",
                "timestamp": _count_time * 1000,
                "type": "long",
                "value": ret_body['output']['pgmap']["read_bytes_sec"],
                "tags":{"ceph_group": ceph_name },
            })
            ###IOPS
            post_data.append({
                "name": "ceph_io_sec",
                "timestamp": _count_time * 1000,
                "type": "long",
                "value": ret_body['output']['pgmap']["op_per_sec"],
                "tags":{"ceph_group": ceph_name },
            })
            ###已使用的存储空间precent
            #print "%0.4f" % (ret_body['output']['pgmap']["bytes_used"] / float(ret_body['output']['pgmap']["bytes_total"]))
            post_data.append({
                "name": "ceph_bytes_used",
                "timestamp": _count_time * 1000,
                #"type": "long",
                "value": "%0.4f" % (int(ret_body['output']['pgmap']["bytes_used"]) /float(ret_body['output']['pgmap']["bytes_total"]),),
                "tags":{"ceph_group": ceph_name },
            })
            ###mon节点状态
            mon_status = ret_body['output']["health"]["timechecks"]['mons']
            for k in mon_status:
                if k['health'] == 'HEALTH_OK':
                    mon_value = 1
                else:
                    mon_value = 0
                post_data.append({
                "name": "ceph_mon_stat",
                "timestamp": _count_time * 1000,
                "type": "long",
                "value": mon_value,
                "tags":{"ceph_group": ceph_name , "mon_name": k['name']},
                })
            p = json.dumps(post_data)
            post_data_2_kairosdb(p)

    def get_pg_status(self,cur_time=int(time.time()), round_time=1):
        _count_time = cur_time
        if _count_time % round_time != 0:
            pass
        else:
            post_data = []
            _ceph_status = "%spg/dump_pools_json" % (ceph_api,)
            ret = requests.get(_ceph_status, headers = r_header)
            ret_body = ret.json()
            _pg_status =  ret_body['output']
            for k in _pg_status:
                post_data.append({
                            "name": "ceph_pg_status_num_objects_sum",
                            "timestamp": _count_time * 1000,
                            "type": "long",
                            "value": k['stat_sum']['num_objects'],
                            "tags":{"ceph_group": ceph_name, "pg_id": k["poolid"] }
                        })
                post_data.append({
                            "name": "ceph_pg_status_num_bytes",
                            "timestamp": _count_time * 1000,
                            "type": "long",
                            "value": k['stat_sum']['num_bytes'],
                            "tags":{"ceph_group": ceph_name, "pg_id": k["poolid"] }
                        })
                post_data.append({
                            "name": "ceph_pg_status_num_objects",
                            "timestamp": _count_time * 1000,
                            "type": "long",
                            "value": k['stat_sum']['num_object_copies'],
                            "tags":{"ceph_group": ceph_name, "pg_id": k["poolid"] }
                        })
                p = json.dumps(post_data)
                post_data_2_kairosdb(p)


def main():
    while True:
        cur_time = int(time.time())
        print cur_time
        k = ceph_get()
        threading.Thread(target=k.get_osd_status, args=(cur_time, 30)).start()
        threading.Thread(target=k.get_ceph_status, args=(cur_time, 30)).start()
        threading.Thread(target=k.get_pg_status, args=(cur_time, 30)).start()
        time.sleep(1)

if __name__ == "__main__":
    main()

# k = ceph_get()
# for i in xrange(1000):
#     cur_time = int(time.time())
#     k.get_osd_status(cur_time=cur_time,round_time=30)
#     k.get_ceph_status(cur_time=cur_time,round_time=30)
#     k.get_pg_status(cur_time=cur_time,round_time=30)
#     time.sleep(1)