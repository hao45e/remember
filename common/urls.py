# -*-coding:utf-8-*-

from django.urls import path
from common import views


app_name = 'common'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('share/<str:share_link>/', views.share, name='share'),
    path('shareSuccess/', views.shareSuccess, name='shareSuccess'),
    path('myInfo/', views.myInfo, name='myInfo'),
    path('editMyInfo/', views.EditMyInfoView.as_view(), name='editMyInfo'),
    path('editMyPWD/', views.EditMyPWD.as_view(), name='editMyPWD'),
    path('search/', views.search, name='search'),
]