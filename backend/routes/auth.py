from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_current_user, jwt_required

from extensions import db
from models import User
from utils import fail, ok

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    nickname = (data.get("nickname") or "").strip() or username

    if not username or not password:
        return fail("账号和密码不能为空")
    if len(username) > 50 or len(password) < 6:
        return fail("账号过长或密码不足 6 位")
    if User.query.filter_by(username=username).first():
        return fail("账号已存在", 409)

    user = User(username=username, nickname=nickname, role="user")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return ok(user.to_dict(), "注册成功")


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return fail("账号或密码错误", 401)

    token = create_access_token(identity=user)
    return ok({"token": token, "user": user.to_dict()}, "登录成功")


@auth_bp.get("/me")
@jwt_required()
def me():
    user = get_current_user()
    if user is None:
        return fail("用户不存在", 404)
    return ok(user.to_dict())
