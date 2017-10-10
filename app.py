#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import sys
import requests
import datetime
import re
#import logging
#logging.basicConfig(level=logging.DEBUG)
from multiprocessing import Pool
requests.packages.urllib3.disable_warnings()
__auther__ = 'heishan'

class User(object):
    def __init__(self,userName,password):
        self.userName = userName
        self.password = password
    def __str__(self):
        return str('userName=%s,password=%s' % (self.userName,self.password))

userOne = User('180....','//...')
userTwo = User('153....','z.....')
userThree = User('13....','......')
user_pool = [userOne,userTwo,userThree]
class SMZDMDailyException(Exception):
    def __init__(self, req):
        self.req = req

    def __str__(self):
        return str(self.req)

class SMZDMAutoSign(object):
    BASE_URL = 'https://zhiyou.smzdm.com'
    LOGIN_URL = BASE_URL + '/user/login/ajax_check'
    CHECKIN_URL = BASE_URL + '/user/checkin/jsonp_checkin'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'https://www.smzdm.com/'
        }

        params = {
            'username': self.username,
            'password': self.password,
        }

        r = self.session.get(self.BASE_URL, headers=headers, verify=False)
        r = self.session.post(self.LOGIN_URL, data=params, headers=headers)
        if r.status_code != 200:
            raise SMZDMDailyException(r)
        data = r.text
        jdata = json.loads(data)
        if jdata["error_code"] == 0:
            print ("%s登录成功" % self.username)
            return self.auto_ceck()
        else:
            print ("%s登录失败" % self.username)
            return "%s签到失败" % self.username

    def auto_ceck(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'https://www.smzdm.com/'
        }
        r = self.session.get(self.CHECKIN_URL, headers=headers, verify=False)
        if r.status_code != 200:
            raise SMZDMDailyException(r)
        data = r.text
        jdata = json.loads(data)
        if jdata["error_code"] == 0:
            result = jdata["data"]
            return "账户:%s增加积分:%s,金币%s,总积分:%s,等级:%s" % (self.username,result["add_point"],result["gold"],result["point"],result["rank"])
        else:
            return "签到失败了"

def long_time_task(user):
    if user.userName and user.password:
        try:
            smzdm = SMZDMAutoSign(user.userName, user.password)
            result = smzdm.login()
        except SMZDMDailyException as e:
            print('fail', e)
        except Exception as e:
            print('fail', e)
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('签到信息: %s,签到时间:%s' % (result,nowtime))
    else:
        print('SMZDM_USERNAME and SMZDM_PASSWORD can not  be empty ')
        sys.exit()
if __name__ == '__main__':
    p = Pool()
    for user in user_pool:
        p.apply_async(long_time_task, args=(user,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()

