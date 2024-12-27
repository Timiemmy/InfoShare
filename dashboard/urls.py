from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='dashboard'),
    path('blog', views.blog, name='dash_blog'),
    path('comment', views.comment, name='dash_comment'),
    path('pages', views.pages, name='dash_pages'),
    path('my-account', views.pages, name='dash_account'),
]