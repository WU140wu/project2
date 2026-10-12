import io
import os
import tempfile

# 用临时 SQLite 文件库代替 MySQL，验证整套接口逻辑
db_path = os.path.join(tempfile.gettempdir(), "kechuang_smoke.db")
if os.path.exists(db_path):
    os.remove(db_path)
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from app import create_app

app = create_app()
app.config["TESTING"] = True
client = app.test_client()

# 健康检查
assert client.get("/api/health").status_code == 200

# 注册
r = client.post("/api/auth/register", json={"username": "alice", "password": "123456", "nickname": "Alice"})
assert r.status_code == 200, r.get_json()
# 重复注册
assert client.post("/api/auth/register", json={"username": "alice", "password": "123456"}).status_code == 409

# 登录 + 错误密码
r = client.post("/api/auth/login", json={"username": "alice", "password": "123456"})
assert r.status_code == 200, r.get_json()
token = r.get_json()["data"]["token"]
assert client.post("/api/auth/login", json={"username": "alice", "password": "wrong"}).status_code == 401

h = {"Authorization": f"Bearer {token}"}

# 当前用户
assert client.get("/api/auth/me", headers=h).status_code == 200

# 发布项目
r = client.post("/api/projects", headers=h, json={
    "title": "智能小车", "summary": "简介", "detail": "详情",
    "cover_url": "/uploads/x.jpg", "images": ["/uploads/a.jpg", "/uploads/b.jpg"],
})
assert r.status_code == 200, r.get_json()
pid = r.get_json()["data"]["id"]

# 未登录发布 -> 401
assert client.post("/api/projects", json={"title": "x", "summary": "s", "detail": "d"}).status_code == 401

# 列表 / 搜索 / 详情
assert client.get("/api/projects").get_json()["data"]["total"] == 1
assert client.get("/api/projects?keyword=小车").get_json()["data"]["total"] == 1
assert client.get("/api/projects?keyword=不存在").get_json()["data"]["total"] == 0
r = client.get(f"/api/projects/{pid}")
assert r.status_code == 200 and r.get_json()["data"]["images"] == ["/uploads/a.jpg", "/uploads/b.jpg"]

# 我的项目
assert len(client.get("/api/projects/mine", headers=h).get_json()["data"]["list"]) == 1

# 评论
r = client.post(f"/api/projects/{pid}/comments", headers=h, json={"content": "不错"})
assert r.status_code == 200
cid = r.get_json()["data"]["id"]
assert len(client.get(f"/api/projects/{pid}/comments").get_json()["data"]["list"]) == 1

# 图片上传
r = client.post("/api/upload", headers=h, data={"file": (io.BytesIO(b"fake"), "t.png")}, content_type="multipart/form-data")
assert r.status_code == 200, r.get_json()
up = r.get_json()["data"]["url"]
os.remove(os.path.join(app.config["UPLOAD_FOLDER"], up.rsplit("/", 1)[1]))

# 清理：删项目 -> 级联删评论
assert client.delete(f"/api/projects/{pid}", headers=h).status_code == 200
assert client.get("/api/projects").get_json()["data"]["total"] == 0

print("ALL SMOKE TESTS PASSED")
