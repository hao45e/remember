from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import uuid
import datetime

# Create your models here.


class Friend(models.Model):
    """
    friend model
    """
    def getAge(self):
        birthday = self.birthday
        year = ''
        if birthday != '':
            now = datetime.datetime.now()
            now_date = datetime.date(now.year, now.month, now.day)
            year = relativedelta(now_date, birthday).years
        return year

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    name = models.CharField(verbose_name='姓名', max_length=50)
    sex = models.SmallIntegerField(verbose_name='性别')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    age = getAge
    phone = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    old_address = models.CharField(verbose_name='故乡', max_length=30, null=True, blank=True)
    new_address = models.CharField(verbose_name='现居地', max_length=30, null=True, blank=True)
    origin = models.TextField(verbose_name='相识', max_length=200, null=True, blank=True)
    status = models.SmallIntegerField(verbose_name='状态', default=2)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name


class FriendPhoto(models.Model):
    """
    friend photos model
    """

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        date = datetime.datetime.now()
        typ = 'file'
        if filename.endswith('.jpg'):
            typ = 'jpg'
        elif filename.endswith('.jpeg'):
            typ = 'jpeg'
        elif filename.endswith('.png'):
            typ = 'png'
        elif filename.endswith('.gif'):
            typ = 'gif'
        else:
            typ = 'other'
        filename = str(uuid.uuid1()) + '.' + typ
        return 'friend/photo/{}/{}/{}/{}/{}'.format(date.year, date.month, date.day, typ, filename)

    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    photo_img = models.ImageField(upload_to=user_directory_path)
    photo_description = models.CharField(max_length=200, null=True, blank=True)
    status = models.SmallIntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
