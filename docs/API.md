# 接口文档

- 基础地址：`http://127.0.0.1:5000`
- 统一返回格式：
  - 成功：HTTP 200，`{"code": 0, "message": "success", "data": {...}}`
  - 失败：HTTP 4xx，`{"code": <状态码>, "message": "错误说明"}`
- 需要登录的接口，请求头加：`Authorization: Bearer <token>`（登录接口返回）

---

## 1. 健康检查

`GET /api/health`

## 2. 用户

### 注册

`POST /api/auth/register`

```json
{ "username": "zhangsan", "password": "123456", "nickname": "张三" }
```

返回：`data` 为用户信息。

### 登录

`POST /api/auth/login`

```json
{ "username": "zhangsan", "password": "123456" }
```

返回：`data` 含 `token` 与 `user`。

### 当前用户（需登录）

`GET /api/auth/me`

## 3. 项目

### 分页列表

`GET /api/projects?page=1&page_size=10&keyword=机器人`

`keyword` 可选，按标题模糊搜索。

### 我发布的（需登录）

`GET /api/projects/mine`

### 详情

`GET /api/projects/<id>`

### 发布（需登录）

`POST /api/projects`

```json
{
  "title": "智能巡逻小车",
  "summary": "基于树莓派的校园巡逻小车",
  "detail": "详细介绍……",
  "cover_url": "/uploads/xxx.jpg",
  "images": ["/uploads/a.jpg", "/uploads/b.jpg"]
}
```

### 编辑（需登录，本人或管理员）

`PUT /api/projects/<id>`

请求体同上，只传要修改的字段即可。

### 删除（需登录，本人或管理员）

`DELETE /api/projects/<id>`

## 4. 评论

### 评论列表

`GET /api/projects/<id>/comments`

### 发表评论（需登录）

`POST /api/projects/<id>/comments`

```json
{ "content": "这个项目很赞！" }
```

### 删除评论（需登录，本人或管理员）

`DELETE /api/comments/<id>`

## 5. 图片上传（需登录）

`POST /api/upload`

`multipart/form-data`，字段名 `file`，支持 png/jpg/jpeg/gif/webp，单文件 ≤ 16MB。

返回：`data.url` 为相对路径（如 `/uploads/xxx.jpg`），前端拼接服务器地址后用于 `cover_url` 或 `images`。
