from django.urls import path
from . import views


urlpatterns = [
    path('', views.reservation, name='reservation'),
    path('add_reservation/<int:product_id>/', views.add_reservation, name='add_reservation'),
    path('remove_reservation/<int:product_id>/<int:reservation_item_id>/', views.remove_reservation, name='remove_reservation'),
    path('remove_reservation_item/<int:product_id>/<int:reservation_item_id>/', views.remove_reservation_item, name='remove_reservation_item'),
    
    path('checkout/', views.checkout, name='checkout'),
]
