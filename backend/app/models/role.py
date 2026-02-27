# -*- coding: utf-8 -*-
from datetime import datetime
from app.models import db


class Role(db.Model):
    """角色表"""
    __tablename__ = 'roles'
    __table_args__ = {'mysql_charset': 'utf8', 'extend_existing': True}

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键')
    name = db.Column(db.String(64), nullable=True, index=True, comment='角色名称')
    role_code = db.Column(db.String(64), nullable=True, index=True, comment='角色编码')
    description = db.Column(db.String(500), nullable=True, comment='描述')
    status = db.Column(db.Integer, nullable=True, default=10, comment='状态 10启用 20禁用')
    enabled_flag = db.Column(db.Boolean, nullable=False, default=True, comment='是否有效')
    creation_date = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    created_by = db.Column(db.BigInteger, nullable=True, comment='创建人')
    updation_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    updated_by = db.Column(db.BigInteger, nullable=True, comment='更新人')

    # 多对多关联权限（通过 role_permission 表）
    permissions = db.relationship(
        'Permission',
        secondary='role_permission',
        backref=db.backref('roles', lazy='dynamic'),
        lazy='select'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role_code': self.role_code,
            'description': self.description,
            'status': self.status,
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S') if self.creation_date else None,
        }


class Permission(db.Model):
    """权限表"""
    __tablename__ = 'permission'
    __table_args__ = {'mysql_charset': 'utf8', 'extend_existing': True}

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键')
    permission_code = db.Column(db.String(100), nullable=False, unique=True, index=True, comment='权限编码')
    permission_name = db.Column(db.String(100), nullable=False, comment='权限名称')
    permission_type = db.Column(db.SmallInteger, nullable=False, comment='1菜单 2按钮 3数据 4API')
    status = db.Column(db.SmallInteger, nullable=True, default=1, comment='1启用 0禁用')
    sort = db.Column(db.Integer, nullable=True, default=0, comment='排序')
    description = db.Column(db.String(500), nullable=True, comment='描述')
    enabled_flag = db.Column(db.Boolean, nullable=False, default=True, comment='是否有效')
    creation_date = db.Column(db.DateTime, default=datetime.now, comment='创建时间')

    def to_dict(self):
        return {
            'id': self.id,
            'permission_code': self.permission_code,
            'permission_name': self.permission_name,
            'permission_type': self.permission_type,
            'status': self.status,
            'sort': self.sort,
            'description': self.description,
        }
