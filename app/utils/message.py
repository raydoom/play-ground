# coding=utf8

import smtplib
from email.mime.text import MIMEText
from app.utils.config_info_formater import ConfigInfo

# 获取配置文件中的email信息
config = ConfigInfo()

# 发送邮件
class EmailSender:
	def __init__(self):
		self.mail_host = config.config_info.get('email').get('mail_host')
		self.mail_user = config.config_info.get('email').get('mail_user')
		self.mail_pass = config.config_info.get('email').get('mail_pass')
		self.mail_postfix = config.config_info.get('email').get('mail_postfix')
		
	def send_mail(self, to_list, sub, context):
		me = self.mail_user + "<" + self.mail_user + ">"
		msg = MIMEText(context)
		msg['Subject'] = sub
		msg['From'] = me
		msg['To'] = "".join(to_list)
		try:
			send_smtp = smtplib.SMTP()
			send_smtp.connect(self.mail_host)
			send_smtp.login(self.mail_user, self.mail_pass)
			send_smtp.sendmail(me, to_list, msg.as_string())
			send_smtp.close()
			return True
		except Exception as e:
			print(str(e))
			return False


