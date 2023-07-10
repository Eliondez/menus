from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=256)
    enabled = models.BooleanField(default=True)
    currency = models.ForeignKey('Currency', on_delete=models.RESTRICT, null=True)


    class Meta:
        verbose_name = 'Меню'

    def __str__(self):
        return self.name


class MenuItemType(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='categories/images',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Тип позиции меню'
        ordering = ['id']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=256)
    menu = models.ForeignKey(Menu, on_delete=models.RESTRICT)
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    item_type = models.ForeignKey(
        MenuItemType,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позициия меню'
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
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Картинка позиции меню'
        ordering = ['order', 'pk']


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
