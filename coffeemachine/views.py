from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from coffeemachine.models import *
from coffeemachine.utils import add_drink_and_ingredients

# Create your views here.

@login_required
def index(request):

    if not CoffeeUser.objects.filter(user=request.user).first():
        CoffeeUser(user=request.user, account=20).save()
    coffeemachine = CoffeMachine.objects.first()
    drinks = [drinklist.drink for drinklist in coffeemachine.drinklist_set.all() if drinklist.count > 0]
    # print(drinks)
    return render(request, 'coffeemachine/index.html', context={'drinks': drinks})

@login_required
def order_drink(request, id):
    drink = Drink.objects.filter(id=id).first()

    if request.method == 'POST':
        coffeemachine = CoffeMachine.objects.first()
        drinklist = coffeemachine.drinklist_set.filter(drink=drink).first()
        drinklist.count -= 1
        drinklist.save()

        user = CoffeeUser.objects.filter(user=request.user).first()

        all_ingredients_names = [ingredient.name for ingredient in Ingredient.objects.all()]

        order = Order(coffee_user=user, drink=drink)
        order.save()

        ingredientlists = coffeemachine.ingredientlist_set

        ingredients_names = ''
        for item in request.POST.keys():
            if item in all_ingredients_names:
                ingredient = Ingredient.objects.filter(name=item).first()
                order.ingredients.add(ingredient)
                ingredientlist = ingredientlists.filter(ingredient=ingredient).first()
                ingredientlist.count -= 1
                ingredientlist.save()


        order.save()

        return redirect(reverse('after_order_url'))



    coffeemachine = CoffeMachine.objects.first()
    ingredients = [ingredientlist.ingredient for ingredientlist in coffeemachine.ingredientlist_set.all() if ingredientlist.count > 0]

    return render(request, 'coffeemachine/order_drink.html', context={'drink': drink, 'ingredients': ingredients})

@login_required
def after_order(request):
    user = CoffeeUser.objects.filter(user=request.user).first()
    # drinks_with_ingredients = make_dict_of_order(user.current_order)
    price = 0
    orders = user.order_set.all()
    for order in orders:
        price += order.drink.price
        for ingredient in order.ingredients.get_queryset():
            price += ingredient.price

    return render(request, 'coffeemachine/after_order.html', context={'coffee_user': user, 'orders': orders, 'price': price})

@login_required
def payment(request):
    user = CoffeeUser.objects.filter(user=request.user).first()

    price = 0
    orders = user.order_set.all()
    for order in orders:
        price += order.drink.price
        for ingredient in order.ingredients.get_queryset():
            price += ingredient.price

    # print(price)
    # print(user.account)
    money = user.account
    if user.account >= price:
        user.account -= price
        user.save()
        for order in user.order_set.all():
            order.delete()
        return render(request, 'coffeemachine/payment.html', context={})
    else:
        error = 'У вас недостатньо коштів на рахунку, поповніть'
        return render(request, 'coffeemachine/add_money.html', context={'error': error, 'money': money})

@login_required
def clear_order(request):
    user = CoffeeUser.objects.filter(user=request.user).first()
    coffeemachine = CoffeMachine.objects.first()

    for order in user.order_set.all():
        drink = order.drink
        drinklist = coffeemachine.drinklist_set.filter(drink=drink).first()
        drinklist.count += 1
        drinklist.save()

        for ingredient in order.ingredients.get_queryset():
            ingredientlists = coffeemachine.ingredientlist_set
            ingredientlist = ingredientlists.filter(ingredient=ingredient).first()
            ingredientlist.count += 1
            ingredientlist.save()

        order.delete()
    return redirect(reverse('index'))

@login_required
def add_money(request):
    user = CoffeeUser.objects.filter(user=request.user).first()
    money = user.account
    # print(money)
    if request.method == 'POST':
        user.account += int(request.POST.get('count'))
        user.save()
    return render(request, 'coffeemachine/add_money.html', context={'money': money})

@staff_member_required
def full_machine(request):

    if request.method == 'POST':
        coffeemachine = CoffeMachine.objects.first()
        for drinklist in coffeemachine.drinklist_set.all():
            drinklist.count = 10
            drinklist.save()

        for ingredientlist in coffeemachine.ingredientlist_set.all():
            ingredientlist.count = 20
            ingredientlist.save()

    return render(request, 'coffeemachine/full_machine.html', context={})
