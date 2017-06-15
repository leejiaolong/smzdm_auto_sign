#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import sys
import requests
import re
from multiprocessing import Pool
from user_obj import User
__auther__ = 'heishan'

userOne = User('','')
userTwo = User('','')
user_pool = [userOne,userTwo]

class SMZDMDailyException(Exception):
    def __init__(self, req):
        self.req = req

    def __str__(self):
        return str(self.req)

class SMZDMAutoSign(object):
    BASE_URL = 'http://zhiyou.smzdm.com'
    LOGIN_URL = BASE_URL + '/user/login/ajax_check'
    CHECKIN_URL = BASE_URL + '/user/checkin/jsonp_checkin'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def checkin(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'http://www.smzdm.com/'
        }

        params = {
            'username': self.username,
            'password': self.password,
        }

        r = self.session.get(self.BASE_URL, headers=headers, verify=False)
        r = self.session.post(self.LOGIN_URL, data=params, headers=headers, verify=False)
        r = self.session.get(self.CHECKIN_URL, headers=headers, verify=False)
        if r.status_code != 200:
            raise SMZDMDailyException(r)

        data = r.text
        jdata = json.loads(data)

        return jdata
def long_time_task(user):
    print('Begin stak at %s' % user.userName)
    if user.userName and user.password:
        try:
            smzdm = SMZDMAutoSign(user.userName, user.password)
            result = smzdm.checkin()
        except SMZDMDailyException as e:
            print('fail', e)
        except Exception as e:
            print('fail', e)

        print('success', result)
    else:
        print('SMZDM_USERNAME and SMZDM_PASSWORD can not  be empty ')
        sys.exit()
    print('end stak at %s' % user.userName)

if __name__ == '__main__':
    p = Pool()
    for user in user_pool:
        p.apply_async(long_time_task, args=(user,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()

