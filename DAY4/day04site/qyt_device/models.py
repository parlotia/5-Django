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
