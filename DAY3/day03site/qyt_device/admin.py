from django.contrib import admin
from qyt_device.models import Devicetype, SNMPtype, DeviceSNMP, Devicedb, Devicecpu

admin.site.register(Devicetype)
admin.site.register(SNMPtype)
admin.site.register(DeviceSNMP)
admin.site.register(Devicedb)
admin.site.register(Devicecpu)
