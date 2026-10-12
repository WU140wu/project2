import os
from datetime import timedelta


class Config:
    """全局配置，敏感信息从环境变量 / .env 读取。"""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # MySQL 连接串：mysql+pymysql://用户名:密码@主机:端口/数据库?charset=utf8mb4
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@127.0.0.1:3306/kechuang?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 连接断线自动重连
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 3600}

    # 上传
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 单次请求上限 16MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
