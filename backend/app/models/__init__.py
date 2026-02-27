# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 用户-角色关联表（多对多）
user_role = db.Table(
    'user_role',
    db.Column('user_id', db.BigInteger, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.BigInteger, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('enabled_flag', db.Boolean, default=True)
)

# 角色-权限关联表（多对多）
role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.BigInteger, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.BigInteger, db.ForeignKey('permission.id'), primary_key=True),
    db.Column('enabled_flag', db.Boolean, default=True)
)
