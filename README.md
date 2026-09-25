# 校园博客 Web 系统 / Campus Blog Web System

基于 Python Flask 构建的校园博客 Web 应用，支持用户注册登录、发布文章、浏览帖子与点赞互动。

A campus-oriented blog web application built with Python Flask, allowing users to register, publish articles, browse posts, and interact through likes.

## 技术栈 / Tech Stack

- **后端 / Backend**：Python 3、Flask
- **数据库 / Database**：SQLite + SQLAlchemy ORM
- **前端 / Frontend**：HTML、CSS、JavaScript、Bootstrap、Jinja2
- **认证 / Authentication**：Flask-Login、Flask-WTF

## 功能特性 / Features

- 用户注册与登录 / User registration and login
- 用户个人资料与头像上传 / User profile with avatar upload
- 文章的创建、编辑与删除（增删改查）/ Article creation, editing, and deletion (CRUD)
- 文章浏览与详情查看 / Article browsing and detail view
- 基于 Ajax 的异步点赞 / 取消点赞 / Ajax-based asynchronous like/unlike
- 通过联合唯一约束防止重复点赞 / Duplicate like prevention via composite unique constraint
- 基于角色的权限控制（游客 vs 登录用户）/ Role-based access control (guest vs. logged-in user)
- 表单校验与安全的会话管理 / Form validation and secure session management

## 项目结构 / Project Structure

```
blog/
├── app.py              # 应用主入口 / Main application entry
├── forms.py            # Flask-WTF 表单定义 / Form definitions
├── requirements.txt    # Python 依赖 / Dependencies
├── static/
│   ├── css/
│   │   └── blog.css
│   ├── js/
│   │   ├── article_likes.js      # Ajax 点赞逻辑 / Like logic
│   │   └── password_toggle.js    # 密码显隐切换 / Password toggle
│   └── uploads/        # 用户头像上传目录 / Avatar uploads
└── templates/
    ├── base.html               # 基础模板 / Base template
    ├── index.html              # 首页 / Home
    ├── login.html              # 登录 / Login
    ├── register.html           # 注册 / Register
    ├── profile.html            # 个人中心 / Profile
    ├── article_list.html       # 文章列表 / Article list
    ├── article_view.html       # 文章详情 / Article view
    ├── article_edit.html       # 文章编辑 / Article edit
    └── navbar.html             # 导航栏 / Navbar
```

## 运行方法 / Getting Started

### 环境要求 / Prerequisites

- Python 3.10+
- pip

### 安装与启动 / Installation

1. 克隆仓库 / Clone the repository:
```bash
git clone https://github.com/zhangwanru20050121/campus-blog-flask.git
cd campus-blog-flask
```

2. 安装依赖 / Install dependencies:
```bash
pip install -r requirements.txt
```

3. 运行应用 / Run the application:
```bash
python app.py
```

4. 浏览器访问 / Open your browser and visit:
```
http://127.0.0.1:5000
```

## 关键设计 / Key Design Decisions

- **联合唯一约束 / Composite unique constraint**：Like 模型对（`user_id`、`article_id`）设置联合唯一约束，从数据库层面防止重复点赞。
- **角色权限控制 / Role-based permissions**：游客可浏览文章但不能点赞或发布；登录用户拥有完整权限。
- **异步交互 / Asynchronous interaction**：点赞通过 Ajax 实现，无需刷新页面，交互更流畅。

## 作者 / Author

张婉茹（Wanru Zhang）- 上海建桥学院 网络工程专业 / Shanghai Jianqiao University, Network Engineering
