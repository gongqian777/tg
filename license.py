#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/7/16 14:41
# @Author  : Jerry
# @Site    : 
# @File    : license.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import Tkinter as Tk
import threading


def get_license(device_code, cpu_num='2', bandwidth='100'):
    print 'getting license.'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    b = webdriver.Chrome(chrome_options=options)
    # b = webdriver.Chrome()
    b.set_window_size(1280, 1024)
    wait = WebDriverWait(b, 10)
    try:
        b.get('http://10.10.6.216:8088/login')
        wait.until(lambda x: x.find_element_by_class_name("to_admin").is_displayed())
        b.find_element_by_class_name("to_admin").click()
        b.find_element_by_id('username').send_keys('xxxx')
        b.find_element_by_id('password').send_keys('xxxx')
        b.find_element_by_xpath('//*[@id="adminloginModal"]/div[2]/form/div/div[2]/div[3]/button').click()
        try:
            wait.until(lambda x: x.find_element_by_class_name('pagination-info').is_displayed())
        except TimeoutException:
            pass
        while b.find_element_by_class_name('page-list').is_displayed():
            pageinfo = b.find_element_by_class_name('pagination-info').text
            b.find_element_by_name("btSelectAll").click()
            b.find_element_by_id('btn_delete').click()
            al = b.switch_to.alert
            al.accept()
            wait.until(lambda x: x.find_element_by_class_name('pagination-info').text != pageinfo)
        while b.find_elements_by_xpath('//td[text()="%s"]' % device_code):
            """删除重复项"""
            time.sleep(1)
            e = b.find_element_by_xpath('//td[text()="%s"]/../td[1]/input' % device_code)
            ActionChains(b).move_to_element(e).perform()
            time.sleep(1)           # 等页脚消失
            e.click()
            e = b.find_element_by_xpath('/html/body/div[1]/div[1]/p')
            ActionChains(b).move_to_element(e).perform()
            b.find_element_by_id('btn_delete').click()
            al = b.switch_to.alert
            al.accept()
            time.sleep(1)
        pageinfo = b.find_element_by_class_name('pagination-info').text
        b.find_element_by_id('btn_add').click()
        wait.until(lambda x: x.find_element_by_id('myModalLabel').is_displayed())
        b.find_element_by_xpath('//button[@data-id="txt_project"]').click()
        b.find_element_by_xpath('//span[contains(text(), "流量安全网关")]').click()
        b.find_element_by_xpath('//button[@data-id="tg_cpu"]').click()
        b.find_element_by_xpath('//span[contains(text(), "%s CPU")]' % cpu_num).click()
        b.find_element_by_xpath('//button[@data-id="tg_band"]').click()
        b.find_element_by_xpath('//span[contains(text(), %s)]' % bandwidth).click()
        b.find_element_by_xpath('//button[@data-id="time_unit"]').click()
        b.find_element_by_xpath('//span[contains(text(), "月")]').click()
        b.find_element_by_xpath('//button[@data-id="time_value"]').click()
        b.find_element_by_xpath('//button[@data-id="time_value"]/../div/ul/li[@data-original-index="1"]').click()
        b.find_element_by_id('txt_mccode').send_keys(device_code)
        # b.find_element_by_id('txt_remark').send_keys('auto_script_added')
        b.find_element_by_id('btn_submit').click()
        wait.until(lambda x: x.find_element_by_class_name('pagination-info').text != pageinfo)
        while b.find_element_by_class_name('page-list').is_displayed():
            pageinfo = b.find_element_by_class_name('pagination-info').text
            b.find_element_by_name("btSelectAll").click()
            b.find_element_by_id('btn_delete').click()
            al = b.switch_to.alert
            al.accept()
            wait.until(lambda x: x.find_element_by_class_name('pagination-info').text != pageinfo)
        b.find_element_by_xpath('//td[text()="%s"]/../td[1]/input' % device_code).click()
        e = b.find_element_by_xpath('/html/body/div[1]/div[1]/p')
        ActionChains(b).move_to_element(e).perform()
        b.find_element_by_id('btn_gen').click()
        wait.until(lambda x: x.find_element_by_xpath('//td[text()="%s"]/../td[9]' % device_code).text == 'yes')
        license_code = b.find_element_by_xpath('//td[text()="%s"]/../td[7]' % device_code).text
        return license_code
    finally:
        time.sleep(5)
        b.quit()


def button_get_license():
    global tk_license_code
    device_code = t1.get(1.0, '1.end')
    license_code = get_license(device_code)
    t2.delete(1.0, Tk.END)
    t2.insert('end', license_code)


def button_clear_text():
    t1.delete(1.0, Tk.END)
    t2.delete(1.0, Tk.END)

window = Tk.Tk()
window.title('License Generator')
window.geometry('400x200')

l = Tk.Label(window, text='GET 2C,100M,1month license')
l.pack()

t1 = Tk.Text(window, height=3)
t1.pack()

tk_license_code = Tk.StringVar()


def new_thread():
    t = threading.Thread(target=button_get_license)
    t.start()

b1 = Tk.Button(window, text='Generate', command=new_thread)
b1.pack()

t2 = Tk.Text(window, height=5)
t2.pack()

b2 = Tk.Button(window, text='Clear', command=button_clear_text)
b2.pack()


if __name__ == '__main__':
    lic = '11'
    r = get_license(lic)
    print r
    # window.mainloop()
