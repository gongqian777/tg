#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/5/3 17:49
# @Author  : Jerry
# @Site    : 
# @File    : nfc_northapi.py
# @Software: PyCharm

from constants import *
import requests
import json
import time
from novaclient import client


class NorthApi(object):
    def __init__(self, company_id):
        self.company_id = company_id
        self.base_url = 'http://' + GC_SERVER + ':' + NORTH_PORT + '/NfcApiRest/'
        self.project_url = self.base_url+'project'
        self.net_url = self.base_url + 'netfunction'
        self.token_url = self.base_url + 'authToken'
        self.headers = {'content-type': 'application/json'}
        self.timeout = 10

    def user_add(self):
        body = '{"company_id":"' + self.company_id + '"}'
        r = requests.post(url=self.project_url, headers=self.headers, data=body, timeout=self.timeout)
        status = r.json()['status']
        if not status:
            print 'Create user "%s" FAILED, reason: "%s"' % (self.company_id, status)
            return False
        else:
            print 'Create user "%s" SUCCESS' % self.company_id
            return True

    def user_del(self):
        params = {'company_id': self.company_id}
        r = requests.delete(url=self.project_url, headers=self.headers, params=params, timeout=self.timeout)
        status = r.json()['status']
        if not status:
            reason = r.json()['reason']
            print 'Delete user "%s" FAILED, reason: "%s"' % (self.company_id, reason)
            return False
        else:
            print 'Delete user "%s" SUCCESS' % self.company_id
            return True

    def service_add(self, bandwidth=None):
        print 'Creating TG for "%s"' % self.company_id
        if not bandwidth:
            bandwidth = 100
        body = r'{"company_id":"' + self.company_id + '","bandwidth":' + str(bandwidth) + "}'"
        r = requests.post(url=self.net_url, headers=self.headers, data=body, timeout=90)
        status = r.json()['status']
        if not status:
            print 'Create service for "%s" FAILED, reason: "%s"' % (self.company_id, status)
            return False
        else:
            print 'Create service for "%s" SUCCESS' % self.company_id
            time.sleep(10)
            return True

    def service_del(self):
        params = {'company_id': self.company_id}
        r = requests.delete(url=self.net_url, headers=self.headers, params=params, timeout=self.timeout)
        status = r.json()['status']
        if not status:
            print 'Delete service for "%s" FAILED, reason: "%s"' % (self.company_id, status)
            return False
        else:
            print 'Delete service for "%s" SUCCESS' % self.company_id
            return True

    def get_api_jump_url(self, tg_admin=None):
        """获取北向接口租户的跳转地址"""
        params = {'company_id': self.company_id}
        r_url = requests.get(self.net_url, headers=self.headers, params=params)
        status = r_url.json()['status']
        if not status:
            print self.company_id, 'has no instance'
            return False
        url = r_url.json()['net_url']
        r_token = requests.get(self.token_url, headers=self.headers, params=params)
        token = r_token.json()['nfc_token']
        jump_addr = url+'?nfc_token='+token
        if tg_admin:
            jump_addr += '&nfc_u=telecomadmin'
        print self.company_id+':', jump_addr
        return jump_addr

    def get_jump_url(self, gc=GC_SERVER, region=None, tg_admin=None):
        """获取任何类型租户的跳转地址，只获取第一个"""
        url_keystone = 'http://' + gc + ':5000/v2.0/'
        url_proxy = 'http://' + gc + ':9999/'
        url_token = url_proxy + 'token'
        headers = {'content-type': 'application/json'}
        r_token = requests.post(url_token, headers=headers,
                                data=json.dumps({'userName': self.company_id, 'password': '123@abc!'}))
        if r_token.status_code != 200:
            print 'get jump url for "%s" failed, reason: "%s"' % (self.company_id, r_token.text)
            return False
        token = r_token.json()['token']
        nc = client.Client('2', 'admin', 'admin', self.company_id, auth_url=url_keystone, region_name=region)
        # servers = nc.servers.list()
        # addr_list = []
        # for server in servers:
        #     vmname = server.to_dict()['metadata']['VMName']
        #     url_proxy_config = url_proxy + VMName
        #     r = requests.get(url_proxy_config)
        #     url = r.json()['externalProxyURL']
        #     jump_addr = url + '?nfc_token=' + token
        #     addr_list.append(jump_addr)
        # return addr_list
        serverlist = nc.servers.list()
        if serverlist:
            server = serverlist[0]          # only get first server
            vmname = server.to_dict()['metadata']['VMName']
            url_proxy_config = url_proxy + vmname
            r_url = requests.get(url_proxy_config)
            url = r_url.json()['externalProxyURL']
            jump_addr = url + '?nfc_token=' + token
            if tg_admin:
                jump_addr += '&nfc_u=telecomadmin'
            print self.company_id+':', jump_addr
            return jump_addr
        else:
            print 'tenant "%s" has no instance.' % self.company_id


if __name__ == '__main__':
    tenant = 'auto2222'
    c = NorthApi(tenant)
    c.user_del()
    # c.user_add()
    # c.service_add()
    # addr = c.get_jump_url()
