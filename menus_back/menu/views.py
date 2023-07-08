import io
import json

from rest_framework import views, response

from . import models as menu_models
from . import serializers

FILE_NAME = 'menu.json'


class MenuListView(views.APIView):

    def get(self, request, format=None):
        print('123123')
        return response.Response({})


class MenuLoad(views.APIView):
    def get(self, request, format=None):
        with open(FILE_NAME, 'r') as menu_dump:
            data = json.load(menu_dump)
            menu_models.MenuItemType.objects.all().delete()
            for type_data in data['types']:
                menu_models.MenuItemType.objects.create(
                    id=type_data['id'],
                    name=type_data['name'],
                )
        return response.Response({})


class MenuClear(views.APIView):
    def get(self, request, format=None):
        menu_models.MenuItemType.objects.all().delete()
        return response.Response({})


class MenuDump(views.APIView):

    def get(self, request, format=None):
        res = dict()
        types = menu_models.MenuItemType.objects.all()
        serializer_class = serializers.MenuTypeSerializer
        serializer = serializer_class(types, many=True)
        res['types'] = serializer.data
        print(f'Dumped {len(res["types"])} types')

        with open('menu.json', 'w') as menu_dump:
            menu_dump.write(json.dumps(res, indent=2))

        # menu_models.MenuItemType.objects.all().delete()
        # menu_types = list()
        #
        # for name in [
        #     'Завтраки',
        #     'Супы',
        #     'Салаты',
        #     'Основные блюда',
        #     'Напитки',
        #     'Десерты',
        #
        # ]:
        #     menu_types.append(
        #         menu_models.MenuItemType.objects.create(
        #             name=name,
        #         )
        #     )

        return response.Response(res)
