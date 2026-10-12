from flask import Blueprint, request
from flask_jwt_extended import get_current_user, jwt_required

from extensions import db
from models import Comment, Project
from utils import fail, ok

comments_bp = Blueprint("comments", __name__)


@comments_bp.get("/projects/<int:project_id>/comments")
def list_comments(project_id):
    if db.session.get(Project, project_id) is None:
        return fail("项目不存在", 404)

    comments = (
        Comment.query.filter_by(project_id=project_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return ok({"list": [c.to_dict() for c in comments]})


@comments_bp.post("/projects/<int:project_id>/comments")
@jwt_required()
def create_comment(project_id):
    user = get_current_user()
    if db.session.get(Project, project_id) is None:
        return fail("项目不存在", 404)

    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return fail("评论内容不能为空")
    if len(content) > 1000:
        return fail("评论过长")

    comment = Comment(project_id=project_id, user_id=user.id, content=content)
    db.session.add(comment)
    db.session.commit()
    return ok(comment.to_dict(), "评论成功")


@comments_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    user = get_current_user()
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        return fail("评论不存在", 404)

    # 管理员可删任意评论，普通用户只能删自己的
    if user.role != "admin" and comment.user_id != user.id:
        return fail("没有权限删除该评论", 403)

    db.session.delete(comment)
    db.session.commit()
    return ok(message="删除成功")
