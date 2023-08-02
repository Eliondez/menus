from __future__ import annotations

from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=256)
    enabled = models.BooleanField(default=True)
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.RESTRICT,
        null=True,
        related_name='menus'
    )
    currency = models.ForeignKey('Currency', on_delete=models.RESTRICT, null=True)

    class Meta:
        verbose_name = 'Menu'

    def __str__(self):
        return self.name


class MenuItemType(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.RESTRICT,
        null=True,
        related_name='types'
    )
    image = models.ImageField(
        upload_to='categories/images',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=256)
    menu = models.ForeignKey(
        Menu,
        on_delete=models.RESTRICT,
        related_name='items',
    )
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    item_type = models.ForeignKey(
        MenuItemType,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item'
        ordering = ['item_type', 'id']

    def __str__(self):
        return self.name


class MenuItemPicture(models.Model):
    image = models.ImageField(
        upload_to='items/images'
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='images',
    )
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Item image'
        ordering = ['pk']


class Currency(models.Model):
    char_code = models.CharField(max_length=8, primary_key=True)
    sign = models.CharField(max_length=1, blank=True)
    from_left = models.BooleanField(default=True, blank=True)
    separated = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return f'{self.char_code} ({self.sign})'


class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    enabled = models.BooleanField(default=True, blank=True)
    address = models.TextField(null=True)
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name='active_restaurants',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Restaurant'
        ordering = ['pk']


class Table(models.Model):
    num = models.CharField(max_length=128, unique=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.num}__{self.restaurant.name}'

    class Meta:
        verbose_name = 'Table'
        ordering = ['pk']

class Order(models.Model):

    STATUS_IN_WORK = 0
    STATUS_COMPLETED = 1

    STATUS_CHOICES = (
        (STATUS_IN_WORK, 'in_work'),
        (STATUS_COMPLETED, 'completed'),
    )

    table = models.ForeignKey('Table', on_delete=models.RESTRICT, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_IN_WORK)

    @classmethod
    def get_for_table(cls, table: Table) -> Order:
        return cls.objects.filter(table=table, status__in=[cls.STATUS_IN_WORK]).first()

    class Meta:
        verbose_name = 'Order'
        ordering = ['pk']


class OrderItem(models.Model):

    STATUS_ORDERED = 'ordered'
    STATUS_PREPARING = 'preparing'

    STATUS_CHOICES = (
        (STATUS_ORDERED, 'ordered'),
        (STATUS_PREPARING, 'preparing'),
    )

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('MenuItem', on_delete=models.RESTRICT)
    count = models.FloatField(default=1.0)
    status = models.CharField(choices=STATUS_CHOICES, max_length=128, default=STATUS_ORDERED)

    def __str__(self):
        return f'Order:{self.order_id} product:{self.product_id} ({self.count})'

    class Meta:
        verbose_name = 'Order item'
        ordering = ['pk']
