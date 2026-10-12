import os

from dotenv import load_dotenv
from flask import Flask, send_from_directory

load_dotenv()

from config import Config
from extensions import cors, db, jwt
from models import User
from routes import register_blueprints
from utils import fail, ok


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # JWT：身份存 user id，访问时反查用户
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db.session.get(User, int(identity))

    register_blueprints(app)

    @app.get("/api/health")
    def health():
        return ok({"status": "ok"})

    # 上传图片访问：GET /uploads/<文件名>
    @app.get("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.errorhandler(404)
    def not_found(e):
        return fail("接口不存在", 404)

    @app.errorhandler(413)
    def too_large(e):
        return fail("文件过大", 413)

    # 首次启动自动建表（改表结构请用迁移或手动 SQL）
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
