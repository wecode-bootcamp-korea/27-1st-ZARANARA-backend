from django.urls import path

from .views import ProductSlideView

urlpatterns = [
    path('/slide', ProductSlideView.as_view()),
]