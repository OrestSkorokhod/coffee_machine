from django.contrib import admin

# Register your models here.

from coffeemachine.models import *



admin.site.register(CoffeeUser)
admin.site.register(Drink)
admin.site.register(Ingredient)
admin.site.register(IngredientList)
admin.site.register(DrinkList)
admin.site.register(CoffeMachine)
admin.site.register(Order)
