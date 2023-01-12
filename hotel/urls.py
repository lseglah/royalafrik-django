from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel, name='hotel'),
    path('<slug:category_slug>/', views.hotel, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
