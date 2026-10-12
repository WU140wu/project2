from flask import Blueprint, request
from flask_jwt_extended import get_current_user, jwt_required

from extensions import db
from models import Project
from utils import fail, ok

projects_bp = Blueprint("projects", __name__)


@projects_bp.get("")
def list_projects():
    """分页查询，支持 title 关键词搜索。"""
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    keyword = (request.args.get("keyword") or "").strip()

    page = max(page, 1)
    page_size = min(max(page_size, 1), 50)

    query = Project.query
    if keyword:
        query = query.filter(Project.title.like(f"%{keyword}%"))

    pagination = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )

    return ok(
        {
            "list": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": page,
            "page_size": page_size,
            "pages": pagination.pages,
        }
    )


@projects_bp.get("/mine")
@jwt_required()
def my_projects():
    """当前用户发布的项目。"""
    user = get_current_user()
    projects = (
        Project.query.filter_by(user_id=user.id)
        .order_by(Project.created_at.desc())
        .all()
    )
    return ok({"list": [p.to_dict() for p in projects]})


@projects_bp.get("/<int:project_id>")
def project_detail(project_id):
    project = db.session.get(Project, project_id)
    if project is None:
        return fail("项目不存在", 404)
    return ok(project.to_dict())


@projects_bp.post("")
@jwt_required()
def create_project():
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    summary = (data.get("summary") or "").strip()
    detail = (data.get("detail") or "").strip()

    if not title or not summary or not detail:
        return fail("标题、简介、详情不能为空")

    project = Project(
        title=title,
        summary=summary,
        detail=detail,
        cover_url=data.get("cover_url") or "",
        images=data.get("images") or [],
        user_id=user.id,
    )
    db.session.add(project)
    db.session.commit()
    return ok(project.to_dict(), "发布成功")


@projects_bp.put("/<int:project_id>")
@jwt_required()
def update_project(project_id):
    user = get_current_user()
    project = db.session.get(Project, project_id)
    if project is None:
        return fail("项目不存在", 404)

    # 管理员可改任意项目，普通用户只能改自己的
    if user.role != "admin" and project.user_id != user.id:
        return fail("没有权限修改该项目", 403)

    data = request.get_json(silent=True) or {}
    if "title" in data:
        project.title = data["title"].strip()
    if "summary" in data:
        project.summary = data["summary"].strip()
    if "detail" in data:
        project.detail = data["detail"].strip()
    if "cover_url" in data:
        project.cover_url = data["cover_url"] or ""
    if "images" in data:
        project.images = data["images"] or []

    db.session.commit()
    return ok(project.to_dict(), "更新成功")


@projects_bp.delete("/<int:project_id>")
@jwt_required()
def delete_project(project_id):
    user = get_current_user()
    project = db.session.get(Project, project_id)
    if project is None:
        return fail("项目不存在", 404)

    if user.role != "admin" and project.user_id != user.id:
        return fail("没有权限删除该项目", 403)

    db.session.delete(project)
    db.session.commit()
    return ok(message="删除成功")
