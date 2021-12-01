from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_event, name='logout'),
    path('register/', views.register_page, name='register'),
    path('profile/<str:pk>', views.user_profile, name='profile'),
    path('update-user/', views.update_user, name='update-user'),
    path('room/<str:pk>/', views.room_page, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),

]