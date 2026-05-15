# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserCreateView, email_verification, UserProfileUpdateView

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserCreateView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', LogoutView.as_view(
        next_page='catalog:home'
    ), name='logout'),
    path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
]



# urlpatterns = [
#     # Регистрация
#     path('register/', UserCreateView.as_view(), name='register'),
#
#     # Авторизация (логин)
#     path('login/', LoginView.as_view(
#         template_name='users/login.html',
#         redirect_authenticated_user=True,  # если уже залогинен — не показывать форму
#     ), name='login'),
#
#     # Выход
#     path('logout/', LogoutView.as_view(
#         next_page='catalog:home'  # после выхода кидает на главную
#     ), name='logout'),
   # path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
# ]
