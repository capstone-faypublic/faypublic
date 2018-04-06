from django.contrib import admin
from .models import Class, ClassSection, ClassRegistration

# Register your models here.
class ClassSectionInline(admin.TabularInline):
    model = ClassSection
    fields = ['date', 'seats_avaliable']


class ClassesAdmin(admin.ModelAdmin):
    inlines = [ClassSectionInline]
    list_display = ['class_title', 'number_of_open_sections']
    exclude = ('slug',)
    ordering = ('class_title',)
    filter_horizontal = ('prerequisite_badges','awarded_badges')
    search_fields = ('class_title',)
admin.site.register(Class, ClassesAdmin)


class ClassRegistrationInline(admin.TabularInline):
    model = ClassRegistration
    fields = ['user', 'completed', 'score_percentage']

class ClassSectionAdmin(admin.ModelAdmin):
    inlines = [ClassRegistrationInline]
    list_display = ['__str__', 'date', 'number_open_seats', 'number_registered']
    list_editable = ['date']
    ordering = ('-date',)
admin.site.register(ClassSection, ClassSectionAdmin)


class ClassRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'class_title', 'section', 'completed', 'score_percentage']
    list_editable = ['completed', 'score_percentage']
admin.site.register(ClassRegistration, ClassRegistrationAdmin)