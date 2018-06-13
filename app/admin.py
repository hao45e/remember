from django.contrib import admin
from . import models

# Register your models here.


class FriendPhotoInline(admin.TabularInline):
    model = models.FriendPhoto

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Friend)
class FriendAdmin(admin.ModelAdmin):
    inlines = [FriendPhotoInline]
    list_display = ('name', 'user', 'sex', 'birthday', 'age', 'phone', 'old_address',
                    'new_address', 'origin', 'status', 'create_time')
    list_per_page = 10
    ordering = ('-create_time',)
    list_editable = []
    fk_fields = ('user',)

    list_filter = ('sex', 'status')
    search_fields = ('user__username', 'name', 'phone', 'old_address', 'new_address')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        return False


@admin.register(models.FriendPhoto)
class FriendPhoto(admin.ModelAdmin):
    list_display = ('friend', 'photo_img', 'photo_description', 'status', 'create_time')
    list_per_page = 10
    fk_fields = ('friend',)
    ordering = ('-create_time',)
    list_filter = ('status',)
    search_fields = ('friend__name',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        return False


