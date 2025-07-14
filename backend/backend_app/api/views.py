from rest_framework import viewsets
from .models import Dish, Menu, MenuDish
from .serializers import DishSerializer, MenuSerializer, MenuDishSerializer
from django.http import JsonResponse
from django.utils.timezone import localdate
from .services import MenuGeneratorService

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
    


def generate_menu_view(request):
    service = MenuGeneratorService()
    menu = service.generate_menu()
    return JsonResponse({"message": f"Menu generated for {menu.date}"})