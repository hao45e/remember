from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import models as auth_models
from django.db.models import Q
from . import forms, results, tools, models
from app import views as app_views
from app import models as app_models
import re
import json
import time
import base64
# Create your views here.


@login_required
def index(request):
    """
    index page
    首页
    如果当前用户没有登陆，则跳转到登陆页面
    如果当前用户已经登陆，则将当前登陆用户的用户名返回给首页
    male_count: 好友男性数量
    female_count: 好友女性数量
    friends_map: 好友地区code和该地区好友数量
    """
    user = auth.get_user(request)
    friends_list = app_models.Friend.objects.filter(user=user, status=1).all();
    male_count = friends_list.filter(sex=2).count()
    female_count = friends_list.filter(sex=1).count()
    friends_map = tools.returnVectorMapAddressCode(friends_list)
    return render(request, 'index.html', {
        'male_count': male_count,
        'female_count': female_count,
        'friends_map': friends_map,
    })


class LoginView(FormView):
    """
    this is login view
    """
    def get(self, request, *args, **kwargs):
        """
        get login page
        如果当前用户已经登陆，则跳转到首页
        """
        if auth.get_user(request) != auth_models.AnonymousUser():
            return redirect('index')
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """
        user login
        账号和密码通过HTTP_AUTHORIZATION传递，base64加密，
        密文前添加了个Basic字符串，解密后结构："username:password"
        由于username是不允许出现":"，所以第一个":"之前表示username，之后表示password
        """
        authorization = request.META.get('HTTP_AUTHORIZATION')
        authorization = re.findall('^Basic(.*?)$', authorization, re.S)[0]
        base64byte = base64.b64decode(authorization)
        base64string = bytes.decode(base64byte)
        username = re.findall(r"^(.*?):.*?$", base64string, re.S)[0]
        password = re.findall(r"^.*?:(.*?)$", base64string, re.S)[0]
        if username == '' or password == '':
            context = results.returnCode(103)
        else:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                context = results.returnCode(code=101)
            else:
                context = results.returnCode(code=102)
        return HttpResponse(json.dumps(context), content_type="application/json")


class RegisterView(FormView):
    """
    this is register view
    """
    def get(self, request, *args, **kwargs):
        """
        get register page
        如果当前用户已经登陆，则直接跳转至首页
        """
        if auth.get_user(request) != auth_models.AnonymousUser():
            return redirect('index')
        form = forms.RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """
        user register
        用户注册
        """
        form = forms.RegisterForm(request.POST)
        return_context = {}
        if form.is_valid():
            user_list_set = list(auth_models.User.objects.values_list('username'))
            user_list = []
            for uname in user_list_set:
                user_list.append(uname[0])
            if form.cleaned_data['username'] in user_list:
                return_context = results.returnCode(106)
            else:
                try:
                    user = auth_models.User.objects.create_user(username=form.cleaned_data.get('username'),
                                                                password=form.cleaned_data.get('password1'))
                    user.save()
                    return_context = results.returnCode(105)
                except Exception as e:
                    print('------------------------------')
                    print('save user error:', e.message)
                    print('------------------------------')
                    return_context = results.returnCode(107)
        else:
            error_json_str = form.errors.as_json()
            json_obj = json.loads(error_json_str)
            context = results.returnCode(104)
            return_context = dict(context, **json_obj)
        return HttpResponse(json.dumps(return_context), content_type="application/json")


@login_required
def logout(request):
    """
    user logout
    将用户退出并重定向到登陆页面
    """
    auth.logout(request)
    return redirect('common:login')


def share(request, share_link):
    plaintext = tools.b64de_today(share_link)
    share_user_id = plaintext.get('share_user_id')
    share_time = plaintext.get('share_time')
    share_type = plaintext.get('share_type')
    if time.strftime('%F') == share_time:
        if share_type == '1':
            return app_views.share(request, share_link, share_user_id)
    else:
        return render(request, 'error/share-timeout.html')
    return render(request, 'error/404.html')


def shareSuccess(request):
    """
    好友填完分享页面后跳转的页面
    """
    return render(request, 'remember/share-success.html')


@login_required
def myInfo(request):
    """
    my information
    """
    user = auth.get_user(request)
    return render(request, 'user/my-info.html', {
        'user': user,
    })


class EditMyInfoView(FormView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        return render(request, 'user/edit-my-info.html', {
            'user': user,
        })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)
        form = forms.EditMyInformationForm(request.POST or None, request.FILES or None)
        return_context = {}
        if form.is_valid():
            if form.cleaned_data['head_photo']:
                hd_photo = models.UserHeadPhoto.objects.filter(user=user, status=1).all()
                if hd_photo.count() != 0:
                    for photo in hd_photo:
                        photo.status = 2
                        photo.save()
                user_head_photo = models.UserHeadPhoto(user=user,
                                                       head_portrait=form.cleaned_data['head_photo'],
                                                       status=1)
                user_head_photo.save()
            if form.cleaned_data['name']:
                us = models.User.objects.get(id=user.id)
                if us.first_name != form.cleaned_data['name']:
                    us.first_name = form.cleaned_data['name']
                    us.save()
            return_context = results.returnCode(115)
        else:
            error_json_str = form.errors.as_json()
            json_obj = json.loads(error_json_str)
            context = results.returnCode(116)
            return_context = dict(context, **json_obj)
        return HttpResponse(json.dumps(return_context), content_type="application/json")


class EditMyPWD(FormView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'user/edit-my-password.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)
        form = forms.EditMyPWDForm(request.POST)
        return_context = {}
        if form.is_valid():
            old_pwd = form.cleaned_data['old_pwd']
            new_pwd = form.cleaned_data['new_pwd']
            if user.check_password(old_pwd):
                user.set_password(new_pwd)
                user.save()
                return_context = results.returnCode(119)
            else:
                return_context = results.returnCode(118)
        else:
            error_json_str = form.errors.as_json()
            json_obj = json.loads(error_json_str)
            context = results.returnCode(117)
            return_context = dict(context, **json_obj)
        return HttpResponse(json.dumps(return_context), content_type="application/json")


def search(request):
    user = auth.get_user(request)
    if request.method == 'GET':
        find = request.GET.get('q')
        friends_list = app_models.Friend.objects.filter(Q(user=user), Q(name__icontains=find), Q(status=1))
        quasi_friends_list = app_models.Friend.objects.filter(Q(user=user), Q(name__icontains=find), Q(status=2))
        return render(request, 'pub/search.html', {
            'friends_list': friends_list,
            'quasi_friends_list': quasi_friends_list,
            'search': find,
        })
    else:
        return render(request, '404.html')
