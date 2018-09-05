#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/5/3 16:17
# @Author  : Jerry
# @Site    :
# @File    : tg_case.py
# @Software: PyCharm

import unittest
import nfc_northapi
import tg_utils
from constants import *
import ipaddress
import random


class TGCases(unittest.TestCase):
    """流量卫士测试用例"""
    api = nfc_northapi.NorthApi(USERNAME)
    if NEW_USER:
        api.user_del()
        api.user_add()
        api.service_add()
    url = api.get_jump_url()
    util = tg_utils.Utils(url)

    @classmethod
    def setUpClass(cls):
        try:
            cls.util.activate_tg()
            cls.util.login_tg()
            cls.util.mode2gw()
        except:
            cls.util.stop_test()
            raise

    @classmethod
    def tearDownClass(cls):
        # pass
        cls.util.stop_test()

    def setUp(self):
        self.util.b.refresh()
        pass

    def test_wan_addip(self):
        """WAN口增加配置"""
        rand_ip = self.util.gen_random_ip()
        rand_prefix = str(random.randint(8, 22))
        wan_int = ipaddress.IPv4Interface(unicode(rand_ip + '/' + rand_prefix))
        wan_net = ipaddress.IPv4Network(wan_int.network)
        wan_gw = str(wan_net[random.randint(1, wan_net.num_addresses - 2)])
        wan_mask = str(wan_net.netmask)
        # while wan_gw == wan_int.ip:           # filter int_ip
        #     wan_gw = wan_net[random.randint(1, wan_net.num_addresses-2)]
        result = self.util.wan_static_add_config(rand_ip, wan_mask, wan_gw, main_dns='8.8.8.8', backup_dns='221.6.4.66')
        self.assertTrue(result, msg='添加WAN口配置失败')

    def test_lan_addip(self):
        """LAN口增加配置"""
        rand_ip = self.util.gen_random_ip()
        rand_prefix = str(random.randint(8, 22))
        lan_int = ipaddress.IPv4Interface(unicode(rand_ip + '/' + rand_prefix))
        lan_net = ipaddress.IPv4Network(lan_int.network)
        lan_mask = str(lan_net.netmask)
        result = self.util.lan_add_config(rand_ip, lan_mask)
        self.assertTrue(result, msg='添加LAN口配置失败')

    def test_dnat_add_config(self):
        """DNAT增加配置"""
        protocol_list = ['TCP', 'UDP', 'TCP+UDP', 'IP', 'ICMP', 'GRE']
        protocol = protocol_list[random.randint(0, 5)]
        globalip = self.util.get_wan_ip()
        localip = self.util.gen_random_ip()
        localport = str(random.randint(0, 65535))
        globalport = str(random.randint(0, 65535))
        remarks = self.util.get_description()
        loopback = bool(random.randint(0, 1))
        if protocol == 'TCP' or protocol == 'UDP' or protocol == 'TCP+UDP':
            result = self.util.dnat_add_config(protocol, globalip, localip, globalport, localport, remarks, loopback)
            self.assertTrue(result, msg='添加DNAT配置失败')
        else:
            result = self.util.dnat_add_config(protocol, globalip, localip, remarks=remarks, loopback=loopback)
            self.assertTrue(result, msg='添加DNAT配置失败')

    def test_snat_add_config(self):
        """SNAT增加配置"""
        protocol_list = ['TCP', 'UDP', 'TCP+UDP', 'IP', 'ICMP', 'GRE']
        protocol = protocol_list[random.randint(0, 5)]
        globalip = self.util.get_wan_ip()
        localip = self.util.gen_random_ip()
        rand_prefix = str(random.randint(8, 22))
        local_net = ipaddress.IPv4Network(unicode(globalip+'/'+rand_prefix), False)
        netmask = str(local_net.netmask)
        remarks = self.util.get_description()
        pat = bool(random.randint(0, 1))
        result = self.util.snat_add_config(protocol, localip, netmask, globalip, remarks, pat)
        self.assertTrue(result, msg='添加SNAT配置失败')

    def test_pool_add_config(self):
        """地址池增加地址"""
        wan_ip = self.util.get_wan_ip()
        pool_ip = str(ipaddress.IPv4Address(unicode(wan_ip))+1)
        name = self.util.get_description()
        result = self.util.pool_add_config(pool_ip, name=name)
        self.assertTrue(result, msg='地址池添加IP失败')

    def test_route_add_config(self):
        """路由增加地址"""
        wan_ip = self.util.get_wan_ip()
        rand_ip = self.util.gen_random_ip()
        rand_prefix = str(random.randint(8, 22))
        ran_int = ipaddress.IPv4Interface(unicode(rand_ip + '/' + rand_prefix))
        ran_net = ipaddress.IPv4Network(ran_int.network)
        ran_mask = str(ran_net.netmask)
        remarks = self.util.get_description()
        state = bool(random.randint(0, 1))
        result = self.util.route_add_config(rand_ip, ran_mask, wan_ip, remarks=remarks, state=state)
        self.assertTrue(result, msg='路由添加失败')

    def test_virus_url(self):
        """测试病毒URL拦截"""
        with open(VIRUS_URL, 'r') as f:
            txt = f.read()
            urls = txt.split('\n')
        random_urls = random.sample(urls, 5)
        print 'tested virus_url:'
        for url in random_urls:
            print '\t' + url
        failed_urls = self.util.url_block_test(random_urls)
        self.assertFalse(failed_urls, msg='病毒失败地址：'+str(failed_urls))

    def test_fraud_url(self):
        """测试欺诈URL拦截"""
        with open(FRAUD_URL, 'r') as f:
            txt = f.read()
            urls = txt.split('\n')
        random_urls = random.sample(urls, 5)
        print 'tested fraud_url:'
        for url in random_urls:
            print '\t' + url
        failed_urls = self.util.url_block_test(random_urls)
        self.assertFalse(failed_urls, msg='欺诈失败地址：'+str(failed_urls))

    def test_update_urldb_online(self):
        """测试在线更新恶意网址库"""
        result = self.util.urldb_update_online()
        self.assertTrue(result[0], msg=result[1])

    def test_update_urldb_offline(self):
        """测试本地更新恶意网址库，结果不好判断，暂时不测"""
        result = self.util.urldb_update_offline()
        self.assertTrue(result[0], msg=result[1])

    def test_manager_add(self):
        """新增管理员"""
        name = 'abc'
        password = password_c = '123.com'
        mgr_type = random.randint(0, 1)
        phone = '13123456789'
        remarks = self.util.get_description()
        result = self.util.mgr_add(name, password, password_c, mgr_type, phone, remarks)
        self.assertTrue(result[0], msg=result[1])
