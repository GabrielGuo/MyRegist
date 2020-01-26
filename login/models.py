from django.db import models

# Create your models here.

# 数据模型设计 数据库设计
# 用户表


# 用户名
# 密码
# 邮箱地址
# 性别
# 创建时间
class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)                # 用户名
    password = models.CharField(max_length=256)                         # 密码
    email = models.EmailField(unique=True)                              # 邮箱地址
    sex = models.CharField(max_length=32, choices=gender, default="男")  # 性别
    c_time = models.DateTimeField(auto_now_add=True)                    # 创建账户时间
    has_confirmed = models.BooleanField(default=False)                  # 布尔值，默认为False，也就是未进行邮件注册

    def __str__(self):
        return self.name                    # 帮助人性化显示对象信息

    class Meta:         # 注意，是模型的子类，要缩进！
        # 最近的最先显示
        ordering = ["-c_time"]              # 用于指定该模型生成的所有对象的排序方式，接收一个字段名组成的元组或列表
        verbose_name = "用户"               # 用于设置模型对象的直观、人类可读的名称
        verbose_name_plural = "用户"        # 人类可读的单数或者复数名


# 用邮件确认的方式对新注册用户进行审查
# 既然要区分通过和未通过邮件确认的用户，那么必须给用户添加一个是否进行过邮件确认的属性
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)                         # 保存用户的确认码 code字段是哈希后的注册码
    user = models.OneToOneField('User', on_delete=models.CASCADE)   # 保存了用户和注册码之间的关系，一对一的形式
    c_time = models.DateTimeField(auto_now_add=True)                # 注册提交的时间

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

