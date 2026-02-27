# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from app.models import db


def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['JWT_EXPIRE_HOURS'] = config.JWT_EXPIRE_HOURS
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO

    # 初始化扩展
    db.init_app(app)
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    # 注册蓝图
    from app.api.auth import auth_bp
    from app.api.user import user_bp
    from app.api.role import role_bp
    from app.api.permission import permission_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(permission_bp)

    # 字典/Lookup stub：返回空列表，避免前端 404
    from app.utils.jwt_utils import login_required
    from flask import jsonify as _jsonify

    @app.get('/api/v1/system/dict/type/list/all')
    @login_required
    def dict_type_list():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': []}), 200

    @app.get('/api/v1/system/dict/data/list/all')
    @login_required
    def dict_data_list():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': []}), 200

    # 菜单管理 stub（前端 /system/menu 页面渲染用）
    MOCK_MENUS = [
        {
            "id": 1, "parent_id": 0, "menu_name": "首页", "path": "/home",
            "component": "/src/views/home/index.vue", "perms": "", "component_name": "home",
            "order_num": 1, "menu_type": "C", "icon": "iconfont icon-shouye", "status": 1
        },
        {
            "id": 2, "parent_id": 0, "menu_name": "系统设置", "path": "/system",
            "component": "/src/layout/routerView/parent.vue", "perms": "", "component_name": "system",
            "order_num": 2, "menu_type": "M", "icon": "iconfont icon-xitongshezhi", "status": 1
        },
        {
            "id": 3, "parent_id": 2, "menu_name": "菜单管理", "path": "/system/menu",
            "component": "/src/views/system/menu/index.vue", "perms": "system:menu:list", "component_name": "systemMenu",
            "order_num": 1, "menu_type": "C", "icon": "ele-Menu", "status": 1
        },
        {
            "id": 4, "parent_id": 2, "menu_name": "角色管理", "path": "/system/role",
            "component": "/src/views/system/role/index.vue", "perms": "system:role:list", "component_name": "systemRole",
            "order_num": 2, "menu_type": "C", "icon": "ele-ColdDrink", "status": 1
        },
        {
            "id": 5, "parent_id": 2, "menu_name": "用户管理", "path": "/system/user",
            "component": "/src/views/system/user/index.vue", "perms": "system:user:list", "component_name": "systemUser",
            "order_num": 3, "menu_type": "C", "icon": "ele-User", "status": 1
        },
        {
            "id": 6, "parent_id": 2, "menu_name": "部门管理", "path": "/system/dept",
            "component": "/src/views/system/dept/index.vue", "perms": "system:dept:list", "component_name": "systemDept",
            "order_num": 4, "menu_type": "C", "icon": "ele-OfficeBuilding", "status": 1
        }
    ]

    @app.get('/api/v1/system/menu')
    @login_required
    def menu_list():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': MOCK_MENUS, 'total': len(MOCK_MENUS)}), 200

    @app.get('/api/v1/system/menu/tree')
    @login_required
    def menu_tree():
        # 构建树形
        tree = []
        for menu in MOCK_MENUS:
            if menu['parent_id'] == 0:
                menu_copy = dict(menu)
                menu_copy['children'] = [dict(m) for m in MOCK_MENUS if m['parent_id'] == menu['id']]
                tree.append(menu_copy)
        return _jsonify({'code': 200, 'msg': 'ok', 'data': tree, 'total': len(tree)}), 200

    @app.post('/api/v1/system/menu')
    @login_required
    def menu_create():
        return _jsonify({'code': 200, 'msg': '暂不支持菜单管理，使用静态路由', 'data': None}), 200

    # 部门管理 stub（前端 /system/dept 页面渲染用）
    @app.get('/api/v1/system/dept')
    @login_required
    def dept_list():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': []}), 200

    @app.get('/api/v1/system/dept/tree')
    @login_required
    def dept_tree():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': []}), 200

    @app.post('/api/v1/system/dept')
    @login_required
    def dept_create():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': None}), 200

    # 字典管理 stub
    @app.get('/api/v1/system/dict/type')
    @login_required
    def dict_type_list2():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': [], 'total': 0}), 200

    @app.post('/api/v1/system/dict/type')
    @login_required
    def dict_type_create():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': None}), 200

    @app.get('/api/v1/system/dict/data')
    @login_required
    def dict_data_list2():
        return _jsonify({'code': 200, 'msg': 'ok', 'data': [], 'total': 0}), 200

    # 全局错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'code': 404, 'msg': '接口不存在', 'data': None}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'code': 405, 'msg': '方法不允许', 'data': None}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'code': 500, 'msg': '服务器内部错误', 'data': None}), 500

    return app
