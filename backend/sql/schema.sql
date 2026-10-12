-- 校园科创作品展示平台 建库建表脚本
-- 也可由 Flask 首次启动自动建表（见 app.py 中的 db.create_all）

CREATE DATABASE IF NOT EXISTS kechuang
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE kechuang;

-- 用户表
CREATE TABLE IF NOT EXISTS `user` (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  username      VARCHAR(50)  NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nickname      VARCHAR(50)  NOT NULL,
  role          VARCHAR(20)  NOT NULL DEFAULT 'user',  -- user / admin
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 项目表
CREATE TABLE IF NOT EXISTS `project` (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  title      VARCHAR(100) NOT NULL,
  summary    VARCHAR(500) NOT NULL,   -- 简介
  detail     TEXT         NOT NULL,   -- 详情
  cover_url  VARCHAR(255) DEFAULT '', -- 封面图
  images     JSON         DEFAULT NULL, -- 详情图片列表
  user_id    INT          NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY idx_project_user (user_id),
  CONSTRAINT fk_project_user FOREIGN KEY (user_id)
    REFERENCES `user`(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 评论表
CREATE TABLE IF NOT EXISTS `comment` (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT           NOT NULL,
  user_id    INT           NOT NULL,
  content    VARCHAR(1000) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY idx_comment_project (project_id),
  CONSTRAINT fk_comment_project FOREIGN KEY (project_id)
    REFERENCES `project`(id) ON DELETE CASCADE,
  CONSTRAINT fk_comment_user FOREIGN KEY (user_id)
    REFERENCES `user`(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 把某个已注册用户提升为管理员
-- UPDATE `user` SET role='admin' WHERE username='你的账号';
