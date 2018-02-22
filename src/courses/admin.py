from django.contrib import admin
from .models import Course

# Register your models here.
class CoursesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CoursesAdmin)