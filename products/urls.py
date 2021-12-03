from django.urls import path

from .views import ProductMainView

urlpatterns = [
    path('', ProductMainView.as_view())
]