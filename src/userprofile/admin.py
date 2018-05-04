from django.contrib import admin
from .models import Badge, User, UserProfile

# Register your models here.
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)

admin.site.register(Badge, BadgeAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('badges',)

admin.site.register(UserProfile, UserProfileAdmin)