from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('events/<int:event_id>/buy/', views.buy_ticket, name='buy_ticket'),
]
