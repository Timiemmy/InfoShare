from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.postgres.search import SearchVector
from .models import Blog, Category, Comment
from .forms import BlogForm, SearchForm


# Create your views here.

def home(request):
    category = Category.objects.all()

    context = {
        'category': category,
    }

    return render(request, 'headers.html', context)


def index(request):
    post = Blog.published.order_by('-created_at')
    head_post = Blog.published.order_by('-id').filter(main_post=True)
    recent = Blog.published.all().order_by('-created_at')[:5]
    popular = Blog.published.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    category = Category.objects.annotate(post_count=Count('category'))
    most_liked = Blog.published.annotate(like_count=Count('likes')).order_by('-like_count')[:5]

    context = {
        'posts': post,
        'head_post': head_post,
        'category': category,
        'recent': recent,
        'popular': popular,
        'most_liked':most_liked,
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


def blog_like(request, post_slug):
    post = get_object_or_404(Blog, slug=post_slug)

    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        #return HttpResponseRedirect(reverse('blog_detail', args=[post.created_at.year, post.created_at.month, post.created_at.day, post.slug]))
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

    #return HttpResponseRedirect({'error': 'User not authenticated'}, status=401)
    return JsonResponse({'error': 'User not authenticated'}, status=401)


def blog_detail(request, year, month, day, slug):
    # posts = Blog.objects.order_by('-id')
    category = Category.objects.annotate(post_count=Count('category'))
    posts = get_object_or_404(
        Blog, slug=slug, created_at__year=year, created_at__month=month, created_at__day=day)

    comments = Comment.objects.filter(post=posts).order_by('-created_at')

    liked = False
    if request.user.is_authenticated and posts.likes.filter(id=request.user.id).exists():
        liked = True

    similar_posts = Blog.published.filter(category=posts.category).exclude(id=posts.id)[:1]

    def calculate_reading_time(text):
        words = len(text.split())
        return max(1, round(words / 200))

    reading_time = calculate_reading_time(posts.content)

    context = {
        'posts': posts,
        'category': category,
        'comments': comments,
        'reading_time': reading_time,
        'likes': liked,
        'total_likes': posts.total_likes(),
        'similar_posts': similar_posts,
    }
    return render(request, 'blog-single-alt.html', context)


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


def blog_search(request):
    form = SearchForm
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Blog.published.annotate(
                search=SearchVector('title')).filter(search=query)
    return render(request, 'search.html', {'form': form, 'query': query, 'results': results})


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


def contact(request):
    return render(request, 'contact.html')
