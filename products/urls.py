from django.urls import path

from .views      import DetailView

urlpatterns = [
	path('/detail/<int:product_id>', DetailView.as_view())
]