# -*- coding: utf-8 -*-
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, current_app, g
from app.utils.response import fail


def generate_token(user_id: int) -> str:
    """生成 JWT token"""
    payload = {
        'sub': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRE_HOURS'])
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def verify_token(token: str) -> dict:
    """验证 JWT token，返回 payload"""
    return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return fail('未提供认证 token', 401)
        token = auth_header[7:]
        try:
            payload = verify_token(token)
            g.user_id = payload['sub']
        except jwt.ExpiredSignatureError:
            return fail('token 已过期，请重新登录', 401)
        except jwt.InvalidTokenError:
            return fail('token 无效', 401)
        return f(*args, **kwargs)
    return decorated
