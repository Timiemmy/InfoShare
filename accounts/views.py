from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CustomUser, Contact
from blog.models import Blog


def about(request, username):
    users = get_object_or_404(CustomUser, username=username)
    blogs = Blog.published.filter(author=users)
    return render(request, 'personal-alt.html', {
        'user': users,
        'blogs': blogs
    })
