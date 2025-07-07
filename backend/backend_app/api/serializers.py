from rest_framework import serializers
from .models import Dish, Menu, MenuDish

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDish
        fields = '__all__'
