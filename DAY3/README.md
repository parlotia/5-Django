# Django DAY3 — 数据库外键设计与数据查询

## 作业背景

基于 Django ORM 设计多表外键关系，创建设备管理相关的 5 个数据模型（`Devicetype`、`SNMPtype`、`DeviceSNMP`、`Devicedb`、`Devicecpu`），完成 `makemigrations` / `migrate`，插入真实实验设备数据，并通过查询打印验证 `__str__` 格式化与外键关联是否正确。

## 实验环境

| 组件 | 版本/地址 |
|------|-----------|
| Linux 服务器 | Rocky Linux 9.7 |
| Python | 3.12 |
| Django | 4.2.30 |
| 数据库 | SQLite3（db.sqlite3） |
| 实验路由器1 | R1 — 10.10.1.101（admin/Cisc0123） |
| 实验路由器2 | R2 — 10.10.1.102（admin/Cisc0123） |

## 项目结构

```
DAY3/
└── day03site/
    ├── manage.py                  # Django 管理脚本
    ├── db.sqlite3                 # SQLite 数据库
    ├── insert_data.py             # 插入测试数据脚本
    ├── query_print.py             # 查询打印验证脚本
    ├── query_output.txt           # 查询打印输出结果
    ├── day03site/
    │   ├── settings.py            # 项目配置（注册 qyt_device）
    │   ├── urls.py                # URL 路由
    │   ├── asgi.py
    │   └── wsgi.py
    └── qyt_device/
        ├── models.py              # 5 个数据模型（含外键 + __str__）
        ├── migrations/
        │   └── 0001_initial.py    # 自动生成的迁移文件
        ├── admin.py
        ├── apps.py
        └── tests.py
```

## 数据库模型（models.py）

```python
from django.db import models


class Devicetype(models.Model):
    # 设备类型名称
    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='设备类型名称')
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.__class__.__name__}( 设备类型: {self.name} )"


class SNMPtype(models.Model):
    # SNMP类型名称
    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='SNMP类型名称')
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.__class__.__name__}( SNMP类型: {self.name} )"


class DeviceSNMP(models.Model):
    # 设备类型
    device_type = models.ForeignKey(Devicetype,
                                    related_name='devicesnmp',
                                    on_delete=models.CASCADE,
                                    verbose_name='设备类型'
                                    )
    # SNMP类型
    snmp_type = models.ForeignKey(SNMPtype,
                                  related_name='devicesnmp',
                                  on_delete=models.CASCADE,
                                  verbose_name='SNMP类型'
                                  )
    # oid
    oid = models.CharField(max_length=999, verbose_name='oid')
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return (f"{self.__class__.__name__}( 设备类型: {self.device_type.name} "
                f"| SNMP类型: {self.snmp_type.name} "
                f"| OID: {self.oid} )")


class Devicedb(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, unique=True, blank=False, verbose_name='设备名称')
    # 设备IP地址
    ip = models.GenericIPAddressField(default='1.1.1.1', unique=True, verbose_name='IP地址')
    # 设备描述信息
    description = models.TextField(blank=True, verbose_name='描述')
    # 设备类型
    type = models.ForeignKey(Devicetype, related_name='device', on_delete=models.CASCADE, verbose_name='设备类型')
    # SNMP只读Community
    snmp_ro_community = models.CharField(max_length=999, blank=False, verbose_name='只读SNMP Community')
    # SNMP读写Community
    snmp_rw_community = models.CharField(max_length=999, blank=True, verbose_name='读写SNMP Community')
    # SSH用户名
    ssh_username = models.CharField(max_length=999, blank=False, verbose_name='SSH用户名')
    # SSH密码
    ssh_password = models.CharField(max_length=999, blank=False, verbose_name='SSH密码')
    # 特权密码(ASA必须设置)
    enable_password = models.CharField(max_length=999, blank=True, verbose_name='Enable密码')
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return (f"{self.__class__.__name__}( 设备名称: {self.name} "
                f"| 设备类型: {self.type.name} "
                f"| IP地址: {self.ip} )")


class Devicecpu(models.Model):
    # 设备
    device = models.ForeignKey(Devicedb,
                               related_name='cpu_usage',
                               on_delete=models.CASCADE,
                               verbose_name='设备',
                               )
    # 当前CPU利用率
    cpu_usage = models.FloatField(default=0, blank=True, verbose_name='当前CPU利用率')
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now_add=True, verbose_name='记录时间')

    def __str__(self):
        return (f"{self.__class__.__name__}( 设备名称: {self.device.name} "
                f"| CPU利用率: {self.cpu_usage} "
                f"| 记录时间: {self.record_datetime.strftime('%Y-%m-%d %H:%M:%S')} )")
```

## 外键关系图

```
Devicetype ──────────────┬──── DeviceSNMP ◄──── SNMPtype
     │                   │
     └──── Devicedb ──── └──── Devicecpu
```

## 执行步骤

### 1. 数据库迁移

```bash
cd /netdevops/homework/5.Django/DAY3/day03site
python3 manage.py makemigrations
python3 manage.py migrate
```

### 2. 插入测试数据

```python
# insert_data.py（执行：python3 insert_data.py）
from qyt_device.models import Devicetype, SNMPtype, DeviceSNMP, Devicedb, Devicecpu

router = Devicetype.objects.create(name='Router')
switch = Devicetype.objects.create(name='Switch')

cpu_type = SNMPtype.objects.create(name='CPU利用率')
mem_type = SNMPtype.objects.create(name='内存利用率')

DeviceSNMP.objects.create(device_type=router, snmp_type=cpu_type, oid='1.3.6.1.4.1.9.2.1.58.0')
DeviceSNMP.objects.create(device_type=router, snmp_type=mem_type, oid='1.3.6.1.4.1.9.9.48.1.1.1.6.1')

r1 = Devicedb.objects.create(
    name='R1', ip='10.10.1.101', description='实验路由器1',
    type=router, snmp_ro_community='public', snmp_rw_community='private',
    ssh_username='admin', ssh_password='Cisc0123', enable_password='',
)
r2 = Devicedb.objects.create(
    name='R2', ip='10.10.1.102', description='实验路由器2',
    type=router, snmp_ro_community='public', snmp_rw_community='private',
    ssh_username='admin', ssh_password='Cisc0123', enable_password='',
)

Devicecpu.objects.create(device=r1, cpu_usage=30.0)
Devicecpu.objects.create(device=r1, cpu_usage=45.5)
Devicecpu.objects.create(device=r2, cpu_usage=22.0)
```

### 3. 查询打印代码

```python
# query_print.py（执行：python3 query_print.py）
from qyt_device.models import Devicedb, DeviceSNMP, Devicecpu

print('Devicedb:')
for device in Devicedb.objects.all():
    print(device)

print('\nDeviceSNMP:')
for snmp in DeviceSNMP.objects.all():
    print(snmp)

print('\nDevicecpu:')
for cpu in Devicecpu.objects.all():
    print(cpu)
```

## Django Shell 查询输出

```
Devicedb:
Devicedb( 设备名称: R1 | 设备类型: Router | IP地址: 10.10.1.101 )
Devicedb( 设备名称: R2 | 设备类型: Router | IP地址: 10.10.1.102 )

DeviceSNMP:
DeviceSNMP( 设备类型: Router | SNMP类型: CPU利用率 | OID: 1.3.6.1.4.1.9.2.1.58.0 )
DeviceSNMP( 设备类型: Router | SNMP类型: 内存利用率 | OID: 1.3.6.1.4.1.9.9.48.1.1.1.6.1 )

Devicecpu:
Devicecpu( 设备名称: R1 | CPU利用率: 30.0 | 记录时间: 2026-05-27 02:08:22 )
Devicecpu( 设备名称: R1 | CPU利用率: 45.5 | 记录时间: 2026-05-27 02:08:22 )
Devicecpu( 设备名称: R2 | CPU利用率: 22.0 | 记录时间: 2026-05-27 02:08:22 )
```

## 知识点

- Django ORM 外键（`ForeignKey`）的 `related_name` 与 `on_delete=CASCADE`
- `auto_now` 与 `auto_now_add` 的区别（修改时间 vs 创建时间）
- `GenericIPAddressField` 用于 IP 地址字段校验
- `__str__` 方法实现对象的自描述字符串
- `makemigrations` 生成迁移文件，`migrate` 同步到数据库

## Django Admin 后台访问

模型已通过 `qyt_device/admin.py` 全部注册到 Django Admin：

```python
from django.contrib import admin
from qyt_device.models import Devicetype, SNMPtype, DeviceSNMP, Devicedb, Devicecpu

admin.site.register(Devicetype)
admin.site.register(SNMPtype)
admin.site.register(DeviceSNMP)
admin.site.register(Devicedb)
admin.site.register(Devicecpu)
```

**启动服务器：**

```bash
cd /netdevops/homework/5.Django/DAY3/day03site
python3 manage.py runserver 0.0.0.0:8000
```

**访问地址：** `http://<服务器IP>:8000/admin/`  
**登录账号：** `admin` / `Cisc0123`

登录后在左侧 **QYT_DEVICE** 分组下可看到所有 5 个数据表的记录列表。

## 提交文件清单

| 文件 | 说明 |
|------|------|
| `day03site/qyt_device/models.py` | 5 个数据模型（含外键 + `__str__`） |
| `day03site/qyt_device/admin.py` | 注册模型到 Django Admin |
| `day03site/qyt_device/migrations/0001_initial.py` | 自动生成的迁移文件 |
| `day03site/day03site/settings.py` | 注册 `qyt_device` 应用 |
| `day03site/insert_data.py` | 插入测试数据脚本 |
| `day03site/query_print.py` | 查询打印验证脚本 |
| `day03site/query_output.txt` | 查询打印输出文本 |
| `README.md` | 本文档 |
