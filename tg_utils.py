#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/5/4 14:11
# @Author  : Jerry
# @Site    : 
# @File    : tg_utils.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from requests import ConnectionError, ReadTimeout
from constants import *
import time
import requests
from nfc_northapi import NorthApi
import os
import random
import codecs
from license import get_license


class Utils(object):
    def __init__(self, url=None):
        self.url_login = url
        self.b = webdriver.Chrome()
        self.b.maximize_window()
        self.b.implicitly_wait(5)
        self.wait = WebDriverWait(self.b, 10)
        # self.b.set_window_size(1280, 1024)

    @staticmethod
    def gen_random_ip():
        first_ip = random.randint(1, 223)
        while first_ip == 127:
            first_ip = random.randint(1, 223)
        rand_ip = str(first_ip) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
            random.randint(0, 255))
        return rand_ip

    @staticmethod
    def get_description():
        """随机从文件读取30-60个字节"""
        f = codecs.open(DESC_FILE, "r", "utf-8")
        fsize = os.path.getsize(DESC_FILE)
        offset = random.randint(0, fsize)
        f.seek(offset)
        size = random.randint(30, 60)
        while 1:
            try:
                return f.read(size)
            except UnicodeDecodeError:          # 遇到非UTF8边界时，重新读取
                pass

    @staticmethod
    def url_block_test(urls):
        """返回能打开的URL"""
        failed_urls = []
        for url in urls:
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    if u'存在未经证实信息的网站' in r.text or u'http://go.microsoft.com/fwlink' in r.text:
                        pass
                    else:
                        failed_urls.append(url)
            except (ConnectionError, ReadTimeout):      # 连接失败/超时，则打开失败，认为成功
                pass
        return failed_urls

    def get_wan_ip(self):
        self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
        self.b.find_element_by_id("device").click()
        wan_ip = self.b.find_element_by_id('port_wanIP').text
        return wan_ip

    def get_lan_ip(self):
        self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
        self.b.find_element_by_id("device").click()
        lan_ip = self.b.find_element_by_id('port_lanIP').text
        return lan_ip

    def activate_tg(self):
        self.b.get(self.url_login)
        time.sleep(1)
        if self.b.title != u'login':
            WebDriverWait(self.b, 5, 0.5).until(lambda b: b.find_element_by_id("licenseState").is_displayed())
            self.b.find_element_by_id('machineCode').click()
            device_code = self.b.find_element_by_class_name('layui-layer-content').text
            license = get_license(device_code)
            self.b.find_element_by_class_name('layui-layer-btn0').click()
            self.b.find_element_by_id('licenseCode').send_keys(license)
            self.b.find_element_by_id('licenseClick').click()
            WebDriverWait(self.b, 5, 0.5).until(lambda b:
                                                b.find_element_by_class_name("layui-layer-title").is_displayed())
            self.b.find_element_by_class_name('layui-layer-btn0').click()

    def login_tg(self, username='telecomadmin', password='xxxx'):
        """登录流量卫士方法，无license则激活后登录"""
        self.b.get(self.url_login)
        if self.b.title == u'login':
            try:
                self.wait.until(lambda b: b.find_element_by_id("login").is_displayed())
                time.sleep(0.5)
                self.b.find_element_by_id("name").send_keys(username)
                self.b.find_element_by_id("password").send_keys(password)
                self.b.find_element_by_id('verificationCode').send_keys('aaaa')
                self.b.find_element_by_id('login').click()
            except:
                raise
        else:
            print 'current page is not login page?'

    def mode2gw(self):
        try:
            self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
            self.b.find_element_by_id("device").click()
            self.wait.until(lambda b: b.find_element_by_id("changeModel").is_displayed())
            mode = self.b.find_element_by_class_name('now_select').text
            if mode == u'网关模式':
                time.sleep(15)          # 等待底层加载license完毕
                self.b.find_element_by_class_name('now_select').click()
                self.wait.until(lambda b: b.find_element_by_xpath(
                    '//*[@class="popBox"]/div[3]/div[1]/a').is_displayed())
                self.b.find_element_by_xpath('//*[@class="popBox"]/div[3]/div[1]/a').click()
                time.sleep(30)
                while 1:
                    try:
                        self.login_tg()
                        WebDriverWait(self.b, 30, 0.5).until(lambda b: b.find_element_by_id("device"))
                        break
                    except TimeoutException:
                        time.sleep(1)
                return True
        except:
            raise

    def stop_test(self):
        self.b.quit()

    def _wan_switch_type(self, value):
        """切换WAN口模式，value=static|pppoe|dynamic"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
            self.b.find_element_by_id("device").click()
            # self.wait.until(lambda b: b.find_element_by_xpath(
            #     '//*[@id="accordion"]/li[2]/div').is_displayed())
            # self.b.find_element_by_xpath('//*[@id="accordion"]/li[2]/div').click()
            # self.b.find_element_by_link_text(u'WAN口设置').click()
            navi1 = '//span[text()="接口设置"]'
            navi2 = '//span[text()="WAN口设置"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi1).is_displayed())
            self.b.find_element_by_xpath(navi1).click()
            self.wait.until(lambda b: b.find_element_by_xpath(navi2).is_displayed())
            self.b.find_element_by_xpath(navi2).click()
            time.sleep(2)
            e = self.b.find_element_by_id(value)
            if e.get_attribute('style') == 'display: none;':
                select = self.b.find_element_by_name('wan_type')
                select.find_element_by_xpath('//option[@value="'+value+'"]').click()
            time.sleep(1)
            if not e.get_attribute('style'):
                return True
            else:
                self.b.get_screenshot_as_file(RESULT_PATH + 'switch_wan_type_failed' + '.jpg')
                return False
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'switch_wan_type_failed' + '.jpg')
            raise

    def wan_static_add_config(self, ip, mask, gw, mtu=1500, main_dns=None, backup_dns=None):
        """配置WAN口静态配置"""
        try:
            assert self._wan_switch_type('static')
            e = self.b.find_element_by_name('static_main_ip')
            e.clear()
            e.send_keys(ip)
            e = self.b.find_element_by_name('static_mask')
            e.clear()
            e.send_keys(mask)
            e = self.b.find_element_by_name('static_gateway')
            e.clear()
            e.send_keys(gw)
            e = self.b.find_element_by_name('static_mtu')
            e.clear()
            e.send_keys(mtu)
            if main_dns:
                e = self.b.find_element_by_name('static_main_dns')
                e.clear()
                e.send_keys(main_dns)
            if backup_dns:
                e = self.b.find_element_by_name('static_backup_dns')
                e.clear()
                e.send_keys(backup_dns)
            self.b.find_element_by_id('static_sub').click()
            self.wait.until(lambda b: b.find_element_by_class_name("popBox").is_displayed())
            if self.b.find_element_by_xpath('//*[@class="popBox"]/div[2]/p').text == u'操作成功':
                self.b.find_element_by_xpath('//*[@class="popBox"]/div[3]/div[1]/a').click()
                time.sleep(3)
                return True
            else:
                self.b.get_screenshot_as_file(RESULT_PATH + 'add_wan_failed' + '.jpg')
                return False
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'add_wan_failed' + '.jpg')
            raise

    def lan_add_config(self, ip, mask):
        """配置LAN口"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
            self.b.find_element_by_id("device").click()
            navi1 = '//span[text()="接口设置"]'
            navi2 = '//span[text()="LAN口设置"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi1).is_displayed())
            self.b.find_element_by_xpath(navi1).click()
            self.wait.until(lambda b: b.find_element_by_xpath(navi2).is_displayed())
            self.b.find_element_by_xpath(navi2).click()
            e = self.b.find_element_by_id('IP')
            e.clear()
            e.send_keys(ip)
            e = self.b.find_element_by_id('subnetMask')
            e.clear()
            e.send_keys(mask)
            self.b.find_element_by_id('save').click()
            self.wait.until(lambda b: b.find_element_by_class_name("popBox").is_displayed())
            if self.b.find_element_by_xpath('//*[@class="popBox"]/div[2]/p').text == u'保存成功':
                self.b.find_element_by_xpath('//*[@class="popBox"]/div[3]/div[1]/a').click()
                return True
            else:
                self.b.get_screenshot_as_file(RESULT_PATH + 'add_lan_conf_failed' + '.jpg')
                return False
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'add_lan_conf_failed' + '.jpg')
            raise

    def route_add_config(self, dip, mask, nexthop, remarks=None, state=True):
        """增加路由"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
            self.b.find_element_by_id("device").click()
            navi1 = '//span[text()="路由功能"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi1).is_displayed())
            self.b.find_element_by_xpath(navi1).click()
            self.wait.until(lambda b: b.find_element_by_xpath(
                "//a[text()='添加新条目']").is_displayed())
            self.b.find_element_by_id('addNew').click()
            self.b.find_element_by_id('destinationNat').send_keys(dip)
            self.b.find_element_by_id('subnetMask').send_keys(mask)
            self.b.find_element_by_id('defaultGateway').send_keys(nexthop)
            select = self.b.find_element_by_id('status')
            if not state:
                select.find_element_by_xpath('//option[@value="0"]').click()
            if remarks:
                self.b.find_element_by_id('remarks').send_keys(remarks)
            self.b.find_element_by_id('addRoute').click()
            if self.b.find_element_by_xpath('//*[@class="popBox"]/div[2]/p').text == u'操作成功':
                self.b.find_element_by_xpath('//*[@class="popBox"]/div[3]/div[1]/a').click()
                return True
            else:
                self.b.get_screenshot_as_file(RESULT_PATH + 'add_route_failed' + '.jpg')
                return False
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'add_route_failed' + '.jpg')
            raise

    def dnat_add_config(self, protocol, globalip, localip, globalport='0', localport='0', remarks=None, loopback=True):
        """配置DNAT，protocol=TCP|UDP|IP|ICMP|TCP+UDP|GRE"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
            self.b.find_element_by_id("device").click()
            navi1 = '//span[text()="转发配置"]'
            navi2 = '//span[text()="目的NAT"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi1).is_displayed())
            self.b.find_element_by_xpath(navi1).click()
            self.wait.until(lambda b: b.find_element_by_xpath(navi2).is_displayed())
            self.b.find_element_by_xpath(navi2).click()
            self.wait.until(lambda b: b.find_element_by_xpath(
                "//a[text()='添加']").is_displayed())
            self.b.find_element_by_xpath("//a[text()='添加']").click()
            select = self.b.find_element_by_name('protocol')
            select.find_element_by_xpath('//option[@value="'+protocol+'"]').click()
            select = self.b.find_element_by_name('globalip')
            select.find_element_by_xpath('//option[@value="'+globalip+'"]').click()
            self.b.find_element_by_name('localip').send_keys(localip)
            if protocol == 'IP' or protocol == 'ICMP' or protocol == 'GRE':
                pass
            else:
                self.b.find_element_by_name('globalport').send_keys(globalport)
                self.b.find_element_by_name('localport').send_keys(localport)
            if remarks:
                self.b.find_element_by_name('remarks').send_keys(remarks)
            if not loopback:
                self.b.find_element_by_xpath("//input[@value='0']").click()
            self.b.find_element_by_xpath("//a[text()='确认']").click()
            try:
                WebDriverWait(self.b, 1, 0.5).until(lambda b: b.find_element_by_class_name('popBox'))
            except TimeoutException:
                return True             # 没有弹窗则正常
            else:                       # 弹窗依然存在则异常
                self.b.get_screenshot_as_file(RESULT_PATH + 'add_dnat_failed' + '.jpg')
                return False
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'add_dnat_failed' + '.jpg')
            raise

    def snat_add_config(self, protocol, localip, netmask, globalip, remarks=None, pat=True):
        """配置DNAT，protocol=TCP|UDP|IP|ICMP|TCP+UDP|GRE"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
            self.b.find_element_by_id("device").click()
            navi1 = '//span[text()="转发配置"]'
            navi2 = '//span[text()="静态源NAT"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi1).is_displayed())
            self.b.find_element_by_xpath(navi1).click()
            self.wait.until(lambda b: b.find_element_by_xpath(navi2).is_displayed())
            self.b.find_element_by_xpath(navi2).click()
            self.wait.until(lambda b: b.find_element_by_xpath(
                "//a[text()='添加']").is_displayed())
            self.b.find_element_by_xpath("//a[text()='添加']").click()
            select = self.b.find_element_by_name('protocol')
            select.find_element_by_xpath('//option[@value="' + protocol + '"]').click()
            select = self.b.find_element_by_name('globalip')
            select.find_element_by_xpath('//option[@value="' + globalip + '"]').click()
            self.b.find_element_by_name('localip').send_keys(localip)
            self.b.find_element_by_name('netmask').send_keys(netmask)
            if remarks:
                self.b.find_element_by_name('remarks').send_keys(remarks)
            if not pat:
                self.b.find_element_by_xpath("//input[@value='0']").click()
            self.b.find_element_by_xpath("//a[text()='确认']").click()
            try:
                WebDriverWait(self.b, 1, 0.5).until(lambda b: b.find_element_by_class_name('popBox'))
            except TimeoutException:
                return True  # 没有弹窗则正常
            else:  # 弹窗依然存在则异常
                self.b.get_screenshot_as_file(RESULT_PATH + 'add_snat_failed' + '.jpg')
                return False
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'add_snat_failed' + '.jpg')
            raise

    def pool_add_config(self, startip, endip=None, name=None):
        """添加地址池地址"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("device").is_displayed())
            self.b.find_element_by_id("device").click()
            navi1 = '//span[text()="转发配置"]'
            navi2 = '//span[text()="地址池"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi1).is_displayed())
            self.b.find_element_by_xpath(navi1).click()
            self.wait.until(lambda b: b.find_element_by_xpath(navi2).is_displayed())
            self.b.find_element_by_xpath(navi2).click()
            self.wait.until(lambda b: b.find_element_by_xpath(
                "//a[text()='添加']").is_displayed())
            self.b.find_element_by_xpath("//a[text()='添加']").click()
            if endip:
                self.b.find_element_by_id('ip').send_keys(startip+'-'+endip)
            else:
                self.b.find_element_by_id('ip').send_keys(startip)
            if name:
                self.b.find_element_by_id('name').send_keys(name)
            self.b.find_element_by_xpath("//a[text()='确认']").click()
            try:
                WebDriverWait(self.b, 1, 0.5).until(lambda b: b.find_element_by_class_name('popBox'))
            except TimeoutException:
                return True  # 没有弹窗则正常
            else:  # 弹窗依然存在则异常
                self.b.get_screenshot_as_file(RESULT_PATH + 'add_poolip_failed' + '.jpg')
                return False
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'add_poolip_failed' + '.jpg')
            raise

    def urldb_update_online(self):
        """在线升级恶意网址库"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("sys_config").is_displayed())
            self.b.find_element_by_id("sys_config").click()
            navi = '//span[text()="系统升级"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi).is_displayed())
            self.b.find_element_by_xpath(navi).click()
            e = '//span[text()="立即在线升级"]'
            self.wait.until(lambda b: b.find_element_by_xpath(e).is_displayed())
            self.b.find_element_by_xpath(e).click()
            e = '/html/body/div[2]/p'
            self.wait.until(lambda b: b.find_element_by_xpath(e).is_displayed())
            pop_msg = self.b.find_element_by_xpath(e).text
            self.b.find_element_by_id("sys_config")
            if pop_msg == u'已经是最新版本无需升级！':
                self.b.refresh()
                return True, pop_msg
            else:
                self.b.get_screenshot_as_file(RESULT_PATH + 'urldb_online_update_failed' + '.jpg')
                self.b.refresh()
                return False, pop_msg
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'urldb_online_update_failed' + '.jpg')
            raise

    def urldb_update_offline(self):
        """离线升级恶意网址库"""
        try:
            self.b.refresh()
            self.wait.until(lambda b: b.find_element_by_id("sys_config").is_displayed())
            self.b.find_element_by_id("sys_config").click()
            navi = '//span[text()="系统升级"]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi).is_displayed())
            self.b.find_element_by_xpath(navi).click()
            e = '//span[text()="本地升级"]'
            self.wait.until(lambda b: b.find_element_by_xpath(e).is_displayed())
            self.b.find_element_by_name('file').send_keys(r'D:\auto\url-package-1.0.0.bin')
            time.sleep(1)
            self.wait.until(lambda b: b.find_element_by_xpath(e).is_displayed())
            self.b.find_element_by_xpath(e).click()
            e = '/html/body/div[2]/p'
            WebDriverWait(self.b, 10, 0.01).until(lambda b: b.find_element_by_xpath(e).is_displayed())
            pop_msg = self.b.find_element_by_xpath(e).text
            if pop_msg == u'本地升级成功！':
                return True, pop_msg
            else:
                self.b.get_screenshot_as_file(RESULT_PATH + 'urldb_offline_update_failed' + '.jpg')
                return False, pop_msg
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'urldb_online_update_failed' + '.jpg')
            raise

    def mgr_add(self, name, password, password_c, mgr_type, phone, remarks=None):
        """增加管理员"""
        try:
            self.wait.until(lambda b: b.find_element_by_id("sys_config").is_displayed())
            self.b.find_element_by_id("sys_config").click()
            navi = '//*[@id="menu"]/div/ul[4]/li/span[2]'
            self.wait.until(lambda b: b.find_element_by_xpath(navi).is_displayed())
            self.b.find_element_by_xpath(navi).click()
            e = '//span[text()="添加"]'
            self.wait.until(lambda b: b.find_element_by_xpath(e).is_displayed())
            time.sleep(1)
            self.b.find_element_by_xpath(e).click()
            self.b.find_element_by_xpath('//*[@id="admin_form"]/div[1]/div/div/input').send_keys(name)
            self.b.find_element_by_xpath('//*[@id="admin_form"]/div[2]/div/div/input').send_keys(password)
            self.b.find_element_by_xpath('//*[@id="admin_form"]/div[3]/div/div/input').send_keys(password_c)
            self.b.find_element_by_xpath('//*[@id="admin_form"]/div[4]/div/div/div/input').click()
            if mgr_type == 1:
                e = '//span[text()="电信管理员"]'
                self.wait.until(lambda b: b.find_element_by_xpath(e).is_displayed())
                self.b.find_element_by_xpath(e).click()
            else:
                e = '//span[text()="电信管理员"]'
                self.wait.until(lambda b: b.find_element_by_xpath(e).is_displayed())
                self.b.find_element_by_xpath(e).click()
            self.b.find_element_by_xpath('//*[@id="admin_form"]/div[5]/div/div/input').send_keys(phone)
            if remarks:
                self.b.find_element_by_xpath('//*[@id="admin_form"]/div[6]/div/div/input').send_keys(remarks)
            self.b.find_element_by_xpath('//*[@id="secondlayer"]/div[1]/div/div[3]/div/div[3]/div/button').click()
            pop_msg = self.b.find_element_by_xpath('/html/body/div[4]/p').text
            if pop_msg == u'添加用户成功！':
                return True, pop_msg
            else:
                self.b.get_screenshot_as_file(RESULT_PATH + 'mgr_add_failed' + '.jpg')
                return False, pop_msg
        except:
            self.b.get_screenshot_as_file(RESULT_PATH + 'mgr_add_failed' + '.jpg')
            raise

if __name__ == '__main__':
    testtenant = 'ggg'
    c = NorthApi(testtenant)
    testurl = c.get_jump_url()
    self = Utils(testurl)
    try:
        self.login_tg()
        self.mode2gw()
    except:
        self.stop_test()
        raise
    #
    # protocol = 'TCP'
    # globalip = self.get_wan_ip()
    #
    # for i in range(56, 100):
    #     globalport = str(i+101)
    #     localip = self.gen_random_ip()
    #     localport = str(random.randint(0, 65535))
    #     remarks = self.get_description()+unicode(i)
    #     loopback = bool(random.randint(0, 1))
    #     try:
    #         self.dnat_add_config(protocol, globalip, localip, globalport, localport, remarks=remarks, loopback=loopback)
    #     except Exception:
    #         raise
    wan = self.get_wan_ip()
    for i in range(1, 6):
        # rand_ip = self.gen_random_ip()
        rand = '1.1.1.' + str(i)
        ran_mask = '255.255.255.255'
        # state = bool(random.randint(0, 1))
        sta = False
        remark = self.get_description()
        result = self.route_add_config(rand, ran_mask, wan, remarks=remark, state=sta)
    self.stop_test()
