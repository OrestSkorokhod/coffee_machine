from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.



class CoffeeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    # current_order =  models.OneToOneField('Order', on_delete=models.CASCADE, blank=True, default=None)
    # current_order = models.CharField(max_length=500, blank=True)
    account = models.IntegerField()

    def __str__(self):
        return self.user.username


class Drink(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    price = models.IntegerField(default=0)


    def get_order_url(self):
        return reverse('order_drink_url', kwargs={'id': self.id})

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    price = models.IntegerField(default=0)


    def __str__(self):
        return self.name


class Order(models.Model):
    coffee_user = models.ForeignKey(CoffeeUser, on_delete=models.CASCADE, db_index=True)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name='orders')



class CoffeMachine(models.Model):
    def __str__(self):
        return 'coffeemachine #{}'.format(self.id)
        # ingredients = models.ForeignKey(IngredientList, on_delete=models.CASCADE,)
        # drinks = models.ForeignKey(DrinkList, on_delete=models.CASCADE,)


class DrinkList(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    count = models.IntegerField()
    coffeemachine = models.ForeignKey(CoffeMachine, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return 'drink: {}, {}'.format(self.drink, self.coffeemachine)


class IngredientList(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.IntegerField()
    coffeemachine = models.ForeignKey(CoffeMachine, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return 'drink: {}, {}'.format(self.ingredient, self.coffeemachine)
