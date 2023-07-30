from rest_framework import views, response
from rest_framework import exceptions

from . import models as mm
from . import serializers


class GetMenuMixin:
    @property
    def menu(self):
        menu_id = self.request.query_params.get('menu_id')
        if not menu_id:
            raise exceptions.ValidationError('Param "menu_id:int" is required.')
        return mm.Menu.objects.get(id=menu_id)


class MenuDetailView(views.APIView, GetMenuMixin):

    def get(self, request, menu_id, format=None):
        if not menu_id:
            raise exceptions.ValidationError('Param "menu_id:int" is required.')
        menu = mm.Menu.objects.get(id=menu_id)

        currency_data = None
        if menu.currency:
            currency_data = {
                'char_code': menu.currency.char_code,
                'sign': menu.currency.sign,
                'from_left': menu.currency.from_left,
                'separated': menu.currency.separated,
            }

        items = []
        categories = {}
        for item in menu.items.select_related('item_type').filter(enabled=True):
            item_image = item.images.first()
            image_url = item_image.image.url if item_image else None

            items.append({
                'id': item.id,
                'description': item.description,
                'name': item.name,
                'category': item.item_type_id,
                'price': item.price,
                'image': image_url,
            })

            if item.item_type_id not in categories:
                categories[item.item_type_id] = {
                    'id': item.item_type_id,
                    'name': item.item_type.name,
                    'description': item.item_type.description,
                    'image': item.item_type.image.url if item.item_type.image else None,
                }

        return response.Response({
            'id': menu.id,
            'name': menu.name,
            'enabled': menu.enabled,
            'currency': currency_data,
            'items': items,
            'categories': categories,
        })


class UserRestaurantView(views.APIView):
    def get(self, request, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return response.Response({'message': 'Anon'})
        if not user.restaurant:
            return response.Response({'message': 'User has no resTAUrant'})
        serializer_class = serializers.RestaurantSerializer
        serializer = serializer_class(user.restaurant)
        return response.Response(serializer.data)


class ClientRestaurantsView(views.APIView):
    def get(self, request, restaurant_id, **kwargs):
        restaurant = mm.Restaurant.objects.filter(id=restaurant_id).first()
        if not restaurant:
            return response.Response(
                f'Restaurant_id={restaurant_id} not found',
                status=404
            )
        serializer_class = serializers.RestaurantSerializer
        serializer = serializer_class(restaurant)
        return response.Response(serializer.data)


class OrderCreate(views.APIView):
    def post(self, request, **kwargs):
        fields = [
            ['restaurant_id', 'int'],
            ['table_id', 'str'],
            ['items', 'list'],
        ]
        errors = []
        for item_name, item_type in fields:
            if item_name not in request.data:
                errors.append(
                    f'Field {item_name}:{item_type} required'
                )
        table = mm.Table.objects.filter(
            num=request.data['table_id'],
            restaurant_id=request.data['restaurant_id']
        ).first()

        if errors:
            return response.Response(
                {
                    'errors': errors,
                },
                status=400,
            )

        order = mm.Order.get_for_table(table_num=table.num)
        for item in request.data['items']:
            order_item = mm.OrderItem(
                order=order,
                product_id=item['id'],
                count=item['count'],
            )
            order_item.save()

        return response.Response({'status': 'OK! :)'})

class OrderDetail(views.APIView):
    def get(self, request, **kwargs):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if not restaurant_id:
            raise exceptions.ValidationError('Param "restaurant_id:int" is required.')
        table_id = self.request.query_params.get('table_id')
        if not table_id:
            raise exceptions.ValidationError('Param "table_id:int" is required.')
        table = mm.Table.objects.filter(num=table_id, restaurant_id=restaurant_id).first()
        if not table:
            return response.Response(
                f'Table id={table_id} not found for '
                f'restaurant_id={restaurant_id}',
                status=404
            )
        order = mm.Order.get_for_table(table_num=table.num)
        res = {
            'order_id': order.id,
            'table': order.table.num,
            'items': []
        }

        for item in order.items.all():
            res['items'].append({
                'id': item.id,
                'product': item.product_id,
                'count': item.count,
                'status': item.status
            })
        return response.Response(res)
