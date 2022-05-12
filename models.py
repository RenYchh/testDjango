from django.db import models

# Create your models here.

class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False) # 邮件确认相关User模型新增了has_confirmed字段，这是个布尔值，默认为False，也就是未进行邮件注册


    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class ConfirmString(models.Model): # 邮件确认相关
    # code字段是哈希后的注册码；
    code = models.CharField(max_length=256) # 邮件确认相关
    # user是关联的一对一用户；
    user = models.OneToOneField('User', on_delete=models.CASCADE) # 邮件确认相关
    # c_time是注册的提交时间。
    c_time = models.DateTimeField(auto_now_add=True) # 邮件确认相关

    def __str__(self): # 邮件确认相关
        # ConfirmString模型保存了用户和注册码之间的关系，一对一的形式
        return self.user.name + ":   " + self.code # 邮件确认相关

    class Meta: # 邮件确认相关

        ordering = ["-c_time"] # 邮件确认相关
        verbose_name = "确认码" # 邮件确认相关
        verbose_name_plural = "确认码" # 邮件确认相关