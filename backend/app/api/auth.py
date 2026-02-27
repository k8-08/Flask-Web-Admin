# -*- coding: utf-8 -*-
import bcrypt
from flask import Blueprint, request, g
from app.models.user import User
from app.utils.jwt_utils import generate_token, login_required
from app.utils.response import success, fail

auth_bp = Blueprint('auth', __name__)


def check_password(plain: str, hashed: str) -> bool:
    """验证密码"""
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


@auth_bp.post('/api/v1/system/auth/login')
def login():
    """用户登录"""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return fail('用户名和密码不能为空')

    user = User.query.filter_by(username=username, enabled_flag=True).first()
    if not user:
        return fail('用户名或密码错误', 401)

    if not check_password(password, user.password):
        return fail('用户名或密码错误', 401)

    if user.status != 1:
        return fail('用户已被禁用', 403)

    token = generate_token(user.id)
    return success({
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': 86400,
    }, '登录成功')


@auth_bp.post('/api/v1/system/auth/logout')
@login_required
def logout():
    """用户登出（前端删除 token 即可，服务端不做处理）"""
    return success(msg='登出成功')


@auth_bp.get('/api/v1/system/auth/userinfo')
@login_required
def userinfo():
    """获取当前用户信息"""
    user = User.query.get(g.user_id)
    if not user or not user.enabled_flag:
        return fail('用户不存在', 404)

    role_codes = [r.role_code for r in user.roles if r.enabled_flag]
    permissions = []
    for role in user.roles:
        if role.enabled_flag:
            for perm in role.permissions:
                if perm.enabled_flag and perm.permission_code not in permissions:
                    permissions.append(perm.permission_code)

    return success({
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'email': user.email,
        'phone': user.phone,
        'avatar': user.avatar,
        'user_type': user.user_type,
        'roles': role_codes,
        'permissions': permissions,
    })


@auth_bp.get('/api/v1/system/auth/menus')
@login_required
def menus():
    """返回用户菜单（前端路由用）— 返回空列表，路由由前端自行控制"""
    return success([])


@auth_bp.get('/api/v1/system/auth/permissions')
@login_required
def permissions():
    """返回当前用户的权限编码列表"""
    user = User.query.get(g.user_id)
    if not user or not user.enabled_flag:
        return fail('用户不存在', 404)

    perm_codes = []
    for role in user.roles:
        if role.enabled_flag:
            for perm in role.permissions:
                if perm.enabled_flag and perm.permission_code not in perm_codes:
                    perm_codes.append(perm.permission_code)

    return success(perm_codes)
