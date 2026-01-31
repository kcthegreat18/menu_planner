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


@api_view(["POST"])
def dish_react_increment(request):
    dish_id = request.data.get("dish_id")
    reaction = request.data.get("reaction")  # "like" or "dislike"

    if not dish_id or reaction not in ("like", "dislike"):
        return Response(
            {"error": "dish_id and reaction ('like'|'dislike') are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    qs = Dish.objects.filter(id=dish_id)
    if not qs.exists():
        return Response({"error": "Dish not found"}, status=status.HTTP_404_NOT_FOUND)

    if reaction == "like":
        qs.update(dish_likes=F("dish_likes") + 1)
    else:
        qs.update(dish_dislikes=F("dish_dislikes") + 1)

    dish = Dish.objects.get(id=dish_id)
    return Response({"ok": True, "likes": dish.dish_likes, "dislikes": dish.dish_dislikes})
