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


class OrderView(views.APIView):

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
        if errors:
            return response.Response({'errors': errors}, status=400)

        table = self.get_table(
            restaurant_id=request.data['restaurant_id'],
            table_id=request.data['table_id']
        )
        order = self.get_order(table=table, can_create=True)

        for item in request.data['items']:
            order_item = mm.OrderItem(
                order=order,
                product_id=item['id'],
                count=item['count'],
            )
            order_item.save()

        return self.get_response(order)

    def get_order(self, table: mm.Table, can_create=False):
        order = mm.Order.get_for_table(table=table)
        if not order:
            if can_create:
                order = mm.Order.objects.create(
                    table=table,
                )
            else:
                raise exceptions.ValidationError('No order found.')
        return order

    def get_table(self, restaurant_id: int, table_id: str) -> mm.Table:
        table = mm.Table.objects.filter(num=table_id, restaurant_id=restaurant_id).first()
        if not table:
            return response.Response(
                f'Table id={table_id} not found for '
                f'restaurant_id={restaurant_id}',
                status=404
            )
        return table

    def get_response(self, order: mm.Order) -> response.Response:
        res = {
            'order_id': order.id,
            'table': order.table.num,
            'items': []
        }
        items_by_product_id = {}
        for item in order.items.all().select_related('product'):
            if item.product_id not in items_by_product_id:
                items_by_product_id[item.product_id] = {
                    'product_id': item.product_id,
                    'name': item.product.name,
                    'count': 0,
                    'price': item.product.price,
                    'order_first_item_id': item.id,
                }
            items_by_product_id[item.product_id]['count'] += item.count
            res['items'] = list(items_by_product_id.values())
        return response.Response(res)

    def get(self, request, **kwargs):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if not restaurant_id:
            raise exceptions.ValidationError('Param "restaurant_id:int" is required.')
        table_id = self.request.query_params.get('table_id')
        if not table_id:
            raise exceptions.ValidationError('Param "table_id:str" is required.')
        table = self.get_table(restaurant_id, table_id)
        order = self.get_order(table)
        return self.get_response(order)


class OrderClose(views.APIView):

    def post(self, request, **kwargs):
        table = mm.Table.objects.filter(
            num=request.data['table_id'],
            restaurant_id=request.data['restaurant_id']
        ).first()
        order = mm.Order.get_for_table(table=table)
        if order:
            order.status = mm.Order.STATUS_COMPLETED
            order.save()
            return response.Response({
                'status': 'OK'
            })
        else:
            return response.Response({
                'status': 'Fail',
                'message': 'No order found'
            })


class OrderCheckout(views.APIView):
    def post(self, request, **kwargs):
        if 'pay_type' not in request.data:
            raise exceptions.ValidationError('Param "pay_type:int" is required.')
        table = mm.Table.objects.filter(
            num=request.data['table_id'],
            restaurant_id=request.data['restaurant_id']
        ).first()
        order = mm.Order.get_for_table(table=table)
        if not order:
            return response.Response({
                'status': 'Fail',
                'message': 'No order found'
            })

        pay_type = request.data['pay_type']
        if pay_type is not None:
            order.pay_type = int(pay_type)
        else:
            order.pay_type = None
        order.save()
        return response.Response({
            'status': 'OK'
        })


class ManagerView(views.APIView):
    def get_restaurant_id(self):
        user = self.request.user
        if not user.is_authenticated:
            return response.Response(status=401)

        restaurant_id = user.restaurant_id
        if not restaurant_id:
            return response.Response(
                f'user "{user.username}" has no restaurant',
                status=400
            )
        return restaurant_id


class ManagerOrderView(ManagerView):

    def get(self, request, **kwargs):
        restaurant_id = self.get_restaurant_id()

        filter_data = {
            'table__restaurant_id': restaurant_id,
            'status': mm.Order.STATUS_IN_WORK,
        }
        orders_data = mm.Order.objects.filter(**filter_data)

        orders = []
        for order in orders_data:
            orders.append({
                'table_id': order.table_id,
                'order_id': order.id,
                'pay_type': order.get_pay_type_display(),
                'items_count': order.items.count(),
            })
        return response.Response({
            'orders': orders,
        })

class ManagerInfoView(ManagerView):

    def get(self, request, **kwargs):
        restaurant_id = self.get_restaurant_id()
        restaurant = mm.Restaurant.objects.get(id=restaurant_id)
        return response.Response({
            'user': {
                'username': request.user.username,
            },
            'restaurant': {
                'id': restaurant_id,
                'name': restaurant.name,
            },
        })


