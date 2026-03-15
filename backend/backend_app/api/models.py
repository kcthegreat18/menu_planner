from django.db import models
from django.utils.timezone import localdate

DISH_TYPE=[
    ("CH","Chicken"),
    ("PO", "Pork"),
    ("SF", "Sea Food"),
    ("VE", "Vegerables"),
    ("BF", "Breakfast"),
    ("SN", "Snacks"),
    ("FR", "Fruits")
]

DISH_METHOD=[
    ("SAUTE", "Saute"),
    ("STIRFY", "Stirfry"),
    ("FRIED", "Fried"),
    ("BAKED", "Baked"),
    ("SAUCY", "Saucy"),
    ("SOUPY", "Soupy"),
    ("ROASTED", "Roasted"),
]

DISH_COLOR=[
    ("BR", "Brown"),
    ("OR","Orange"),
    ("WH","White"),
    ("YE", "Yellow"),
]

# Create your models here.
class Dish(models.Model):
    
    dish_name=models.CharField(max_length=30, unique=True)
    dish_type=models.CharField(max_length=3,choices=DISH_TYPE)
    dish_method=models.CharField(max_length=10, choices=DISH_METHOD, blank=True)
    dish_color=models.CharField(max_length=4, choices=DISH_COLOR, blank=True)
    dish_description=models.CharField(max_length=100, blank=True)
    dish_calories=models.PositiveIntegerField(max_length=3, blank=True)

    dish_likes=models.PositiveIntegerField(default=0)
    dish_dislikes=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.dish_name}"


class Menu(models.Model):
    date = models.DateField(unique=True, default=localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date}"

class MenuDish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_dishes")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_menus")


    def __str__(self):
        return f"{self.dish.dish_name} in {self.menu.date}"

class Request(models.Model):
    name = models.CharField(max_length=30)
    student_number = models.CharField(max_length=11) 
    up_mail = models.EmailField(max_length=50)
    dish_name = models.CharField(max_length=30)
    dish_type = models.CharField(max_length=3, choices=DISH_TYPE)
    dish_description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.dish_name}"
#    dish_name=models.CharField(max_length=30, unique=True)
