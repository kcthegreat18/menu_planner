from rest_framework import viewsets
from .models import Dish, Menu, MenuDish
from .serializers import DishSerializer, MenuSerializer, MenuDishSerializer
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the Menu Planner API"})

    
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuDishViewSet(viewsets.ModelViewSet):
    queryset = MenuDish.objects.all()
    serializer_class = MenuDishSerializer
