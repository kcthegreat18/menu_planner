from django.contrib import admin
from .models import *

class DishAdmin(admin.ModelAdmin):
    list_display=["id","dish_name","dish_type","dish_method","dish_color","dish_description", "dish_calories", "dish_likes","dish_dislikes"]

class MenuAdmin(admin.ModelAdmin):
    list_display=["date","created_at"]

@admin.register(MenuDish)
class MenuDishAdmin(admin.ModelAdmin):
    list_display=["menu","dish"]

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display=["name","student_number","up_mail","dish_name","dish_type","dish_description"]


admin.site.register(Dish,DishAdmin)
admin.site.register(Menu,MenuAdmin)
