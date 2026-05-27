"""
插入测试数据脚本
使用两台实验路由器: R1(10.10.1.101) / R2(10.10.1.102)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day03site.settings')
django.setup()

from qyt_device.models import Devicetype, SNMPtype, DeviceSNMP, Devicedb, Devicecpu

# ── 1. 插入设备类型 ──────────────────────────────────────────
router = Devicetype.objects.create(name='Router')
switch = Devicetype.objects.create(name='Switch')
print(f'已创建设备类型: {router}')
print(f'已创建设备类型: {switch}')

# ── 2. 插入 SNMP 类型 ─────────────────────────────────────────
cpu_type = SNMPtype.objects.create(name='CPU利用率')
mem_type = SNMPtype.objects.create(name='内存利用率')
print(f'已创建SNMP类型: {cpu_type}')
print(f'已创建SNMP类型: {mem_type}')

# ── 3. 插入 DeviceSNMP（设备类型 + SNMP类型 + OID 的对应关系）──
snmp1 = DeviceSNMP.objects.create(
    device_type=router,
    snmp_type=cpu_type,
    oid='1.3.6.1.4.1.9.2.1.58.0',
)
snmp2 = DeviceSNMP.objects.create(
    device_type=router,
    snmp_type=mem_type,
    oid='1.3.6.1.4.1.9.9.48.1.1.1.6.1',
)
print(f'已创建DeviceSNMP: {snmp1}')
print(f'已创建DeviceSNMP: {snmp2}')

# ── 4. 插入设备（两台实验路由器）─────────────────────────────────
r1 = Devicedb.objects.create(
    name='R1',
    ip='10.10.1.101',
    description='实验路由器1',
    type=router,
    snmp_ro_community='public',
    snmp_rw_community='private',
    ssh_username='admin',
    ssh_password='Cisc0123',
    enable_password='',
)
r2 = Devicedb.objects.create(
    name='R2',
    ip='10.10.1.102',
    description='实验路由器2',
    type=router,
    snmp_ro_community='public',
    snmp_rw_community='private',
    ssh_username='admin',
    ssh_password='Cisc0123',
    enable_password='',
)
print(f'已创建设备: {r1}')
print(f'已创建设备: {r2}')

# ── 5. 插入 CPU 利用率记录 ────────────────────────────────────
cpu1 = Devicecpu.objects.create(device=r1, cpu_usage=30.0)
cpu2 = Devicecpu.objects.create(device=r1, cpu_usage=45.5)
cpu3 = Devicecpu.objects.create(device=r2, cpu_usage=22.0)
print(f'已创建CPU记录: {cpu1}')
print(f'已创建CPU记录: {cpu2}')
print(f'已创建CPU记录: {cpu3}')

print('\n>>> 所有测试数据插入完成！')
