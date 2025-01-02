from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',views.blog_detail, name='blog_detail'),
    path('search/', views.blog_search, name='blog_search'),
    path('like/<str:post_slug>', views.blog_like, name='post_like'),
    path('category/<str:slug>/', views.category, name='category'),
    path('<slug:slug>/add_comment', views.add_comment, name='add_comment'),
    path('add_new', views.create_post, name='create_post'),
    path('<str:slug>/edit', views.edit_post, name='edit_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    
    path('classic', views.classic, name='classic'),
    path('personal', views.personal, name='personal'),
    path('personal_alt', views.personal_alt, name='personal_alt'),
]
