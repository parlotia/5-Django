# Django DAY2 — 最基本模板练习

## 作业背景

使用 Django 模板引擎实现 Bootstrap 5.3 页面框架，掌握模板继承（`base.html` + 业务页面），正确配置和显示静态图片，在模板中完成变量替换，理解并打通 `urls.py`、view、template 三者关系。

## 实验环境

| 组件 | 版本/地址 |
|------|-----------|
| Linux 服务器 | 10.10.1.205 (Rocky Linux 9.7) |
| Python | 3.12.12 |
| Django | 5.2.1 |
| Bootstrap | 5.3（本地静态文件） |
| 开发服务器 | http://0.0.0.0:8000 |
| 虚拟环境路径 | `/tmp/.venv_django`（独立于项目目录，不随项目提交） |

## 项目结构

```
DAY2/
└── day02site/
    ├── manage.py               # Django 管理脚本
    ├── day02site/
    │   ├── __init__.py         # 包标识
    │   ├── settings.py         # 项目配置（模板目录 + 静态文件目录）
    │   ├── urls.py             # URL 路由配置
    │   ├── asgi.py             # ASGI 入口
    │   └── wsgi.py             # WSGI 入口
    ├── templates/
    │   ├── base.html           # 基础模板（Bootstrap 5.3 + 导航栏 + 静态图片）
    │   └── index.html          # 业务页面（继承 base.html，变量替换）
    ├── static/
    │   ├── css/
    │   │   └── bootstrap.min.css
    │   ├── js/
    │   │   └── bootstrap.bundle.min.js
    │   └── img/
    │       ├── favicon.ico
    │       ├── logo.jpg
    │       └── logo_long_new.png
    └── views/
        ├── __init__.py
        └── index.py            # 首页视图函数
```

## 关键代码

### urls.py

```python
from django.contrib import admin
from django.urls import path
from views.index import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
]
```

### views/index.py

```python
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'qyt_title': '强化班作业Title',
                                          'qyt_body': '强化班作业Body'})
```

### templates/index.html（模板继承 + 变量替换）

```django
{% extends 'base.html' %}

{% block title %}
    {{ qyt_title }}
{% endblock title %}

{% block body %}
<div class="container-fluid">
    <h1>{{ qyt_body }}</h1>
</div>
{% endblock body %}
```

## 运行步骤

```bash
# 1. 激活虚拟环境
source /tmp/.venv_django/bin/activate

# 2. 进入项目目录
cd /netdevops/homework/5.Django/DAY2/day02site

# 3. 启动开发服务器
python manage.py runserver 0.0.0.0:8000

# 4. 浏览器访问 http://10.10.1.205:8000/ 查看页面
```

## 知识点

- Django 模板引擎（DTL）的继承机制（`extends` / `block`）
- Bootstrap 5.3 本地静态文件引入
- Django 静态文件配置（`STATIC_URL` / `STATICFILES_DIRS`）
- 模板标签 `{% load static %}` 与 `{% static %}`
- 视图函数 `render()` 的 context 参数传递
- URL 路由分发：`urls.py` → view → template 的完整链路

## 提交文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `day02site/day02site/settings.py` | Python | 项目配置（模板 + 静态文件） |
| `day02site/day02site/urls.py` | Python | URL 路由配置 |
| `day02site/views/index.py` | Python | 首页视图函数 |
| `day02site/templates/base.html` | HTML | 基础模板（Bootstrap 5.3 + 导航栏） |
| `day02site/templates/index.html` | HTML | 业务页面模板（变量替换） |
| `day02site/static/` | 目录 | Bootstrap CSS/JS + 图片资源 |
| `README.md` | 文档 | 本文档 |
