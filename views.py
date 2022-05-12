from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from .import sendEmailConfirm
from django.conf import settings
# Create your views here.


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/templates/index.html')


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

            if not user.has_confirmed: # 邮件确认_是否已确认
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/templates/login.html', locals())

            if user.password == hash_code(password): # 密码加密相关
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/templates/login.html', locals())
        else:
            return render(request, 'login/templates/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/templates/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/templates/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/templates/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/templates/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1) # 密码加密
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                code = make_confirm_string(new_user) # 邮箱确认
                sendEmailConfirm.send_email_confirm(email, code) # 邮箱确认

                message = '请前往邮箱进行确认！' # 邮箱确认
                return render(request, 'login/templates/confirm.html', locals())
                # return redirect('/login/')
        else:
            return render(request, 'login/templates/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/templates/register.html', locals())


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


# 用户名密码加密
# import hashlib 引用挪到前面了
def hash_code(s, salt='mysite'):# hash加密
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# 邮件确认相关
# 首先利用datetime模块生成一个当前时间的字符串now，
# 再调用前面编写的hash_code()以用户名为基础，now为‘盐’，生成一个独一无二的哈希值，再调用
def make_confirm_string(user):  # 邮件确认相关
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 邮件确认相关
    code = hash_code(user.name, now)  # 邮件确认相关

    #ConfirmString模型的create()方法，生成并保存一个确认码对象。最后返回这个哈希值
    models.ConfirmString.objects.create(code=code, user=user, )  # 邮件确认相关
    return code  # 邮件确认相关
# 邮件确认相关
# 邮件确认相关
def user_confirm(request):
    # 从请求的url地址中获取确认码;
    code = request.GET.get('code', None)
    message = ''
    try:
        # 先去数据库内查询是否有对应的确认码;
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        # 如果没有，返回confirm.html页面，并提示;
        message = '无效的确认请求!'
        return render(request, 'login/templates/confirm.html', locals())
    # 如果有，获取注册的时间c_time，加上设置的过期天数，这里是7天，然后与现在时间点进行对比；
    c_time = confirm.c_time
    now = datetime.datetime.now()
    # 如果时间已经超期，删除注册的用户，同时注册码也会一并删除
    # 然后返回confirm.html页面，并提示;
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/templates/confirm.html', locals())
    else:
        # 如果未超期，修改用户的has_confirmed字段为True，并保存，表示通过确认了。
        # 然后删除注册码，但不删除用户本身。最后返回confirm.html页面，并提示。
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/templates/confirm.html', locals())
