from django.urls import path

from .views      import ProductView,ProductListView, ProductSetListView

urlpatterns = [
	path('/detail/<int:product_id>', ProductView.as_view()),
    path('/set',ProductSetListView.as_view()),
    path('', ProductListView.as_view()),
]