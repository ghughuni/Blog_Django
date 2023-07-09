from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    posts=Post.objects.all().order_by('-created')
    context = {
        'posts': posts
    }

    return render(request, "index.html", context)

from .forms import PostForm

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'add_post.html', context)


    
@api_view(['GET'])
def postsList(request):
	posts = Post.objects.all()
	serializer = PostSerializer(posts, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def postDetail(request, pk):
	posts = Post.objects.get(post_id=pk)
	serializer = PostSerializer(posts, many=False)
	return Response(serializer.data)

def register(request):
    title = 'Create an account'
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and email and password1 and password2):
            messages.error(request, 'Please fill out all fields')
            return render(request, 'register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()
        
        return redirect('login')
    else:
        return render(request, 'register.html', {'title': title})

def loginView(request):

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        users = authenticate(username=username, password=password)
        login(request, users)
        return redirect('index')

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')