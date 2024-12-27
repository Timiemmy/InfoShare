from django.shortcuts import render
from django.db.models import Sum
from blog.models import Blog, Category, Comment


def home(request):
    total_views = Blog.objects.filter(author=request.user).aggregate(
        total_views=Sum('views'))['total_views']
    total_comments = Comment.objects.filter(post__author=request.user).count()
    total_post = Blog.objects.filter(author=request.user).count()
    posts = Blog.objects.filter(author=request.user).order_by('-created_at')

    context = {
        'total_views': total_views,
        'total_comments': total_comments,
        'total_post': total_post,
        'posts': posts}
    return render(request, 'dashboard/dash.html', context)


def blog(request):
    post = Blog.objects.filter(author=request.user).order_by('-created_at')

    context = {'post': post}
    return render(request, 'dashboard/dash_blog.html', context)


def comment(request):
    comment = Comment.objects.select_related('post').order_by('-created_at')
    context = {'comment': comment}
    return render(request, 'dashboard/comments.html', context)


def pages(request):
    return render(request, 'dashboard/pages.html')


def pages(request):
    return render(request, 'dashboard/account.html')
