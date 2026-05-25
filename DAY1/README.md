# Django DAY1 — 让 Django 的小火箭起飞

## 作业背景

使用 Python 3.12.12 创建虚拟环境，安装 Django 5.2.1，创建全新 Django 项目 `day01site`，启动开发服务器并在浏览器中看到 Django 默认的"小火箭"欢迎页面，验证 Django 环境搭建成功。

## 实验环境

| 组件 | 版本/地址 |
|------|-----------|
| Linux 服务器 | 10.10.1.205 (Rocky Linux 9.7) |
| Python | 3.12.12 |
| Django | 5.2.1 |
| 开发服务器 | http://0.0.0.0:8000 |
| 虚拟环境路径 | `/tmp/.venv_django`（独立于项目目录，不随项目提交） |

## 项目结构

```
DAY1/
└── day01site/
    ├── manage.py               # Django 管理脚本
    └── day01site/
        ├── __init__.py         # 包标识
        ├── settings.py         # 项目配置（数据库/中间件/模板等）
        ├── urls.py             # URL 路由配置
        ├── asgi.py             # ASGI 入口
        └── wsgi.py             # WSGI 入口
```

## 任务说明

### 任务一：搭建 Django 开发环境并启动小火箭页面

**要求：**
1. 使用 Python 3.12.12 创建虚拟环境
2. 安装固定版本 Django 5.2.1
3. 使用 `django-admin startproject` 创建项目
4. 启动开发服务器，运行不能报错
5. 浏览器访问看到 Django 默认小火箭页面

**预期输出：**

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 25, 2026 - 06:03:51
Django version 5.2.1, using settings 'day01site.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

浏览器访问 `http://<服务器IP>:8000/` 显示：
- 绿色小火箭图标
- "The install worked successfully! Congratulations!"

## 运行步骤

```bash
# 1. 创建虚拟环境（放在 /tmp 下，与 netdevops 目录完全隔离）
python3.12 -m venv /tmp/.venv_django

# 2. 激活虚拟环境
source /tmp/.venv_django/bin/activate

# 3. 安装 Django 5.2.1
pip install Django==5.2.1

# 4. 进入作业目录
cd /netdevops/homework/5.Django/DAY1/

# 5. 创建 Django 项目
django-admin startproject day01site

# 6. 进入项目目录并启动开发服务器
cd day01site
python manage.py runserver 0.0.0.0:8000

# 7. 浏览器访问 http://10.10.1.205:8000/ 查看小火箭页面
```

## 知识点

- Python 3.12 虚拟环境创建（`python3.12 -m venv`）
- Django 固定版本安装（`pip install Django==5.2.1`）
- `django-admin startproject` 项目脚手架
- Django 开发服务器（`runserver`）
- Django 项目默认目录结构（settings/urls/wsgi/asgi）
- `ALLOWED_HOSTS` 配置（生产环境需设置）
- 未应用 migrations 的提示信息（不影响小火箭页面显示）

## 截图清单

1. 终端启动成功截图（显示 `Starting development server at http://0.0.0.0:8000/`）
2. 浏览器小火箭页面截图（显示 "The install worked successfully!"）

## 提交文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `day01site/manage.py` | Python | Django 项目管理脚本 |
| `day01site/day01site/settings.py` | Python | 项目配置文件 |
| `day01site/day01site/urls.py` | Python | URL 路由配置 |
| `day01site/day01site/wsgi.py` | Python | WSGI 入口 |
| `day01site/day01site/asgi.py` | Python | ASGI 入口 |
| `README.md` | 文档 | 本文档 |
