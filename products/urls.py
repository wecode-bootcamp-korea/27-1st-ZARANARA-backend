from django.urls import path

from .views import ProductSetListView, ProductSlideView

urlpatterns = [
    path('/slide', ProductSlideView.as_view()),
    path('/setlist', ProductSetListView.as_view()),
]