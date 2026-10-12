from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(db.Model):
    """用户表：普通学生 / 管理员。"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # user / admin
    created_at = db.Column(db.DateTime, default=datetime.now)

    projects = db.relationship(
        "Project", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )
    comments = db.relationship(
        "Comment", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Project(db.Model):
    """项目表：标题、简介、详情、封面图、详情图片列表。"""

    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(500), nullable=False)  # 简介（列表页展示）
    detail = db.Column(db.Text, nullable=False)          # 详情（详情页展示）
    cover_url = db.Column(db.String(255), default="")    # 封面图
    images = db.Column(db.JSON, default=list)            # 详情图片列表
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    comments = db.relationship(
        "Comment", backref="project", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self, include_author=True):
        data = {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "detail": self.detail,
            "cover_url": self.cover_url,
            "images": self.images or [],
            "created_at": self.created_at.isoformat(),
            "comment_count": self.comments.count(),
        }
        if include_author and self.author:
            data["author"] = {"id": self.author.id, "nickname": self.author.nickname}
        return data


class Comment(db.Model):
    """评论表：某项目下的某用户留言。"""

    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "author": (
                {"id": self.author.id, "nickname": self.author.nickname}
                if self.author
                else None
            ),
        }
