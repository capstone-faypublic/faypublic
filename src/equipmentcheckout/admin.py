from django.contrib import admin
from .models import Equipment, EquipmentCheckout

# Register your models here.
class EquipmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Equipment, EquipmentAdmin)

class EquipmentCheckoutAdmin(admin.ModelAdmin):
    pass
admin.site.register(EquipmentCheckout, EquipmentCheckoutAdmin)