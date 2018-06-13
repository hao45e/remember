from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.UserHeadPhoto)
class UserHeadPhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'create_time')
    ordering = ('-create_time',)
    list_per_page = 10
    fk_fields = ('user',)
    list_filter = ('status',)
    search_fields = ('user__username',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        return False