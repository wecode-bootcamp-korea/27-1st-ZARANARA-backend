from django.urls import path

from users.views import LoginView, SignUpView, UserCartView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/cart', UserCartView.as_view()),
]
