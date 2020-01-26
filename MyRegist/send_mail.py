# python 3.6
# -*- coding: utf-8 -*-
# @Time    : 2020-01-26 20:51
# @Author  : 乐天派逗逗
# @Site    : Windows 10
# @File    : send_mail.py
# @Software: PyCharm
# @Contact : 1584838420@qq.com
# @Features: 邮件发送系统

import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'MyRegist.settings'   #  必须添加 , 依赖于 Django

if __name__ == '__main__':

    res = send_mail(
        '来自www.liujiangblog.com的测试邮件',
        '欢迎访问www.cnblogs.com/shiwei1930，这里是SUOSUO博客站点，本站专注于Python、Django技术的分享！',
        '1584838420@qq.com',
        ['1584838420@qq.com'],        # target email@aliyun.com
    )
    print('res=', res)   # 成功 返回  1

# 对于send_mail方法，
#    第一个参数是邮件主题subject；
#    第二个参数是邮件具体内容；
#    第三个参数是邮件发送方，
#    第四个参数是接受方的邮件地址列表, 需要和你settings中的一致；

