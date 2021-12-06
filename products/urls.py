from django.urls import path

from .views import ProductSlideView

urlpatterns = [
    path('/theme', ProductSlideView.as_view()),
]