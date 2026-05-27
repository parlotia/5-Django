"""
查询打印代码 - 验证 __str__ 格式化和外键关联是否正确
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day03site.settings')
django.setup()

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
