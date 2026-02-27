# -*- coding: utf-8 -*-
from flask import Blueprint, request, g
from app.models import db
from app.models.role import Role, Permission
from app.utils.jwt_utils import login_required
from app.utils.response import success, fail

role_bp = Blueprint('role', __name__)


@role_bp.get('/api/v1/system/role')
@login_required
def get_roles():
    """获取角色列表"""
    roles = Role.query.filter_by(enabled_flag=True).order_by(Role.id.desc()).all()
    return success([r.to_dict() for r in roles])


@role_bp.post('/api/v1/system/role')
@login_required
def create_role():
    """创建角色"""
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if not name:
        return fail('角色名称不能为空')

    if Role.query.filter_by(name=name, enabled_flag=True).first():
        return fail('角色名称已存在')

    role = Role(
        name=name,
        role_code=data.get('role_code', ''),
        description=data.get('description', ''),
        status=data.get('status', 10),
        created_by=g.user_id,
        updated_by=g.user_id,
    )
    db.session.add(role)
    db.session.commit()
    return success(role.to_dict(), '创建成功')


@role_bp.put('/api/v1/system/role/<int:role_id>')
@login_required
def update_role(role_id):
    """更新角色"""
    role = Role.query.filter_by(id=role_id, enabled_flag=True).first()
    if not role:
        return fail('角色不存在', 404)

    data = request.get_json() or {}
    if 'name' in data:
        role.name = data['name']
    if 'role_code' in data:
        role.role_code = data['role_code']
    if 'description' in data:
        role.description = data['description']
    if 'status' in data:
        role.status = data['status']
    role.updated_by = g.user_id

    db.session.commit()
    return success(role.to_dict(), '更新成功')


@role_bp.delete('/api/v1/system/role/<int:role_id>')
@login_required
def delete_role(role_id):
    """删除角色（逻辑删除）"""
    role = Role.query.filter_by(id=role_id, enabled_flag=True).first()
    if not role:
        return fail('角色不存在', 404)

    role.enabled_flag = False
    role.updated_by = g.user_id
    db.session.commit()
    return success(msg='删除成功')


@role_bp.get('/api/v1/system/role/<int:role_id>/permissions')
@login_required
def get_role_permissions(role_id):
    """获取角色的权限ID列表"""
    role = Role.query.filter_by(id=role_id, enabled_flag=True).first()
    if not role:
        return fail('角色不存在', 404)

    perm_ids = [p.id for p in role.permissions if p.enabled_flag]
    return success(perm_ids)


@role_bp.put('/api/v1/system/role/<int:role_id>/permissions')
@login_required
def update_role_permissions(role_id):
    """更新角色权限"""
    role = Role.query.filter_by(id=role_id, enabled_flag=True).first()
    if not role:
        return fail('角色不存在', 404)

    data = request.get_json() or {}
    perm_ids = data.get('permission_ids', [])
    permissions = Permission.query.filter(
        Permission.id.in_(perm_ids), Permission.enabled_flag == True
    ).all()
    role.permissions = permissions
    role.updated_by = g.user_id

    db.session.commit()
    return success(msg='权限更新成功')
