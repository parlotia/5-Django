from django import forms
from qyt_device.models import Devicetype, Devicedb


class AddDeviceForm(forms.Form):
    required_css_class = 'required'

    # 设备名称
    name = forms.CharField(max_length=50,
                           min_length=2,
                           label='设备名称',
                           required=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    # IP地址
    ip = forms.GenericIPAddressField(label='IP地址',
                                     required=True,
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    # 设备描述信息
    description = forms.CharField(label='描述',
                                  required=False,
                                  widget=forms.Textarea(attrs={"class": "form-control"}))
    # SNMP只读Community
    snmp_ro_community = forms.CharField(label='SNMP只读Community',
                                        required=True,
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    # SNMP读写Community
    snmp_rw_community = forms.CharField(label='SNMP读写Community',
                                        required=False,
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    # SSH用户名
    ssh_username = forms.CharField(max_length=50,
                                   min_length=2,
                                   label='SSH用户名',
                                   required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    # SSH密码
    ssh_password = forms.CharField(max_length=50,
                                   min_length=2,
                                   label='SSH密码',
                                   required=False,
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    # enable密码
    enable_password = forms.CharField(max_length=50,
                                      min_length=2,
                                      label='Enable密码',
                                      required=False,
                                      widget=forms.PasswordInput(attrs={"class": "form-control"}))
    # 设备类型
    type = forms.ModelChoiceField(
        queryset=Devicetype.objects.all(),
        label='设备类型',
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label='请选择设备类型',
    )

    def clean_ip(self):
        ip_address = self.cleaned_data['ip']
        existing = Devicedb.objects.filter(ip=ip_address).exists()
        if existing:
            raise forms.ValidationError("IP地址已经存在")
        return ip_address

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('ssh_password')
        username = cleaned_data.get('ssh_username')
        if bool(password) ^ bool(username):
            raise forms.ValidationError("用户名和密码需要同时填写")
        return cleaned_data
