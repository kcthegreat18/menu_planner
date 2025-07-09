from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, MenuViewSet, MenuDishViewSet, home

router = DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'menu-dish', MenuDishViewSet)

urlpatterns = [
    path('', home),  # <-- root of /api/
    *router.urls,
]
