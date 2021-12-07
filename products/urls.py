from django.urls import path

from .views      import ProductView, SetProductView

urlpatterns = [
	path('/detail/<int:product_id>', ProductView.as_view()),
	path('/set-detail/<int:product_id>', SetProductView.as_view())
]