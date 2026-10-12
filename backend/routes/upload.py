import os
import uuid

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from config import Config
from utils import fail, ok

upload_bp = Blueprint("upload", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@upload_bp.post("/upload")
@jwt_required()
def upload():
    if "file" not in request.files:
        return fail("未收到文件")

    file = request.files["file"]
    if file.filename == "":
        return fail("文件名为空")

    if not allowed_file(file.filename):
        return fail("仅支持图片：png/jpg/jpeg/gif/webp")

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"  # 随机文件名，避免重名与路径注入

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    file.save(os.path.join(Config.UPLOAD_FOLDER, filename))

    # 返回相对路径，前端拼接服务器地址后使用
    return ok({"url": f"/uploads/{filename}"}, "上传成功")
