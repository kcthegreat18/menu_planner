from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, MenuViewSet, MenuDishViewSet, home, generate_menu_view, RequestViewSet

router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dishes')
router.register(r'menus', MenuViewSet, basename='menus')
router.register(r'menu-dishes', MenuDishViewSet, basename='menu-dishes')
router.register(r'requests', RequestViewSet, basename='requests')




urlpatterns = [
    path('', home),  # <-- root of /api/
    *router.urls,
    path('generate-menu/', generate_menu_view),
]
