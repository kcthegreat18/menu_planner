from rest_framework import viewsets
from .models import Dish, Menu, MenuDish, Request
from .serializers import DishSerializer, MenuSerializer, MenuDishSerializer, RequestSerializer
from django.http import JsonResponse
from django.utils.timezone import localdate
from .services import MenuGeneratorService

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F


def home(request):
    return JsonResponse({"message": "Welcome to the Menu Planner API"})

    
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset=Menu.objects.all()
    serializer_class=MenuSerializer


class MenuDishViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MenuDishSerializer

    def get_queryset(self):
        today=localdate()
        return MenuDish.objects.filter(menu__date=today).select_related('dish')

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    


def generate_menu_view(request):
    service = MenuGeneratorService()
    menu = service.generate_menu()
    return JsonResponse({"message": f"Menu generated for {menu.date}"})


@api_view(['POST'])
def dish_react_increment(request):
    dish_id=request.data.get("dish_id")
    reaction=request.data.get