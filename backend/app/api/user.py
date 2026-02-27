# -*- coding: utf-8 -*-
import bcrypt
from flask import Blueprint, request, g
from app.models import db
from app.models.user import User
from app.models.role import Role
from app.utils.jwt_utils import login_required
from app.utils.response import success, fail

user_bp = Blueprint('user', __name__)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


@user_bp.get('/api/v1/system/user')
@login_required
def get_users():
    """获取用户列表（分页）"""
    page = int(request.args.get('page', 1))
    page_size = min(int(request.args.get('pageSize', request.args.get('page_size', 10))), 100)
    keyword = request.args.get('username', request.args.get('keyword', '')).strip()

    query = User.query.filter_by(enabled_flag=True)
    if keyword:
        query = query.filter(
            db.or_(User.username.like(f'%{keyword}%'), User.nickname.like(f'%{keyword}%'))
        )

    pagination = query.order_by(User.id.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return success({
        'rowTotal': pagination.total,
        'pageTotal': pagination.pages,
        'page': page,
        'pageSize': page_size,
        'rows': [u.to_dict() for u in pagination.items]
    })


@user_bp.get('/api/v1/system/user/<int:user_id>')
@login_required
def get_user(user_id):
    """获取用户详情"""
    user = User.query.filter_by(id=user_id, enabled_flag=True).first()
    if not user:
        return fail('用户不存在', 404)
    return success(user.to_dict())


@user_bp.post('/api/v1/system/user')
@login_required
def create_user():
    """创建用户"""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return fail('用户名和密码不能为空')

    if User.query.filter_by(username=username, enabled_flag=True).first():
        return fail('用户名已存在')

    role_ids = data.get('role_ids', [])
    user = User(
        username=username,
        password=hash_password(password),
        nickname=data.get('nickname', username),
        email=data.get('email'),
        phone=data.get('phone'),
        status=data.get('status', 1),
        user_type=data.get('user_type', 20),
        created_by=g.user_id,
        updated_by=g.user_id,
    )
    if role_ids:
        roles = Role.query.filter(Role.id.in_(role_ids), Role.enabled_flag == True).all()
        user.roles = roles

    db.session.add(user)
    db.session.commit()
    return success(user.to_dict(), '创建成功')


@user_bp.put('/api/v1/system/user/<int:user_id>')
@login_required
def update_user(user_id):
    """更新用户"""
    user = User.query.filter_by(id=user_id, enabled_flag=True).first()
    if not user:
        return fail('用户不存在', 404)

    data = request.get_json() or {}
    if 'nickname' in data:
        user.nickname = data['nickname']
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'status' in data:
        user.status = data['status']
    if 'password' in data and data['password']:
        user.password = hash_password(data['password'])
    if 'role_ids' in data:
        roles = Role.query.filter(Role.id.in_(data['role_ids']), Role.enabled_flag == True).all()
        user.roles = roles
    user.updated_by = g.user_id

    db.session.commit()
    return success(user.to_dict(), '更新成功')


@user_bp.delete('/api/v1/system/user')
@login_required
def delete_user():
    """删除用户（支持单个和批量，通过 ?ids=1&ids=2 传参）"""
    ids = request.args.getlist('ids', type=int)
    if not ids:
        return fail('请提供要删除的用户ID')

    User.query.filter(User.id.in_(ids), User.enabled_flag == True).update(
        {'enabled_flag': False, 'updated_by': g.user_id}, synchronize_session=False
    )
    db.session.commit()
    return success(msg='删除成功')


@user_bp.put('/api/v1/system/user/<int:user_id>/status')
@login_required
def update_user_status(user_id):
    """启用/禁用用户"""
    user = User.query.filter_by(id=user_id, enabled_flag=True).first()
    if not user:
        return fail('用户不存在', 404)

    data = request.get_json() or {}
    user.status = data.get('status', 1)
    user.updated_by = g.user_id
    db.session.commit()
    return success(msg='状态更新成功')


@user_bp.put('/api/v1/system/user/<int:user_id>/reset-password')
@login_required
def reset_password(user_id):
    """管理员重置密码"""
    user = User.query.filter_by(id=user_id, enabled_flag=True).first()
    if not user:
        return fail('用户不存在', 404)

    data = request.get_json() or {}
    new_pwd = data.get('new_password', '123456')
    user.password = hash_password(new_pwd)
    user.updated_by = g.user_id
    db.session.commit()
    return success(msg='密码重置成功')
