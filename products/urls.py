from django.urls import path

from .views import ProductListView, ProductSetListView, ProductThemeView

urlpatterns = [
    path('/theme', ProductThemeView.as_view()),
    path('/set',ProductSetListView.as_view()),
    path('/category/<int:category_id>', ProductListView.as_view())
]