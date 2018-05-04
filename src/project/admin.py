from django.contrib import admin
from .models import Project, ProgramRequest

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)

class ProgramRequestAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProgramRequest, ProgramRequestAdmin)