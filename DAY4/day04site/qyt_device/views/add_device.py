from django.shortcuts import render
from qyt_device.models import Devicedb, Devicetype
from qyt_device.forms.qyt_device_form_add_device import AddDeviceForm
from django.http import HttpResponseRedirect


def add_device(request):
    if request.method == 'POST':
        # 没有登录
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login?next=/add_device')
        # 登录但是没有权限
        elif not request.session.get('device_permission') and request.user.is_authenticated:
            return render(request, 'qyt_device_deny.html', {'errormessage': '你无权访问此页面'})

        form = AddDeviceForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把新添加的设备写入数据库
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
        # 没有登录
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login?next=/add_device')
        # 登录但是没有权限
        elif not request.session.get('device_permission') and request.user.is_authenticated:
            return render(request, 'qyt_device_deny.html', {'errormessage': '你无权访问此页面'})
        form = AddDeviceForm()
        return render(request, 'qyt_device_add_device.html', {'form': form})
