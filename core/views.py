from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import redirect

def index(request):
    posts=Post.objects.all()
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

def logout_view(request):
    logout(request)
    return redirect('/')