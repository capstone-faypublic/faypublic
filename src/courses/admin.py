from django.contrib import admin
from .models import Course, CourseSection, CourseRegisteration

# Register your models here.
class CoursesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CoursesAdmin)



class CourseSectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseSection, CourseSectionAdmin)


class CourseRegisterationAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseRegisteration, CourseRegisterationAdmin)