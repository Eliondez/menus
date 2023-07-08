from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=256)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Меню'

    def __str__(self):
        return self.name


class MenuItemType(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Тип позиции меню'
        ordering = ['id']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=256)
    menu = models.ForeignKey(Menu, on_delete=models.RESTRICT)
    description = models.TextField()
    enabled = models.BooleanField(default=True)
    item_type = models.ForeignKey(
        MenuItemType,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позициия меню'
        ordering = ['id']

    def __str__(self):
        return self.name


class MenuItemPicture(models.Model):
    image = models.ImageField()
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Картинка позиции меню'
        ordering = ['order', 'pk']
