from rest_framework import serializers

from . import models


class MenuItemSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.MenuItem
        fields = ['id', 'name', 'description', 'price', 'images']

    def get_images(self, obj):

        return []


class MenuTypeSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = models.MenuItemType
        fields = ['id', 'name', 'items']

    def get_items(self, obj):
        items = obj.items.all()
        return MenuItemSerializer(items, many=True).data

