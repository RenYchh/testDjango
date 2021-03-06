# -*-coding:utf-8 -*-

"""
# File       : sendEmailConfirm.py
# Time       ：2022/5/4 19:02
# Author     ：renyc
# version    ：python 3
"""

from django.conf import settings

def send_email_confirm(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.renyongchenghh.com的注册确认邮件'

    text_content = '''感谢注册https://www.cnblogs.com/rychh/，这里是renyc的博客,专注于Python、Django和学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirmstring/?code={}" target=blank>http://127.0.0.1:8000/admin/login/</a>，\
                    这里是renyc的博客，专注于Python、Django和学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()