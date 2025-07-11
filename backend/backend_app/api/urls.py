from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, MenuViewSet, MenuDishViewSet, home

router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dishes')
router.register(r'menus', MenuViewSet, basename='menus')
router.register(r'menu-dishes', MenuDishViewSet, basename='menu-dishes')


urlpatterns = [
    path('', home),  # <-- root of /api/
    *router.urls,
]
