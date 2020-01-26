import datetime
import hashlib

from django.shortcuts import render, redirect
from django.utils import timezone

from login import models, forms

# Create your views here.


# 密码加密 使用哈希值的方式加密密码，可能安全等级不够高，但足够简单，方便使用
def hash_code(s, salt='MyRegedit'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


# 创建确认码对象的方法 接收一个用户对象作为参数
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")     # 利用datetime模块生成一个当前时间的字符串now
    code = hash_code(user.name, now)        # 再调用我们前面编写的hash_code()方法以用户名为基础,now为‘盐’，生成一个独一无二的哈希值
    models.ConfirmString.objects.create(code=code, user=user,)  # 调用ConfirmString模型的create()方法，生成并保存一个确认码对象
    return code

from django.conf import settings


# 发送邮件
def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'

    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# 主页
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


# # 登录
# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         message = '请检查填写的内容！'
#         # 确保用户名和密码不能为空
#         if username.strip() and password:  # 确保用户名和密码都不为空
#             # 用户名字符合法性验证
#             # 密码长度验证
#             # 更多的其它验证.....
#             try:        # 使用try异常机制，防止数据库查询失败的异常
#                 user = models.User.objects.get(name=username)
#             except:
#                 message = '用户不存在！'
#                 return render(request, 'login/login.html', {'message':message})
#             if user.password == password:
#                 print(username, password)
#                 return redirect('/index/')
#             else:
#                 message = "密码不正确"
#                 return render(request, 'login/login.html', {'message': message})
#     return render(request, 'login/login.html', {'message': message})


def login(request):
    if request.session.get('is_login', None):       # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':        # 对于POST方法，接收表单数据，并验证；
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():       # 使用表单类自带的is_valid()方法一步完成数据验证工作；
            # 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值；
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            # 进行邮箱验证
            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):    # 解密
                # 往session字典内写入用户状态和数据
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    # 如果验证不通过，则返回一个包含先前数据的表单给前端页面，方便用户修改。
    # 也就是说，它会帮你保留先前填写的数据内容，而不是返回一个空表！
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


# 注册
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

            # 两次输入的密码必须相同
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                # 不能存在相同用户名和邮箱
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                # 利用ORM的API，创建一个用户实例，然后保存到数据库内
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)        # hash加密
                # new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


# 登出
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，就没有登出一说
        return redirect("/login/")      # 重定向到登录界面

    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    request.session.flush()
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


# 邮箱验证码确认界面
def user_confirm(request):
    code = request.GET.get('code', None)            # 从请求的url地址中获取确认码;
    message = ''
    # 先去数据库内查询是否有对应的确认码;
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        # 如果没有，返回confirm.html页面，并提示;
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    # 获取注册的时间c_time，加上设置的过期天数，这里是7天，然后与现在时间点进行对比；
    c_time = confirm.c_time
    # now = datetime.datetime.now()
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        # 时间已经超期，删除注册的用户，同时注册码也会一并删除，然后返回confirm.html页面，并提示;
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:
        # 未超期，修改用户的has_confirmed字段为True，并保存，表示通过确认了。
        # 然后删除注册码，但不删除用户本身。最后返回confirm.html页面，并提示
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


