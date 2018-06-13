from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import uuid

# Create your models here.


class UserHeadPhoto(models.Model):

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
        return 'user/head_portrait/{}/{}/{}/{}/{}'.format(date.year, date.month, date.day, typ, filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    head_portrait = models.ImageField(verbose_name='头像', upload_to=user_directory_path)
    status = models.SmallIntegerField(verbose_name='状态', default=1)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
