# coding=utf8

import jwt, datetime, time
from django.contrib.auth.hashers import make_password, check_password
from app.models import UserInfo
from app.utils.config_info_formater import ConfigInfo

# 获取配置文件中的jwt_secret_key
config = ConfigInfo()
jwt_secret_key = config.config_info.get('jwt_info').get('jwt_secret_key')
jwt_expire = int(config.config_info.get('jwt_info').get('jwt_expire'))

class Auth():
	# 生成认证Token, 参数user_id: int类型, 参数login_time: 类型int(timestamp)
	def encode_auth_token(self, user_id, login_time):
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
				'iat': datetime.datetime.utcnow(),
				'iss': 'maxd',
				'data': {
					'user_id': user_id,
					'login_time': login_time
				}
			}
			return jwt.encode(
				payload,
				jwt_secret_key,
				algorithm='HS256'
			)
		except Exception as e:
			return e
	# 验证Token
	def decode_auth_token(self, auth_token):
		try:
			#payload = jwt.decode(auth_token, jwt_secret_key, leeway=datetime.timedelta(seconds=jwt_expire))
			# 取消过期时间验证
			payload = jwt.decode(auth_token, jwt_secret_key, options={'verify_exp': False})
			if ('data' in payload and 'user_id' in payload['data']):
				return payload
			else:
				raise jwt.InvalidTokenError
		except jwt.ExpiredSignatureError:
			return 'Token过期'
		except jwt.InvalidTokenError:
			return '无效Token'

	# 用户登录，登录成功返回token，将登录时间写入数据库；登录失败返回失败原因        
	def authenticate(self, username, password):
		user = UserInfo.objects.filter(username=username).first()
		if (user is None):
			return ({'state':'fail' ,'data':'', 'msg':'用户不存在'})
		else:
			if check_password(password, user.password):
				login_time = int(time.time())
				user.login_time = login_time
				user.save()
				token = self.encode_auth_token(user.user_id, login_time)
				return ({'state':'succ', 'data':token.decode(), 'msg':'登录成功'})
			else:
				return ({'state':'fail' ,'data':'', 'msg':'密码不正确'})
	# 用户鉴权
	def identify(self, request):
		auth_header = request.META.get('HTTP_AUTHORIZATION')
		if (auth_header):
			auth_token_arr = auth_header.split(" ")
			if (not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2):
				result = {'state':'fail' ,'data':'', 'msg':'请传递正确的验证头信息'}  
			else:
				auth_token = auth_token_arr[1]
				payload = self.decode_auth_token(auth_token)
				if not isinstance(payload, str):
					user = UserInfo.objects.get(user_id=payload['data']['user_id'])
					if (user is None):
						result = {'state':'fail' ,'data':'', 'msg':'找不到该用户信息'}
					else:
						if (user.login_time == payload['data']['login_time']):
							result = {'state':'succ', 'data':user.user_id, 'msg':'请求成功'}
						else:
							result = {'state':'fail' ,'data':'', 'msg':'Token已更改，请重新登录获取'}
				else:
					result = {'state':'fail' ,'data':'', 'msg':payload}
		else:
			result = {'state':'fail' ,'data':'', 'msg':'没有提供认证token'}
		return result