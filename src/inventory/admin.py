from django.contrib import admin
from .models import Equipment, EquipmentCategory, EquipmentCheckout, ClosedDay

# Register your models here.

class EquipmentCheckoutInline(admin.TabularInline):
    model = EquipmentCheckout
    fields = ('user', 'project', 'equipment', 'checkout_date', 'due_date', 'checkout_status')

class EquipmentAdmin(admin.ModelAdmin):
    inlines = [EquipmentCheckoutInline]
    list_display = ('make', 'model', 'quantity', 'available', 'checkout_timeframe')
    list_filter = ('make', 'checkout_timeframe', 'category__title')
    exclude = ('slug',)
    ordering = ('make', 'model')
    filter_horizontal = ('prerequisite_badges',)
    search_fields = ('make', 'model')
    autocomplete_fields = ['category']

admin.site.register(Equipment, EquipmentAdmin)


class EquipmentCategoryInline(admin.TabularInline):
    model = Equipment
    fields = ('make', 'model', 'quantity', 'checkout_timeframe', 'image')

class EquipmentCategoryAdmin(admin.ModelAdmin):
    inlines = [EquipmentCategoryInline]
    list_display = ('title', 'number_of_items')
    search_fields = ('title',)
    fields = ('title',)
    ordering = ('title',)

admin.site.register(EquipmentCategory, EquipmentCategoryAdmin)

class EquipmentCheckoutAdmin(admin.ModelAdmin):
    list_display = ('equipment_name', 'user_name', 'project_title', 'checkout_date', 'due_date', 'due_date_humanized', 'checkout_status')
    list_editable = ('checkout_status', 'checkout_date', 'due_date',)
    list_filter = ('due_date', 'checkout_status')
    search_fields = ('user__first_name', 'user__last_name', 'equipment__make', 'equipment__model', 'equipment__category__title')
    fields = ('user', 'project', 'equipment', 'checkout_date', 'due_date', 'checkout_status',)
    autocomplete_fields = ['user', 'equipment', 'project']

    ordering = ('-due_date',)
admin.site.register(EquipmentCheckout, EquipmentCheckoutAdmin)


class ClosedDayAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'begin_date', 'end_date')
    list_editable = ('begin_date', 'end_date')
    list_filter = ('day_of_week', 'begin_date', 'end_date')
    search_fields = ('day_of_week', 'begin_date', 'end_date')
    fields = ('day_of_week', 'begin_date', 'end_date')
    ordering = ('-begin_date',)
admin.site.register(ClosedDay, ClosedDayAdmin)