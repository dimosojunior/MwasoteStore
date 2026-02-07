
from django.urls import path
from . import views

urlpatterns = [
    
    
    path('', views.user_login, name="user_login"),
    path('registration/', views.registration, name="registration"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('options/', views.options, name="options"),
    path('maduka_yote/', views.maduka_yote, name="maduka_yote"),
    path("users/", views.users_list, name="users_list"),

    



]