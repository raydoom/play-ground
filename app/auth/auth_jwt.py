import jwt, datetime, time
from django.contrib.auth.hashers import make_password, check_password
from app.models import UserInfo

SECRET_KEY = 'maxd'

class Auth():
    # 生成认证Token, 参数user_id: int类型, 参数login_time: 类型int(timestamp)
    def encode_auth_token(user_id, login_time):
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
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e
    # 验证Token
    def decode_auth_token(auth_token):
        try:
            # payload = jwt.decode(auth_token, SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, SECRET_KEY, options={'verify_exp': False})
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
    def identify(self, req_data_msg):
        jwt_token = req_data_msg.get('Head').get('jwt_token', '')
        if not jwt_token:
            result = {'state':'fail' ,'data':'', 'msg':'没有提供认证token'}
        else:
            payload = self.decode_auth_token(jwt_token)
            user = UserInfo.objects.get(user_id=payload['data']['user_id'])
            if (user is None):
                result = {'state':'fail' ,'data':'', 'msg':'找不到该用户信息'}
            else:
                if (user.login_time == payload['data']['login_time']):
                    result = {'state':'succ', 'data':user.user_id, 'msg':'请求成功'}
                else:
                    result = {'state':'fail' ,'data':'', 'msg':'Token已更改，请重新登录获取'}
        return result