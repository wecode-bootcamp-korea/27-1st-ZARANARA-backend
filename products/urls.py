from django.urls import path

from .views      import ProductView,ProductListView, ProductSetListView, SetProductView, LikeToggleView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/set',ProductSetListView.as_view()),
	path('/detail/<int:product_id>', ProductView.as_view()),
	path('/set-detail/<int:product_id>', SetProductView.as_view()),
	path('/like/<int:product_id>', LikeToggleView.as_view())
]