# Django DAY4 — 添加网络设备（Django Form）

## 作业背景

基于 DAY3 的数据模型，使用 Django Form 创建"添加网络设备"页面，实现字段渲染、校验、POST 提交写入数据库，以及错误/成功提示。

## 实验环境

| 组件 | 版本/地址 |
|------|-----------|
| Linux 服务器 | Rocky Linux 9.7 |
| Python | 3.9.23 |
| Django | 4.2.30 |
| 数据库 | SQLite3（db.sqlite3） |
| 登录账号 | admin / Cisc0123 |

## 项目结构

```
DAY4/
├── README.md
├── add_device_form.png              # 添加设备页面截图
├── success_message.png              # 添加成功截图
├── admin_devicedb_list.png          # 数据库记录截图
└── day04site/
    ├── manage.py
    ├── db.sqlite3
    ├── static/img/logo_long_new.png # 导航栏 logo
    ├── templates/
    │   ├── base.html                # 基础模板（Bootstrap 5.3 + navbar）
    │   ├── qyt_device_add_device.html   # 添加设备页面
    │   ├── qyt_device_deny.html         # 权限拒绝页面
    │   └── login.html                   # 登录页面
    ├── day04site/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    └── qyt_device/
        ├── models.py                # 数据模型（同 DAY3）
        ├── forms/
        │   └── qyt_device_form_add_device.py  # AddDeviceForm
        ├── views/
        │   ├── add_device.py        # 添加设备视图
        │   └── auth_views.py        # 登录/登出视图
        ├── admin.py
        ├── migrations/
        │   └── 0001_initial.py
        └── apps.py
```

## 核心代码

### Form（qyt_device/forms/qyt_device_form_add_device.py）

```python
from django import forms
from qyt_device.models import Devicetype, Devicedb


class AddDeviceForm(forms.Form):
    required_css_class = 'required'

    name = forms.CharField(max_length=50, min_length=2, label='设备名称', required=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    ip = forms.GenericIPAddressField(label='IP地址', required=True,
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label='描述', required=False,
                                  widget=forms.Textarea(attrs={"class": "form-control"}))
    snmp_ro_community = forms.CharField(label='SNMP只读Community', required=True,
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    snmp_rw_community = forms.CharField(label='SNMP读写Community', required=False,
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    ssh_username = forms.CharField(max_length=50, min_length=2, label='SSH用户名', required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    ssh_password = forms.CharField(max_length=50, min_length=2, label='SSH密码', required=False,
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    enable_password = forms.CharField(max_length=50, min_length=2, label='Enable密码', required=False,
                                      widget=forms.PasswordInput(attrs={"class": "form-control"}))
    type = forms.ModelChoiceField(queryset=Devicetype.objects.all(), label='设备类型',
                                  widget=forms.Select(attrs={"class": "form-control"}),
                                  empty_label='请选择设备类型')

    def clean_ip(self):
        ip_address = self.cleaned_data['ip']
        if Devicedb.objects.filter(ip=ip_address).exists():
            raise forms.ValidationError("IP地址已经存在")
        return ip_address

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('ssh_password')
        username = cleaned_data.get('ssh_username')
        if bool(password) ^ bool(username):
            raise forms.ValidationError("用户名和密码需要同时填写")
        return cleaned_data
```

### View（qyt_device/views/add_device.py）

```python
from django.shortcuts import render
from qyt_device.models import Devicedb, Devicetype
from qyt_device.forms.qyt_device_form_add_device import AddDeviceForm
from django.http import HttpResponseRedirect


def add_device(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login?next=/add_device')
        elif not request.session.get('device_permission') and request.user.is_authenticated:
            return render(request, 'qyt_device_deny.html', {'errormessage': '你无权访问此页面'})

        form = AddDeviceForm(request.POST)
        if form.is_valid():
            try:
                d1 = Devicedb(name=request.POST.get('name'),
                              ip=request.POST.get('ip'),
                              description=request.POST.get('description'),
                              type=form.cleaned_data['type'],
                              snmp_ro_community=request.POST.get('snmp_ro_community'),
                              snmp_rw_community=request.POST.get('snmp_rw_community'),
                              ssh_username=request.POST.get('ssh_username'),
                              ssh_password=request.POST.get('ssh_password'),
                              enable_password=request.POST.get('enable_password'))
                d1.save()
            except Devicetype.DoesNotExist:
                return render(request, 'qyt_device_add_device.html', {'form': form,
                                                                      'errormessage': '设备类型没有找到'})
            form = AddDeviceForm()
            return render(request, 'qyt_device_add_device.html', {'form': form,
                                                                  'successmessage': '设备添加成功'})
        else:
            return render(request, 'qyt_device_add_device.html', {'form': form})
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login?next=/add_device')
        elif not request.session.get('device_permission') and request.user.is_authenticated:
            return render(request, 'qyt_device_deny.html', {'errormessage': '你无权访问此页面'})
        form = AddDeviceForm()
        return render(request, 'qyt_device_add_device.html', {'form': form})
```

### HTML 模板（templates/qyt_device_add_device.html）

```html
{% extends "base.html" %}

{% block title %}添加网络设备{% endblock title %}

{% block body %}
<div class="row justify-content-center">
  <div class="col-md-8">
    <h2 class="mb-4">添加网络设备</h2>

    {% if successmessage %}
    <div class="alert alert-success alert-dismissible fade show" role="alert">
      {{ successmessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endif %}

    {% if form.non_field_errors %}
    <div class="alert alert-danger">
      {% for error in form.non_field_errors %}
      <p>{{ error }}</p>
      {% endfor %}
    </div>
    {% endif %}

    <form method="post" action="/add_device">
      {% csrf_token %}
      {% for field in form %}
      <div class="mb-3">
        <label for="{{ field.id_for_label }}" class="form-label">
          {% if field.field.required %}<span class="text-danger">*</span>{% endif %}{{ field.label }}:
        </label>
        {{ field }}
        {% if field.errors %}
        <div class="text-danger small mt-1">
          {% for error in field.errors %}<p class="mb-0">{{ error }}</p>{% endfor %}
        </div>
        {% endif %}
      </div>
      {% endfor %}
      <button type="submit" class="btn btn-success">提交</button>
    </form>
  </div>
</div>
{% endblock body %}
```

## 效果截图

### 1. 添加设备页面

![添加设备表单](add_device_form.png)

### 2. 添加成功提示

![设备添加成功](success_message.png)

### 3. 数据库新增记录

![Admin数据库记录](admin_devicedb_list.png)

## 启动与使用

```bash
cd /netdevops/homework/5.Django/DAY4/day04site
source /netdevops/.venv/bin/activate
python3 manage.py runserver 0.0.0.0:8000
```

- 访问地址：`http://<服务器IP>:8000/add_device`
- 登录账号：`admin` / `Cisc0123`

## 知识点

- Django Form 字段定义与 widget 自定义样式
- `clean_<field>` 单字段校验（IP 唯一性检查）
- `clean()` 全局校验（用户名密码联合检查）
- `ModelChoiceField` 关联外键下拉选择
- session 权限控制与登录重定向
- 模板继承（base.html → 子模板）
- Bootstrap 5.3 表单样式与响应式布局
