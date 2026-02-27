# -*- coding: utf-8 -*-
from datetime import datetime
from app.models import db


class User(db.Model):
    """用户表"""
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8', 'extend_existing': True}

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键')
    username = db.Column(db.String(64), nullable=False, index=True, comment='用户名')
    password = db.Column(db.Text, nullable=False, comment='密码')
    nickname = db.Column(db.String(255), nullable=False, default='', comment='昵称')
    email = db.Column(db.String(64), nullable=True, comment='邮箱')
    phone = db.Column(db.String(20), nullable=True, comment='手机号')
    avatar = db.Column(db.Text, nullable=True, default='', comment='头像')
    status = db.Column(db.Integer, nullable=False, default=1, comment='状态 1启用 0禁用')
    user_type = db.Column(db.Integer, nullable=False, default=20, comment='用户类型 10管理员 20普通用户')
    enabled_flag = db.Column(db.Boolean, nullable=False, default=True, comment='是否有效 1有效 0删除')
    creation_date = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    created_by = db.Column(db.BigInteger, nullable=True, comment='创建人')
    updation_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    updated_by = db.Column(db.BigInteger, nullable=True, comment='更新人')

    # 多对多关联角色（通过 user_role 表）
    roles = db.relationship(
        'Role',
        secondary='user_role',
        backref=db.backref('users', lazy='dynamic'),
        lazy='select'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'status': self.status,
            'user_type': self.user_type,
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S') if self.creation_date else None,
            'roles': [{'id': r.id, 'name': r.name, 'role_code': r.role_code} for r in self.roles]
        }
