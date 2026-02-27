# -*- coding: utf-8 -*-
from flask import Blueprint
from app.models.role import Permission
from app.utils.jwt_utils import login_required
from app.utils.response import success

permission_bp = Blueprint('permission', __name__)


@permission_bp.get('/api/v1/system/permission')
@login_required
def get_permissions():
    """获取所有权限列表"""
    permissions = Permission.query.filter_by(enabled_flag=True).order_by(
        Permission.permission_type, Permission.sort
    ).all()
    return success([p.to_dict() for p in permissions])
