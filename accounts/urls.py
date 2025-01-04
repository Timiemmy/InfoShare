from django.urls import path
from . import views



urlpatterns = [
    path('<username>/', views.about, name='about'),
]
