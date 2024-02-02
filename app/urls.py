from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

    path('', views.dashboard, name='dashboard'),
    path('clinics-rooms/', views.clinics_rooms, name='clinics_and_rooms'),
    path('room-times/<int:room_id>/', views.room_times, name='room_times'),
    path('update_capacity/<int:room_id>/', views.update_capacity, name='update_capacity'),
    path('reserve_time/<int:room_id>/', views.reserve_time, name='reserve_time'),
]

