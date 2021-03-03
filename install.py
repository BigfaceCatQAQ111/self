# -*- encoding=utf8 -*-

from airtest.core.api import *
from airtest.core.android.adb import *
from airtest.core.android.android import *
import os

auto_setup(__file__)
PACKAGE = 'com.cc.pd'
path = os.path.join(os.getcwd(), "apk")
INSTALL_PATH = path + r"/" + (os.listdir(path))[0]


class InstallApp(object):

    def install_app(self,devices):

        for dev in devices:
            # 指定设备号连接
            connect_device("android:///" + dev)
        android = Android()
            #判断手机上是否安装包
        a = android.list_app()
        try:
            android.check_app(PACKAGE)
        except AirtestError:
            # 安装应用,是否同意覆盖安装,默认否
            android.install_app(INSTALL_PATH,False)
            # 覆盖安装
            # android.install_app(INSTALL_PATH,True)
        # 清空包数据,有的手可能没有权限
        # try:
        #     clear_app(PACKAGE)
        # except:
        #     # 安装应用
        #     install(INSTALL_PATH)


if __name__ == "__main__":
    print("hello world!")
