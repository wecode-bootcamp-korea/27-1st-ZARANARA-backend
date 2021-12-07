from django.urls import path

from .views import ProductListView, ProductSetListView

urlpatterns = [
    path('/set',ProductSetListView.as_view()),
    path('', ProductListView.as_view()),
]