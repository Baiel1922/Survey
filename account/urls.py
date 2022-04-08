
from django.urls import path

from .views import RegisterView, ActivationView, LoginView, LogoutView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view())
    ]

