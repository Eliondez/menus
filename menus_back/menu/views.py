import io
import json

from rest_framework import views, response

from . import models as menu_models
from . import serializers

FILE_NAME = 'menu.json'


class GetMenuMixin:
    @property
    def menu(self):
        return menu_models.Menu.objects.first()


class MenuParamsView(views.APIView, GetMenuMixin):

    def get(self, request, format=None):
        menu = self.menu

        currency_data = None
        if menu.currency:
            currency_data = {
                'char_code': menu.currency.char_code,
                'sign': menu.currency.sign,
                'from_left': menu.currency.from_left,
                'separated': menu.currency.separated,
            }

        return response.Response({
            'id': menu.id,
            'name': menu.name,
            'enabled': menu.enabled,
            'currency': currency_data,
        })


class MenuListView(views.APIView, GetMenuMixin):

    def get(self, request, format=None):
        menu = self.menu
        items = menu_models.MenuItem.objects.filter(
            menu=menu,
        ).select_related('item_type')
        serializer_class = serializers.MenuItemSerializer
        serializer = serializer_class(items, many=True)
        return response.Response(serializer.data)


class MenuCategoryListView(views.APIView):

    def get(self, request, format=None):
        items = menu_models.MenuItemType.objects.all()
        serializer_class = serializers.MenuTypeSerializer
        serializer = serializer_class(items, many=True)
        return response.Response(serializer.data)
