from django.contrib import admin
from . import models


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'item_type', 'price', 'menu']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'table']
    list_editable = ['status']


admin.site.register(models.Menu)
admin.site.register(models.MenuItem, MenuItemAdmin)
admin.site.register(models.MenuItemType)
admin.site.register(models.MenuItemPicture)
admin.site.register(models.Currency)
admin.site.register(models.Restaurant)
admin.site.register(models.Table)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)
