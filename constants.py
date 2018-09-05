# coding: utf-8

# DEVICE='22'                                                     #运行脚本的设备名，不同设备须使用不同的名称
# WEB_URL='https://10.10.2.172:8383/NFCv1.0'                      #NFC web的url
# GC_SERVER='10.10.2.172'                                         #总控地址
# DESC_PATH='D:/auto/book.txt'                                    #租户、开发者描述从该文件中读取
# RESULT_PATH="D:/auto/result/"                                   #测试结果保存的目录
# TGW_LIST=['nanjing','shanghai']                                 #选择在哪些接入点下添加vpn
# REGION_LIST=['nanjing','shanghai']                              #租户页面提交添加服务链时默认从这里随机挑一个接入点
# APP_NAME='NFC-DNS'                                              #服务链要添加的应用名称
# CLOUD_NETWORK='shanghai_cloud'                                  #在指定云网络创建云主机，如果不填，随机从所有云网络中选一个
# HOST_APP_NAME='NFC-WAF'                                         #指定云主机名称
# CASSANDRA_SERVER='10.10.2.11'                                   #cassandra地址
# ADMIN_USRENAME='nfc_api'
# ADMIN_PASSWORD='nfc_api'
#
# #开发者提交应用申请
# APP_ICO_PATH_DEVELOPER = 'D:\\auto\\file\\icon\\1.png'         # 开发者提交应用申请时填写的应用模版图标路径
# APP_TEMPLATE_FILE_PATH = 'D:\\auto\\file\\NFCv1.0.zip'         # 开发者提交应用申请时填写的文件路径
# APP_TEMPLATE_IMAG_PATH = 'D:\\auto\\file\\icon\\null.png'      # 开发者提交应用申请时上传的截600*400图路径
#
#
# #应用模版配置
# APP_ICO_PATH=u'D:/auto/file/icon/1.png'                          #应用模版图标路径
# APP_TEMPLATE_NAME=u'webdriver_测试'                             #应用模版名称
# HAS_WEB=1                                                       #是否有web，0表示没有，1表示有
# PRICE_FLOW=100                                                  #按量价格
# PRICE_PACKAGE=200                                               #包月价格
# WEB_SERVICE='file:///home/AppWebservice.wsdl'                   #WEB服务地址
# APP_TYPE='监控类'                                               #应用类型
# IMAGE='ips-3.1.20-LTS-T33'                                      #应用模版绑定的镜像名称
# MASTER_TYPE=[2,3,4]                                             #资源模板序号
# TEMPLATE_TYPE=random.choice([[1],[2],[3],[1,2]])                #模板类型序号
#
# #镜像配置
# DUMP_URL='http://10.10.2.187:8383/NSUM/login/innerLogin.do'     #跳转地址，可以不填
# IMAGE_NAME='NFC-IPS_webtests'                                   #镜像名称
# IMAGE_TYPE='kvm'                                                #镜像类型
# PROTOCOL_TYPE='http'                                            #镜像协议类型
# MIRROR_URL='http://10.10.3.100/image/rules.rar'                 #镜像地址URL

GC_SERVER = '10.10.2.187'
NORTH_PORT = '8385'
USERNAME = 'autotest'
NEW_USER = 0
RESULT_PATH = "D:/auto/result/"                                   #测试结果保存的目录
DESC_FILE = 'D:/auto/book.txt'
VIRUS_URL = 'D:/auto/bingdu.txt'
FRAUD_URL = 'D:/auto/qizha.txt'
