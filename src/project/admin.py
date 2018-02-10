from django.contrib import admin
from .models import Project, ProjectSubmission

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)


class ProjectSubmissionAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProjectSubmission, ProjectSubmissionAdmin)