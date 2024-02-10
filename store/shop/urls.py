from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('category/', views.category, name='category'),
    path('<slug:category>/subcategory/',
         views.subcategory, name='subcategory'),
    path('add_to_cart/<int:product_id>/<int:quantity>/',
         views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/<int:cart_item_id>/<int:new_quantity>/',
         views.update_cart_item, name='update_cart_item'),
    path('remove_from_cart/<int:cart_item_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('cart_sum/', views.cart_sum, name='cart_sum'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
]
