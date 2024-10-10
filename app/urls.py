from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('validate/', views.validate_license, name='validate_license'),
    path('create/', views.create_license, name='create_license'),
    path('revoke/', views.revoke_license, name='revoke_license'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
