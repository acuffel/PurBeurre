from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('search', views.search, name='search'),
    path('<product_id>', views.detail, name='detail'),
    path('substitute/<product_id>', views.substitute, name='substitute'),
    path('favorites/<sub_id>', views.save, name='save'),
]
