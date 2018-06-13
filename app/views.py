from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from common import tools as common_tools, results as common_results, models as common_models
from . import forms, models
import json
import time

# Create your views here.


@login_required
def myFriends(request):
    """
    my friends
    """
    user = auth.get_user(request)
    name = request.GET.get('name')
    sex = request.GET.get('sex')
    kwargs = {}
    if name is not None and name != '':
        kwargs['name__icontains'] = name
    if sex is not None and sex != '' and sex != '3':
        kwargs['sex'] = sex
    kwargs['user'] = user
    kwargs['status'] = 1
    friends_list_all = models.Friend.objects.filter(**kwargs).all().order_by('-create_time')
    friends_count = friends_list_all.count()
    paginator = Paginator(friends_list_all, 10)
    page = request.GET.get('page')
    try:
        friends_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        friends_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        friends_list = paginator.page(paginator.num_pages)
    return render(request, 'remember/friends-list.html', {
        'friends_count': friends_count,
        'name': name,
        'sex': sex,
        'friends_list': friends_list,
    })


@login_required
def selectShare(request):
    """
    share page
    """
    return render(request, 'remember/share.html')


@login_required
def shareChain(request):
    """
    chain share
    """
    user_id = auth.get_user(request).id
    msg_base64 = common_tools.b64en_today(user_id=user_id, tp='1')
    return render(request, 'remember/chain.html', {'msg': msg_base64})


@login_required
def shareQRcode(request):
    """
    QRcode share
    """
    user = auth.get_user(request)
    user_id = user.id
    msg_base64 = common_tools.b64en_today(user_id=user_id, tp='2')
    data = 'http://' + request.get_host() + '/share/' + msg_base64
    img_list = common_models.UserHeadPhoto.objects.filter(user=user, status=1)
    img = 'static/image/logo-m.png'
    if img_list:
        img = img_list[0].head_portrait
    img_url = common_tools.makeQRcodeInURL(data, user.username, img)

    return render(request, 'remember/qrcode.html', {'msg': img_url})


def share(request, share_link, share_user_id):
    """
    填写remember页面
    """
    user = User.objects.filter(id=share_user_id)[0]
    if user:
        return render(request, 'remember/share-save.html', {
            'link': share_link,
            'first_name': user.first_name
        })
    else:
        pass
    return render(request, 'error/404.html')


def shareSave(request, share_link):
    """
    好友提交remember
    """
    if request.method == 'POST':
        plaintext = common_tools.b64de_today(share_link)
        share_user_id = plaintext.get('share_user_id')
        share_time = plaintext.get('share_time')
        user = User.objects.filter(id=share_user_id)[0]
        if time.strftime('%F') == share_time and user:
            return_context = {}
            form = forms.ShareSaveForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                friend = models.Friend(user=user,
                                       name=form.cleaned_data['form_name_value'],
                                       sex=form.cleaned_data['form_sex_value'],
                                       birthday=form.cleaned_data['form_birthday_value'],
                                       phone=form.cleaned_data['form_phone_value'],
                                       old_address=form.cleaned_data['form_old_address_value'],
                                       new_address=form.cleaned_data['form_new_address_value'],
                                       origin=form.cleaned_data['form_origin_value'],)
                friend.save()
                for i in range(1, 5):
                    if form.cleaned_data['form_photo_value_' + str(i)]:
                        photo = models.FriendPhoto(friend=friend, photo_img=form.cleaned_data['form_photo_value_' + str(i)],
                                                   photo_description=form.cleaned_data['form_photo_description_' + str(i)])
                        photo.save()
                return_context = common_results.returnCode(109)
            else:
                error_json_str = form.errors.as_json()
                json_obj = json.loads(error_json_str)
                context = common_results.returnCode(108)
                return_context = dict(context, **json_obj)
            return HttpResponse(json.dumps(return_context), content_type="application/json")
        else:
            return HttpResponse(json.dumps(common_results.returnCode(111)), content_type="application/json")
    else:
        pass
    return render(request, 'error/404.html')


@login_required
def quasiFriends(request):
    """
    query quasi friends
    """
    user = auth.get_user(request)
    friends_list = models.Friend.objects.filter(user=user, status=2).all().order_by('-create_time')
    return render(request, 'remember/quasi-friends.html', {
        'friends_list': friends_list,
    })


@login_required
def quasiOperating(request):
    """
    quasi friends operating
    type 1: 通过
         2: 拒绝
    values: friend id
    """
    user = auth.get_user(request)
    if request.method == 'POST':
        req = json.loads(request.body)
        type = req['type']
        values = req['value']
        context = {}
        if type == 1:
            for v in values:
                try:
                    friend = models.Friend.objects.get(user=user, id=v, status=2)
                    if friend:
                        friend.status = 1
                        friend.save()
                    else:
                        pass
                except models.Friend.DoesNotExist:
                    pass
            context = common_results.returnCode(112)
        elif type == 2:
            for v in values:
                try:
                    friend = models.Friend.objects.get(user=user, id=v, status=2)
                    if friend:
                        friend.status = 4
                        friend.save()
                    else:
                        pass
                except models.Friend.DoesNotExist:
                    pass
            context = common_results.returnCode(113)
        else:
            context = common_results.returnCode(114)
    else:
        raise Http404()
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def friendInfo(request, fid):
    """
    a friend information
    """
    user = auth.get_user(request)
    friend = models.Friend.objects.filter(user=user).get(id=fid)
    return render(request, 'remember/friend-info.html', {
        'friend': friend,
    })
