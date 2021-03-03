# -*- encoding=utf8 -*-
__author__ = "C"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

start_app("com.tencent.mm")
poco("com.tencent.mm:id/czk").swipe([-0.0076, 0.5723])


poco(text="彩创科技").click()
sleep(5)
poco(text="新品热卖").click()
while not poco(text="佳琦推荐 欧伊俪珍珠纹洗脸巾").exists():
    poco.scroll(direction='vertical', percent=0.3, duration=1.0)
    snapshot()
poco(text="佳琦推荐 欧伊俪珍珠纹洗脸巾").click()
# poco(text="KitchenAid 珐琅壶").click
poco(text="加入购物车")
poco(text="珍珠纹（20*20）100张")[1].click()
# poco(text="1").set_text(2)
poco(text="确定").click()
poco(text="购物车")[1].click()

poco(text="彩创官方平台").click()
poco(text="去结算").click()
if poco(text=" 新建收货地址").exists():
    poco(text=" 新建收货地址").click()
    poco(text="请填写收货人姓名").click()
    poco(text="请填写收货人姓名").set_text("test")
    sleep(1)
    poco(text="请填写收货人手机号").click()
    poco(text="请填写收货人手机号").set_text("15812103729")
    poco(text="国家、省市区县、乡镇等").click()
    poco(text="确定").click()
    poco(text="街道、楼牌号、小区、单元室等").click()
    poco(text="街道、楼牌号、小区、单元室等").set_text("测试地址")
    poco(text="保存").click()
poco(text="提交订单").click()
poco("com.tencent.mm:id/g78").click()
poco("com.tencent.mm:id/g78").click()
poco("com.tencent.mm:id/al3").click()



