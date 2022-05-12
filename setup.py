#encoding=utf-8
# -*-encoding:utf-8 -*-
#encoding=utf-8

"""
# File       : setup.py
# Time       ：2022/5/6 23:54
# Author     ：renyc
# version    ：python 3.10
"""
# 包含了编译和安装app的配置细节。
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-login-register',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='一个通用的用户注册和登录系统',
    long_description=README,
    url='https://www.cnblogs.com/rychh/',
    author='renyc',
    author_email='renyongchenghh@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)