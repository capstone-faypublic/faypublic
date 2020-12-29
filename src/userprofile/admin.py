import arrow
from django.contrib import admin
from django.utils import timezone
from django.db.models import Count
from .models import Badge, User, UserProfile

# Register your models here.
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)

admin.site.register(Badge, BadgeAdmin)

class InactiveUserListFilter(admin.SimpleListFilter):
    title = 'Inactive users'
    parameter_name = 'inactive'

    def lookups(self, request, model_admin):
        return (
            ('1mo', 'Inactive for a month'),
            ('3mo', 'Inactive for three months'),
            ('6mo', 'Inactive for six months')
        )
    
    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        inactive_months = -1 if self.value() == '1mo' else -3 if self.value() == '3mo' else -6
        months_ago = arrow.get(timezone.now()).shift(months=inactive_months).datetime

        return queryset.filter(
            user__last_login__lte=months_ago,
            user__project__expected_completion_date__gte=months_ago,
            # user__equipmentcheckout__due_date__gte=months_ago
        ).annotate(
            recent_projects=Count('user__project'),
            recent_checkouts=Count('user__equipmentcheckout')
        ).filter(
            # recent_projects=0,
            # recent_checkouts=0
        )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = (InactiveUserListFilter,)
    filter_horizontal = ('badges',)

admin.site.register(UserProfile, UserProfileAdmin)