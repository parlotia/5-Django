from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    """用户登录视图，登录成功后设置session权限"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 设置设备管理权限session
            request.session['device_permission'] = True
            # 跳转到next参数指定的页面，默认跳转到添加设备页面
            next_url = request.GET.get('next', '/add_device')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'errormessage': '用户名或密码错误'})
    else:
        return render(request, 'login.html')


def user_logout(request):
    """用户登出"""
    logout(request)
    return redirect('/accounts/login')
