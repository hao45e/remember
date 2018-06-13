# -*-coding:utf-8-*-

from django.urls import path
from . import views

app_name = 'remember'

urlpatterns = [
    path('myFriends/', views.myFriends, name='myFriends'),
    path('selectShare/', views.selectShare, name='selectShare'),
    path('selectShare/chain/', views.shareChain, name='shareChain'),
    path('selectShare/qrcode/', views.shareQRcode, name='shareQRcode'),
    path('share/join/<str:shareLink>', views.shareSave, name='shareSave'),
    path('quasiFriends/', views.quasiFriends, name='quasi'),
    path('quasiFriends/operating/', views.quasiOperating, name='quasiOperating'),
    path('myFriends/f/<int:fid>/', views.friendInfo, name='friendInfo'),
]