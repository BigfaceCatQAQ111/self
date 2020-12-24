#coding:utf-8

import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from public.common.log import Log
# from config import globalparam

# 测试报告的路径

project_name = os.getcwd().split('\\')[1]

# 配置收发件人
recvaddress = ['841120827@qq.com']
# 163的用户名和密码
sendaddr_name = 'chejingbo@ynlcgroup.com'
sendaddr_pswd = 'nishiZHU110'

class SendMail:
	def __init__(self,recver=None):
		"""接收邮件的人：list or tuple"""
		if recver is None:
			self.sendTo = recvaddress
		else:
			self.sendTo = recver

	def __get_report(self,air):
		"""获取最新测试报告"""
		report_dir = os.path.join(os.getcwd(), 'FTP_report',air)
		list = os.listdir(report_dir)
		list.sort(key=lambda fn: os.path.getmtime(report_dir + '\\' + fn))
		report = os.path.join(report_dir, list[-1])
		report_to_send = report+"\\" + air + "_report.html"
		print('The new report name: {0}'.format(report_to_send))
		return report_to_send

	def __take_messages(self,air):
		"""生成邮件的内容，和html报告附件"""
		newreport = self.__get_report(air)
		report_dir = os.path.join(os.getcwd(), 'FTP_report', air)
		list = os.listdir(report_dir)
		list.sort(key=lambda fn: os.path.getmtime(report_dir + '\\' + fn))
		report = os.path.join(report_dir, list[-1])
		dir = report.split("\\")[-1]
		url = "http://47.108.203.157:15000/multi-device-runner-master/" + '/' + air + '/' + dir + "/" + air + "_report.html"
		self.msg = MIMEMultipart()
		self.msg['Subject'] = project_name
		self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
		self.msg['url'] = url

		with open(os.path.join(newreport), 'rb') as f:
			mailbody = f.read()
		html = MIMEText(mailbody, _subtype='html', _charset='utf-8')
		self.msg.attach(html)

		# report_dir = os.path.join(os.getcwd(), 'FTP_report', air)
		# list = os.listdir(report_dir)
		# list.sort(key=lambda fn: os.path.getmtime(report_dir + '\\' + fn))
		# report = os.path.join(report_dir, list[-1])
		# dir = report.split("\\")[-1]
		# url = "http://47.108.203.157:15000/multi-device-runner-master/" + '/' + air + '/'+  dir + "/"+ air+"_report.html"
		# att = MIMEText(url, 'base64', 'utf-8')
		# att["Content-Type"] = 'application/octet-stream'
		# att['Content-Disposition'] = 'attachment;访问连接="%s"' % (url)
		# self.msg.attach(att)

		# html附件
		att1 = MIMEText(mailbody, 'base64', 'gb2312')
		att1["Content-Type"] = 'application/octet-stream'
		att1["Content-Disposition"] = 'attachment; filename="TestReport.html"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
		self.msg.attach(att1)

	def send(self,air):
		"""发送邮件"""
		self.__take_messages(air)
		self.msg['from'] = sendaddr_name
		try:
			smtp = smtplib.SMTP('smtp.exmail.qq.com',25)
			smtp.login(sendaddr_name, sendaddr_pswd)
			smtp.sendmail(self.msg['from'], self.sendTo, self.msg.as_string())
			smtp.close()
			print("发送邮件成功")
		except Exception:
			print('发送邮件失败')
			raise

if __name__ == '__main__':
	sendMail = SendMail()
	sendMail.send()

