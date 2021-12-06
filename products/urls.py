from django.urls import path

from .views import ProductThemeView

urlpatterns = [
    path('/theme', ProductThemeView.as_view()),
]