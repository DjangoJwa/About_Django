from django.urls import path
from users.views import CreateUserAPIView
from users.views import authenticate_user

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('login/', authenticate_user),
]
