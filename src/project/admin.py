from django.contrib import admin
from .models import Project, ProgramRequest

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['title', 'owner__first_name', 'owner__last_name', 'owner__username']
admin.site.register(Project, ProjectAdmin)

class ProgramRequestAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProgramRequest, ProgramRequestAdmin)