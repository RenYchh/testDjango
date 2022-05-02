from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
# Create your views here.


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):  # session引入不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/templates/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True # seesion相关，往session里写数据
                request.session['user_id'] = user.id # 引入session相关，往session里写数据
                request.session['user_name'] = user.name# 引入session相关，往session写数据
                return redirect('/index/')# 引入session相关
            else:
                message = '密码不正确！'
                return render(request, 'login/templates/login.html', locals())
        else:
            return render(request, 'login/templates/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/templates/login.html', locals())


def register(request):
    pass
    return render(request, 'login/templates/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")