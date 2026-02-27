# -*- coding: utf-8 -*-
from flask import jsonify


def success(data=None, msg='ok', code=200):
    """统一成功响应"""
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data
    }), 200


def fail(msg='error', http_code=400, code=None):
    """统一失败响应"""
    return jsonify({
        'code': code or http_code,
        'msg': msg,
        'data': None
    }), http_code
