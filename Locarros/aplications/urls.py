from django.contrib import admin
from django.urls import path, include
from aplications import views
from django.urls import path
from users.views import *



from django.views.generic import RedirectView

urlpatterns = [
    path('', views.index, name='index'),

    path("accounts/login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("register-submit/", register_submit, name="register-submit"),
    path("register_colaborador/", register_colaborador_submit, name="register_colaborador"),
    path("login-submit/", login_submit, name="login-submit"),
    path("logout/", logout_user, name="logout"),

    path("home/", views.home, name="home"),
    path('accounts/', include("allauth.urls")),

]