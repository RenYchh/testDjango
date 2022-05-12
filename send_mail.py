# -*-coding:utf-8 -*-

"""
# File       : send_mail.py
# Time       ：2022/5/4 16:25
# Author     ：renyc
# version    ：python 3
"""

import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = "DjangoRenyc.settings"
#E:\\DjangoRenyc

if __name__ == '__main__':
    send_mail(
        '来自www.cnblogs.com/rychh/的测试邮件',
        '欢迎访问www.cnblogs.com/rychh/，这里是renyc的博客,欢迎交流学习！',
        'renyongchenghh@163.com',
        ['756271310@qq.com'],
    )


# import os
#
# for i, v in enumerate(os.environ.items(), 1):
#     print(i, v)