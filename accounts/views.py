from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import CustomUser
from blog.models import Blog



def about(request, username):
    users = get_object_or_404(CustomUser, username=username)
    blogs = Blog.published.filter(author=users)
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.following.filter(id=users.id).exists()




    return render(request, 'personal-alt.html', {
        'user': users,
        'blogs': blogs,
        'is_following': is_following,
        'followers_count': users.user_followers.count(),
        'following_count': users.following.count(),
    })
'''
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if request.user.is_authenticated:
        if request.user.following.filter(id=user_id).exists():
            Follow.objects.create(follower=request.user, following = user_to_follow)
        else:
            Follow.objects.delete(id=user_id)
        return redirect('about')
'''


# views.py
from django.http import JsonResponse

@login_required
def follow_user(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(CustomUser, username=username)
        if request.user == user_to_follow:
            return JsonResponse({'error': 'You cannot follow yourself'}, status=400)

        try:
            if request.user.following.filter(id=user_to_follow.id).exists():
                request.user.following.remove(user_to_follow)
                is_following = False
            else:
                request.user.following.add(user_to_follow)
                is_following = True

            return JsonResponse({
                'success': True,
                'is_following': is_following,
                'followers_count': user_to_follow.user_followers.count(),
                'following_count': user_to_follow.following.count()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

