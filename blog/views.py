from django.shortcuts import render, redirect
from blog.models import BlogPost


def create_blogpost_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    return render(request, 'blog/create_blogpost.html')
