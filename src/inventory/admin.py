from django.contrib import admin
from .models import Equipment, EquipmentCategory, EquipmentCheckout

# Register your models here.
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'quantity', 'available', 'checkout_timeframe')
    list_filter = ('make', 'checkout_timeframe', 'category__title')
    exclude = ('slug',)
    ordering = ('make', 'model')
    filter_horizontal = ('prerequisite_badges',)
    search_fields = ('make', 'model', '')
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
    list_display = ('equipment_name', 'user_name', 'project_title', 'due_date_humanized', 'checkout_status')
    list_editable = ('checkout_status',)
    list_filter = ('due_date', 'checkout_status')
    search_fields = ('user__first_name', 'user__last_name', 'equipment__make', 'equipment__model', 'equipment__category__title')
    fields = ('checkout_status',)

    ordering = ('-due_date',)
admin.site.register(EquipmentCheckout, EquipmentCheckoutAdmin)