from django.contrib import admin
from . import models


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'item_type', 'price', 'menu']


admin.site.register(models.Menu)
admin.site.register(models.MenuItem, MenuItemAdmin)
admin.site.register(models.MenuItemType)
admin.site.register(models.MenuItemPicture)
admin.site.register(models.Currency)
admin.site.register(models.Restaurant)
admin.site.register(models.Table)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
