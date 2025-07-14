import random
from datetime import timedelta
from django.utils.timezone import localdate
from django.db.models import Q
from .models import Dish, Menu, MenuDish


class MenuGeneratorService:
    def __init__(self, date=None):
        self.today = date or localdate()
        self.week_start = self.today - timedelta(days=self.today.weekday())
        self.week_end = self.week_start + timedelta(days=6)

    def get_week_used_dishes(self):
        return Dish.objects.filter(
            dish_menus__menu__date__range=(self.week_start, self.week_end)
        ).distinct()

    def get_candidates(self):
        return Dish.objects.exclude(id__in=self.get_week_used_dishes())

    def pick_dishes(self, dishes, count, filters=None):
        filtered = dishes
        if filters:
            filtered = dishes.filter(**filters)
        return random.sample(list(filtered), count) if len(filtered) >= count else []

    def generate_menu(self):
        if Menu.objects.filter(date=self.today).exists():
            return None  # Menu already exists

        dishes = self.get_candidates()

        selected = []

        # --- Chicken Rules ---
        chicken = dishes.filter(dish_type='CH')
        chicken_saucy = chicken.filter(dish_method='SAUCY')

        saucy_or = chicken_saucy.filter(dish_color='OR')
        saucy_br = chicken_saucy.filter(dish_color='BR')
        saucy_wh = chicken_saucy.filter(dish_color='WH')

        fried_or_soupy = chicken.filter(dish_method__in=['FRIED', 'SOUPY'])
        baked_or_roasted = chicken.filter(dish_method__in=['BAKED', 'ROASTED'])

        # pick 2 saucy chicken with different colors
        chicken_saucy_combo = self.pick_color_combo([saucy_or, saucy_br, saucy_wh], 2)
        selected += chicken_saucy_combo
        selected += self.pick_dishes(fried_or_soupy.exclude(id__in=[d.id for d in selected]), 1)
        selected += self.pick_dishes(baked_or_roasted.exclude(id__in=[d.id for d in selected]), 1)

        # --- Pork Rules ---
        pork = dishes.filter(dish_type='PO')
        pork_saucy = pork.filter(dish_method='SAUCY')

        saucy_or = pork_saucy.filter(dish_color='OR')
        saucy_br = pork_saucy.filter(dish_color='BR')
        saucy_wh = pork_saucy.filter(dish_color='WH')

        fried = pork.filter(dish_method='FRIED')

        pork_saucy_combo = self.pick_color_combo([saucy_or, saucy_br, saucy_wh], 2)
        selected += pork_saucy_combo
        selected += self.pick_dishes(fried.exclude(id__in=[d.id for d in selected]), 1)

        # --- Seafood ---
        seafood = dishes.filter(dish_type='SF')
        selected += self.pick_dishes(seafood, 1)

        # --- Vegetables ---
        vegetables = dishes.filter(dish_type='VE')
        selected += self.pick_dishes(vegetables, 2)

        # --- Breakfast ---
        breakfast = dishes.filter(dish_type='BF')
        selected += self.pick_dishes(breakfast, random.randint(1, 2))

        # --- Snacks ---
        snacks = dishes.filter(dish_type='SN')
        selected += self.pick_dishes(snacks, random.randint(1, 2))

        # --- Fruits ---
        fruits = dishes.filter(dish_type='FR')
        selected += self.pick_dishes(fruits, random.randint(1, 2))

        # Save menu
        menu = Menu.objects.create(date=self.today)
        for dish in selected:
            MenuDish.objects.create(menu=menu, dish=dish)

        return menu

    def pick_color_combo(self, color_groups, count):
        combos = []
        used = set()
        for group in color_groups:
            group_set = list(group.exclude(id__in=used))
            if group_set:
                pick = random.choice(group_set)
                combos.append(pick)
                used.add(pick.id)
                if len(combos) == count:
                    break
        return combos
