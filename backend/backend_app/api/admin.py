from django.contrib import admin
from .models import *

class DishAdmin(admin.ModelAdmin):
    list_display=["id","dish_name","dish_type","dish_method","dish_color","dish_description", "dish_calories"]

class MenuAdmin(admin.ModelAdmin):
    list_display=["date","created_at"]

@admin.register(MenuDish)
class MenuDishAdmin(admin.ModelAdmin):
    list_display=["menu","dish"]


admin.site.register(Dish,DishAdmin)
admin.site.register(Menu,MenuAdmin)
