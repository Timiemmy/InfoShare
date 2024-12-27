from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count
from .models import Blog, Category, Comment
from .forms import BlogForm


# Create your views here.

def home(request):
    category = Category.objects.all()

    context = {
        'category': category,
    }

    return render(request, 'headers.html', context)


def index(request):
    post = Blog.objects.order_by('-id')
    head_post = Blog.objects.order_by('-id').filter(main_post=True)
    recent = Blog.objects.all().order_by('-created_at')[:5]
    popular = Blog.objects.filter(section='Popular').order_by('id')[:5]
    category = Category.objects.annotate(post_count=Count('category'))

    context = {
        'posts': post,
        'head_post': head_post,
        'category': category,
        'recent': recent,
        'popular': popular,
    }

    return render(request, 'index.html', context)


def category(request, slug):
    category = Category.objects.all()
    blog_category = Category.objects.filter(slug=slug)

    context = {
        'blog_category': blog_category,
        'active_category': slug,
        'category': category,
    }
    return render(request, 'category.html', context)


def blog_detail(request, slug):
    # posts = Blog.objects.order_by('-id')
    category = Category.objects.all()
    posts = get_object_or_404(Blog, slug=slug)

    comments = Comment.objects.filter(post=posts).order_by('-created_at')

    context = {
        'posts': posts,
        'category': category,
        'comments': comments,
    }
    return render(request, 'blog_detail.html', context)


def add_comment(request, slug):

    if request.method == 'POST':
        post = get_object_or_404(Blog, slug=slug)
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        website = request.POST.get('InputWebsite')
        content = request.POST.get('InputContent')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        Comment.objects.create(
            post=post,
            email=email,
            website=website,
            name=name,
            content=content,
            parent=parent_comment,  # if parent comment exists, set it as parent comment
        )
        return redirect('blog_detail', slug=post.slug)
    return redirect('blog_detail')


def create_post(request):

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.created_at = timezone.now()
            blog.save()
            return redirect('blog_detail', slug=blog.slug)
        else:
            print(form.errors)
    else:
        form = BlogForm()
    return render(request, 'create_post.html', {'form': form})


def edit_post(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug)
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_detail', slug=blog.slug)
        else:
            print(form.errors)
    else:
        blog = get_object_or_404(Blog, slug=slug)
        form = BlogForm(instance=blog)
    return render(request, 'edit_post.html', {'form': form})


def delete_post(request, pk):
    blog = Blog.objects.get(pk=pk)
    blog.delete()
    return redirect('home')
