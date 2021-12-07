from django.urls    import path

from users.views    import LoginView, SignUpView
from products.views import SetProductDetailView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/setproducts', SetProductDetailView.as_view),
]
