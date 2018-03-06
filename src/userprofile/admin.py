from django.contrib import admin
from .models import Badge, User, UserProfile

# Register your models here.
class BadgeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Badge, BadgeAdmin)

