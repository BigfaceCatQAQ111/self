# -*- encoding=utf8 -*-
__author__ = "starkYang"
from airtest.core.api import *
from airtest.core.android.adb import *
from airtest.core.android.android import *

auto_setup(__file__)

PACKAGE = "com.tencent.af"
INSTALL_PATH = "/Users/starkYang/Desktop/Android_apk/test.apk"

 # 获得当前设备列表
adb = ADB()
devicesList = adb.devices()
devicesNum = len(devicesList) > 1
assert_equal(devicesNum,True,"设备连接数量至少为2")

 # 连接手机 默认连接方式
connect_device("android:///")
 # 指定设备号连接
connect_device("android:///" + devicesList[0][0])

android = Android()
 #判断手机上是否安装包
try:
    android.check_app(PACKAGE)
except AirtestError:
    # 安装应用,是否同意覆盖安装,默认否
    android.install_app(INSTALL_PATH,False)
    # 覆盖安装
     # android.install_app(INSTALL_PATH,True)

 # 清空包数据,有的手机可能没有权限
try:
 clear_app(PACKAGE)

except:
    # 卸载A   `1 uninstall(PACKAGE)
 # 安装应用
 install(INSTALL_PATH)

# 启动应用,可以带Acitvity,也可以不带
start_app(PACKAGE)
# 休眠两秒
sleep(2)
# 停止应用
stop_app(PACKAGE)

# 切换手机
connect_device("android:///" + devicesList[1][0])

clear_app(PACKAGE)
uninstall(PACKAGE)
install(INSTALL_PATH)

start_app(PACKAGE)
sleep(2)
stop_app(PACKAGE)