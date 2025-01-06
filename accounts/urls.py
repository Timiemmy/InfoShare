from django.urls import path
from . import views



urlpatterns = [
    path('<username>/', views.about, name='about'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]
