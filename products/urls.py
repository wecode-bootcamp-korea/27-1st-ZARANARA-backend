from django.urls import path, re_path

from products.models import Product

from .views import ProductSlideView

urlpatterns = [
    path('/silde', ProductSlideView.as_view()),
]