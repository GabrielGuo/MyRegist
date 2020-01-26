# python 3.6
# -*- coding: utf-8 -*-
# @Time    : 2020-01-26 18:00
# @Author  : 乐天派逗逗
# @Site    : Windows 10
# @File    : form.py
# @Software: PyCharm
# @Contact : 1584838420@qq.com
# @Features: 表单模型
from captcha.fields import CaptchaField
from django import forms


# 登录表单
class UserForm(forms.Form):
    # 每个表单字段都有自己的字段类型比如CharField，它们分别对应一种HTML语言中<form>内的一个input元素。
    # 这一点和Django模型系统的设计非常相似。
    # max_length限制字段输入的最大长度。它同时起到两个作用，
    # 一是在浏览器页面限制用户输入不可超过字符数，
    # 二是在后端服务器验证用户输入的长度也不可超过。
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Username",
            'autofocus': ''}))  # 在form类里添加attr属性
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Password"}))

    captcha = CaptchaField(label='验证码')


# 注册表单
class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

