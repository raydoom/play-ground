# coding=utf8

from django.urls import path

from app.user_jwt import views

urlpatterns = [
    path('v1.0/register/', views.RegisterView.as_view()),
    path('v1.0/login/', views.LoginView.as_view()),
    path('v1.0/get_user_info/', views.GetUserInfoView.as_view()),

]