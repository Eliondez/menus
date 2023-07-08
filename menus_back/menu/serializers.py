from rest_framework import serializers

from . import models


class MenuTypeSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()

    class Meta:
        model = models.MenuItemType
        fields = ['id', 'name', 'cover']

    def get_cover(self, obj):
        return obj.image.url if obj.image else None


class MenuItemSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = models.MenuItem
        fields = ['id', 'name', 'description', 'price', 'cover', 'category']

    def get_category(self, obj):
        return MenuTypeSerializer(obj.item_type).data

    def get_cover(self, obj):
        return obj.images.first()



