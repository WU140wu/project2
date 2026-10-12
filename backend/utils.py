from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_current_user


def ok(data=None, message="success"):
    """成功返回：{code: 0, message, data}"""
    return jsonify({"code": 0, "message": message, "data": data})


def fail(message="error", status=400):
    """失败返回：{code: <状态码>, message}"""
    return jsonify({"code": status, "message": message}), status


def admin_required(fn):
    """要求当前用户是管理员（需配合 @jwt_required() 一起使用）。"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user is None or user.role != "admin":
            return fail("需要管理员权限", 403)
        return fn(*args, **kwargs)

    return wrapper
