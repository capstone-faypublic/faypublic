from django.contrib import admin
from .models import Class, ClassSection, ClassRegistration

# Register your models here.
class ClassesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Class, ClassesAdmin)



class ClassSectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClassSection, ClassSectionAdmin)


class ClassRegistrationAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClassRegistration, ClassRegistrationAdmin)