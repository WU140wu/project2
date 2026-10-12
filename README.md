# 校园科创作品展示平台

面向校内学生，用来发布、浏览科创项目，可上传简介与图片、留言评论。全栈练手项目，方便后续升级为参赛作品。

## 技术栈

| 层 | 技术 |
| --- | --- |
| 后端 | Python Flask 3 + Flask-SQLAlchemy + Flask-JWT-Extended |
| 数据库 | MySQL 8（3 张表：user / project / comment） |
| 前端 | uni-app（Vue3，HBuilderX 开发） |
| 部署 | 本地 Nginx 反向代理 |
| 托管 | GitHub 私有仓库 |

## 目录结构

```
project2/
├── backend/            # Flask 后端
│   ├── app.py          # 应用工厂 + 启动入口
│   ├── config.py       # 配置（从环境变量 / .env 读取）
│   ├── extensions.py   # db / jwt / cors 实例
│   ├── models.py       # 数据模型（3 张表）
│   ├── utils.py        # 统一返回格式、管理员校验
│   ├── routes/         # 接口蓝图
│   ├── sql/schema.sql  # 建表脚本
│   └── uploads/        # 上传图片（本地，已 gitignore）
├── docs/API.md         # 接口文档
└── README.md
```

## 快速开始（后端）

1. 准备数据库：确保 MySQL 已启动，执行 `backend/sql/schema.sql` 建库建表（或首次启动后端会自动建表）。
2. 创建虚拟环境并安装依赖：

```bash
cd backend
python -m venv venv
venv/Scripts/activate        # Windows（Git Bash 用 source venv/Scripts/activate）
pip install -r requirements.txt
```

3. 配置环境变量：复制 `.env.example` 为 `.env`，填入真实数据库密码。

```bash
cp .env.example .env
```

4. 启动服务：

```bash
python app.py
# 默认 http://127.0.0.1:5000，健康检查 GET /api/health
```

## 角色说明

- 注册的用户默认为「普通学生」，可浏览、评论、发布项目、查看自己发布的项目。
- 管理员可编辑/删除任意项目与评论。把某个用户提为管理员：

```sql
UPDATE `user` SET role='admin' WHERE username='你的账号';
```

## 下一步

- 用 Postman 测试全部接口（见 `docs/API.md`）
- HBuilderX 新建 uni-app 项目对接后端
- 本地 Nginx 配置前后端联调
