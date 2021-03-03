# -*- encoding=utf8 -*-
__author__ = "C"

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from time import sleep
from airtest.core.api import *
from airtest.core.android.adb import *

adb = ADB()
deviceList = adb.devices()
print(deviceList)

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
start_app('com.lc.oppo.store')
sleep(3)

# if poco("com.lc.oppo.store:id/tvLabel").get_text() != "工作台":
#                         poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.lc.oppo.store:id/bottomNav").offspring("com.lc.oppo.store:id/home").child("com.lc.oppo.store:id/icon").click()   
    
# poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.lc.oppo.store:id/rv").child("android.widget.FrameLayout")[5].child("com.lc.oppo.store:id/cl").click()
# poco("com.lc.oppo.store:id/tvWithdraw").click()
# poco("com.lc.oppo.store:id/etMoney").set_text('1')
# poco(text="1").swipe([-0.004, 0.0])
# poco("com.lc.oppo.store:id/tvWithdraw").click()
# poco(text="1").click()
# poco(text="1").click()
# poco("android:id/button2").click()
# poco("关闭").click()
# poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.tencent.mm:id/c6s").child("com.tencent.mm:id/dp5")[0].offspring("com.tencent.mm:id/b39").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("关闭")[0].child("android.view.ViewGroup").click()
# poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.tencent.mm:id/c6s").child("com.tencent.mm:id/dp5")[0].offspring("com.tencent.mm:id/b39").child("android.view.ViewGroup").click()
# poco("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[0].child("android.widget.RelativeLayout").child("android.widget.FrameLayout")[1].child("android.widget.RelativeLayout").child("android.widget.FrameLayout").offspring("com.tencent.mm:id/nf").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.TextView").click()
# poco(text="1").click()
# poco(text="1").click()
# poco(text="1").click()
# poco(text="1").click()
# result = poco("com.lc.oppo.store:id/tv3").get_text()
# time.sleep(1)
# assert_equal(result, "等待财务审核", "是否提现成功")
# poco("com.lc.oppo.store:id/tvKnow").click()
# stop_app('com.lc.oppo.store')
# 点击跳转订单列表页面
if poco(text="订单列表").exists():
    # poco(text="订单列表").click
    poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.lc.oppo.store:id/rv").child("android.widget.FrameLayout")[0].child("com.lc.oppo.store:id/cl").click()

# 判断跳转页面是否正确
# assert_equal(poco(name="com.lc.vivo.store:id/label").get_text(),"订单列表")


# 检查订单状态table是否正确
# poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.lc.vivo.store:id/tabLayout")

# poco(text="待付款").click()
# poco(text="全部").click()
# poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.lc.oppo.store:id/tabLayout").offspring("待出库").child("android.widget.TextView").click()
# poco("android.widget.FrameLayout").child('android.widget.LinearLayout').child('android.widget.FrameLayout').child("android.widget.LinearLayout").child('android.widget.Fr7ameLayout').child('android.view.ViewGroup').child('android.widget.HorizontalScrollView').child('android.widget.LinearLayout')

status_list = []
for table in poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.lc.oppo.store:id/tabLayout").child("android.widget.LinearLayout "):
    print(table)
    a = table.offspring("android.widget.LinearLayout").offspring("android.widget.TextView")
 #   if not a.exists():
 #       continue
    status = a.get_text()
    if not status in status_list:
        status_list.append(status)
        print(status)
        
print(status_list)



