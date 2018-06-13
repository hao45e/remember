# -*-coding:utf-8-*-
from django import forms
from django.contrib.auth.models import User
from common import final
import re
import datetime


class LoginForm(forms.Form):
    """
    login form
    [username, password]
    """
    class Meta:
        model = User
        fields = ('username', 'password')
    username = forms.CharField(max_length=20, label='账号', required=True, widget=forms.TextInput)
    password = forms.CharField(max_length=50, label='密码', required=True, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """
    register form
    [username, password1, password2, invite, terms]
    (clean_username, clean_password2, clean_invite, clean_terms)
    """
    class Meta:
        model = User
        fields = ('username', 'password')
    username = forms.CharField(min_length=6, max_length=20, label='账号', required=True, widget=forms.TextInput,
                               help_text='6~20个字符, 可使用字母、数字、下划线', error_messages={
                                'required': '账号是必填项',
                                'min_length': '账号最短6个字符',
                                'max_length': '账号最长20个字符',
        })
    password1 = forms.CharField(min_length=8, max_length=16, label='密码', required=True, widget=forms.PasswordInput,
                                help_text='8~16个字符, 区分大小写', error_messages={
                                'required': '密码是必填项',
                                'min_length': '密码最短8个字符',
                                'max_length': '密码最长16个字符',
        })
    password2 = forms.CharField(min_length=8, max_length=50, label='确认密码', required=True, widget=forms.PasswordInput,
                                help_text='请再次填写密码', error_messages={'required': '请输入确认密码'})
    invite = forms.CharField(label='邀请码', required=True, widget=forms.TextInput, help_text='填写邀请码',
                             error_messages={'required': '邀请码是必填项'})
    terms = forms.BooleanField(widget=forms.CheckboxInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_check = re.findall('^\w*?$', username, re.S)
        if username_check:
            pass
        else:
            raise forms.ValidationError('账号只能有字母数字和下划线')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次密码不一致')
        return password2

    def clean_invite(self):
        invite = self.cleaned_data.get('invite')
        now_time = datetime.datetime.now()
        success_invite = now_time.year + now_time.month + now_time.day + now_time.hour
        if invite == str(success_invite) or invite == str(success_invite + 1):
            pass
        else:
            raise forms.ValidationError('邀请码错误')
        return invite

    def clean_terms(self):
        terms = self.cleaned_data.get('terms')
        if terms:
            pass
        else:
            raise forms.ValidationError('请同意服务条款')
        return terms


class EditMyInformationForm(forms.Form):
    """
    edit my information form
    """
    head_photo = forms.ImageField(required=False)
    name = forms.CharField(max_length=50, min_length=1, required=True)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.search(u'^[a-zA-Z0-9\u4e00-\u9fa5]+$', name):
            raise forms.ValidationError('姓名不可乱填哦')
        if name in final.FinalList.DIRTY_LIST:
            raise forms.ValidationError('你的名字很特殊啊')
        return name


class EditMyPWDForm(forms.Form):
    """
    edit my password
    """
    old_pwd = forms.CharField(min_length=8, max_length=16, label='密码', required=True, widget=forms.PasswordInput,
                              help_text='8~16个字符, 区分大小写', error_messages={
            'required': '原密码是必填项',
            'min_length': '原密码最短8个字符',
            'max_length': '原密码最长16个字符',
        })
    new_pwd = forms.CharField(min_length=8, max_length=16, label='密码', required=True, widget=forms.PasswordInput,
                              help_text='8~16个字符, 区分大小写', error_messages={
            'required': '新密码是必填项',
            'min_length': '新密码最短8个字符',
            'max_length': '新密码最长16个字符',
        })
    re_new_pwd = forms.CharField(min_length=8, max_length=16, label='密码', required=True, widget=forms.PasswordInput,
                              help_text='8~16个字符, 区分大小写', error_messages={
            'required': '确认新密码是必填项',
            'min_length': '确认新密码最短8个字符',
            'max_length': '确认新密码最长16个字符',
        })

    def clean_re_new_pwd(self):
        re_new_pwd = self.cleaned_data.get('re_new_pwd')
        new_pwd = self.cleaned_data.get('new_pwd')
        if new_pwd and re_new_pwd and new_pwd != re_new_pwd:
            raise forms.ValidationError('两次新密码不一致')
        return re_new_pwd
