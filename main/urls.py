from django.urls import path
from . import views



urlpatterns = [
    path('login_page/', views.LoginPage, name = 'login_page'),
    path('register_page/', views.RegisterPage, name = 'register_page'),
    path('logout_page/', views.LogoutPage, name = 'logout_page'),
    path('topic_page/', views.TopicPage, name = 'topic_page'),
    path('activity_page/', views.ActivityPage, name = 'activity_page'),

    path('', views.home, name='home'),

    path('room/<str:pk>/', views.room, name = 'room'),
    path('user-profile/<str:pk>/',views.userProfile, name = "user-profile"),
    
    path('create-room/',views.createRoom, name = "create-room"),
    path('update-room/<str:pk>/',views.updateRoom, name = "update-room"),
    path('update-user/<str:pk>/',views.updateUser, name = "update-user"),
    path('delete-room/<str:pk>/',views.deleteRoom, name = "delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage, name = "delete-message"),

]
