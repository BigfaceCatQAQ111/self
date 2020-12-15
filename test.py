# -*- encoding=utf8 -*-
__author__ = "wxy"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# if not cli_setup():
#     auto_setup(__file__, logdir=True, devices=[
#         "android://127.0.0.1:5037/HJS0219115000550?cap_method=MINICAP_STREAM&&ori_method=MINICAPORI&&touch_method=MINITOUCH",
#     ])

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

poco(text="彩创门店端").click()
sleep(1)
if poco("com.lc.cc.store:id/button").exists():
    poco("com.lc.cc.store:id/phone").set_text("18208772700")
    poco("com.lc.cc.store:id/next").click()
    sleep(1)
    # 获取设备的高度和宽度
    width, height = device().get_current_resolution()
    # 校准滑动的起点和终点
    start_pt = [width * 0.5, height / 20]
    end_pt = [width * 0.5, height]
    # 滑动
    swipe(start_pt, end_pt)
    sleep(6)
    poco(text="复制验证码").click()
    # 长按显示粘贴按钮
    # poco(text="输入手机验证码").swipe([0,0],duration=2)
    poco(text="输入手机验证码").long_click(duration=2)
    sleep(2)
    touch(Template(r"/tpl1607931343927.png", record_pos=(-0.301, -0.501), resolution=(1080, 2244)))
    poco("com.lc.cc.store:id/next").click()

if poco("com.lc.cc.store:id/tvSysTitle").exists():
    poco("com.lc.cc.store:id/storeName").click()

if poco("com.lc.cc.store:id/tvLabel").exists():
    poco(text="商品管理").click()
    sleep(1)
    poco("com.lc.cc.store:id/item2Tips").click()
    poco("com.lc.cc.store:id/item2Tips").click()
    # 如果没有找到该产品名称就会一直向下滑动
    while not poco(text="多功能快充折叠充电宝").exists():
        poco.scroll(direction='vertical', percent=0.4, duration=1)
    poco(text="多功能快充折叠充电宝").click()
    sleep(1)
    poco("com.lc.cc.store:id/tvSubtitleTitle").click()
    sleep(1)
    poco("com.lc.cc.store:id/shareWX").click()
    poco(text="文件传输助手").click()
    sleep(1)
    poco("com.tencent.mm:id/doz").click()
    sleep(1)
    poco("com.tencent.mm:id/dom").click()
    sleep(1)
    poco("转到上一层级").click()
    sleep(1)
    poco("com.lc.cc.store:id/ivSysBack").click()
    sleep(1)
    poco("com.lc.cc.store:id/ivBack").click()
    sleep(1)
    poco("android.widget.LinearLayout").offspring("android:id/content").offspring(
        "com.lc.cc.store:id/bottomNav").offspring("com.lc.cc.store:id/store").child("com.lc.cc.store:id/icon").click()
    sleep(1)
    poco("android.widget.LinearLayout").offspring("android:id/content").offspring("android.view.ViewGroup").offspring(
        "com.lc.cc.store:id/setting").child("android.widget.ImageView").click()
    poco("com.lc.cc.store:id/logout").click()
    poco("com.lc.cc.store:id/sure").click()
    poco("com.lc.cc.store:id/sms").click()
    home()
