from django.urls import path

from .views      import SetProductDetailView

urlpatterns = [
	path('/detail/<int:product_id>', SetProductDetailView.as_view())
]