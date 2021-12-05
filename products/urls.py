from django.urls import path, re_path

from products.models import Product

from .views import ProductMainView

urlpatterns = [
    path('', ProductMainView.as_view()),
]