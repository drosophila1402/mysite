from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('info', views.info_index, name='info_index'),
    path('info/<int:info_id>', views.info_detail, name='info_detail'),
    path('info/category/<int:category_id>', views.info_category, name='info_category'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),

    path('login', views.Account_login.as_view(), name='login'),
    path('signup', views.Create_account.as_view(), name='signup'),
    
    path('account', views.account, name='account'),
    path('account/delete', views.account_delete, name="account_delete"),
    path('account/info', views.account_info, name='account_info'),
    path('account/edit', views.account_edit, name='account_edit'),
    path('account/delete', views.account_delete, name='account_delete'),
    
    path('shop', views.shop, name='shop'),
    path('shop/category/<int:category_id>', views.category, name='category'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
    
    path('favorite/<int:product_id>', views.favorite_product, name='favorite'),
    path('unfavorite/<int:product_id>', views.unfavorite_product, name='unfavorite'),
    path('favorites', views.faved_products, name='faved_products'),
    
    path('cart', views.cart, name='cart'),
    path('cart/<int:product_id>/add', views.cart_add, name='cart_add'),
    path('cart/<int:product_id>/<int:number>/update', views.cart_update, name='cart_update'),
    path('cart/<int:product_id>/delete', views.cart_delete, name='cart_delete'),
    
    
]