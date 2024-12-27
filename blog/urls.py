from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('<str:slug>/', views.blog_detail, name='blog_detail'),
    path('category/<str:slug>/', views.category, name='category'),
    path('<slug:slug>/add_comment', views.add_comment, name='add_comment'),
    path('add_new', views.create_post, name='create_post'),
    path('<str:slug>/edit', views.edit_post, name='edit_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
]
