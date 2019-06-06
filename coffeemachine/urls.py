
from django.urls import path
from django.urls import include
from coffeemachine.views import *


urlpatterns = [
    path('', index, name='index'),
    path('order/<str:id>/', order_drink, name='order_drink_url'),
    path('after_order/', after_order, name='after_order_url'),
    path('payment/', payment, name='payment_url'),
    path('clear_order/', clear_order, name='clear_order_url'),
    path('add_money/', add_money, name='add_money_url'),
    path('full_machine/', full_machine, name='full_machine_url'),

]
