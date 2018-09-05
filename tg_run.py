#coding:utf-8

from HTMLTestRunner import HTMLTestRunner
import unittest
import time
import os
import constants
from tg_case import TGCases
import sys


reload(sys)
sys.setdefaultencoding('utf8')


now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
report_path = constants.RESULT_PATH + '/'
if not os.path.exists(report_path):
    os.makedirs(report_path)
filename = report_path + now + '.html'
f = file(filename, 'wb')
runner = HTMLTestRunner(stream=f, title=u'TG测试报告', description=u'用例执行情况：')


tgsuite = unittest.TestSuite()
tgsuite.addTest(TGCases('test_wan_addip'))
tgsuite.addTest(TGCases('test_lan_addip'))
tgsuite.addTest(TGCases('test_route_add_config'))
tgsuite.addTest(TGCases('test_dnat_add_config'))
tgsuite.addTest(TGCases('test_snat_add_config'))
tgsuite.addTest(TGCases('test_pool_add_config'))
tgsuite.addTest(TGCases('test_update_urldb_online'))
tgsuite.addTest(TGCases('test_manager_add'))
tgsuite.addTest(TGCases('test_virus_url'))
tgsuite.addTest(TGCases('test_fraud_url'))


if __name__ == '__main__':
    r = runner.run(tgsuite)
    result_list = str(r).split(' ')
    errors = result_list[2].split('=')[1]
    failures = result_list[3].split('=')[1][0:-1]
    if int(errors) or int(failures):
        os.system(r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" ' + filename)