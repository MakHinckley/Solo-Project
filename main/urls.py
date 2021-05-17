from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('registrationVal', views.registrationVal),
    path('loginVal', views.loginVal),
    path('homepage', views.homepage),
    path('parks', views.parks),
    path('logout', views.logout),
    path('user/edit', views.edit),
    path('user/account', views.userAcct),
    path('user/deletePage', views.deletePage),
    path('user/update', views.update),
    path('parks/<int:park_id>', views.parkPage),
]
