# coding=utf8

import json, os, time, datetime, logging
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from app.models import UserInfo
from app.auth.auth_jwt import Auth
from app.utils.message import EmailSender 

# 获取日志记录方法
logger = logging.getLogger('app')

# 用户注册
class RegisterView(View):
	def post(self, request):
		req_data = json.loads(request.body.decode())
		req_body_data = req_data.get('body').get('data', {})
		username = req_body_data.get('username', '')
		password = req_body_data.get('password', '')
		repassword = req_body_data.get('repassword')
		# email_sender = EmailSender()
		# email_sender.send_mail('maxd@cloudsecca.com', 'cloudsecca', '11111')
		res_body = {}
		if len(username) == 0:
			res_code = 'mi0002'
			res_msg = '用户名不能为空'
			res_state = 'fail'
		elif len(password) == 0:
			res_code = 'mi0002'
			res_msg = '密码不能为空'
			res_state = 'fail'		
		elif password != repassword:
			res_code = 'mi0002'
			res_msg = '两次输入的密码不一致'
			res_state = 'fail'
		elif UserInfo.objects.filter(username=username).count() != 0:
			res_code = 'mi0002'
			res_msg = '用户名已存在'
			res_state = 'fail'
		else:
			password=make_password(password, None, 'pbkdf2_sha256')
			UserInfo.objects.create(username=username, password=password)
			res_code = 'mi0001'
			res_msg = '注册成功'
			res_state = 'succ'
			res_body = {'userInfo': {'username': username}}
		res_body = {'res_code': res_code, 'res_msg': res_msg, 'res_state': res_state}
		return JsonResponse(res_body)

# 用户登陆
class LoginView(View):
	def post(self, request):
		req_data = json.loads(request.body.decode())
		req_body_data = req_data.get('body').get('data', {})
		username = req_body_data.get('username')
		password = req_body_data.get('password')
		res_body = {}
		# user = UserInfo.objects.get(username=username)
		auth = Auth()
		res_body = auth.authenticate(username, password)
		logger.debug(res_body)
		return JsonResponse(res_body)

# 获取用户信息
class GetUserInfoView(View):
	def get(self, request):
		# # req_data = json.loads(request.body.decode())
		auth = Auth()
		result = auth.identify(request)
		logger.debug(result)
		return JsonResponse(result)