from django.contrib import admin
from .models import Equipment, EquipmentCategory, EquipmentCheckout

# Register your models here.
class EquipmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Equipment, EquipmentAdmin)

class EquipmentCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(EquipmentCategory, EquipmentCategoryAdmin)

class EquipmentCheckoutAdmin(admin.ModelAdmin):
    pass
admin.site.register(EquipmentCheckout, EquipmentCheckoutAdmin)