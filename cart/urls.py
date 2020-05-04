from django.urls import path
from . import views



urlpatterns = [
    path('<int:product_id>/add', views.cart_add, name='cart_add'),
    
]