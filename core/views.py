from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import UserLoginForm, PostForm, UserProfileForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Post, Comment, ReplyComments, Likes_Unlikes
from .serializers import PostSerializer, ReplyCommentsSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import CommentForm
from django.urls import reverse
from django.http import HttpResponseForbidden

def index(request):
    search_query = request.GET.get('q')
    top_posts = Post.objects.order_by('-views')[:3]
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        ).order_by('-created')
    else:
        posts = Post.objects.all().order_by('-created')

    tags = Post.objects.order_by('slug').values_list('slug', flat=True).distinct()
    context = {
        'posts': posts,
        'tags': tags,
        'top_posts': top_posts
    }
    return render(request, "index.html", context)

def index_by_tag(request, tag_slug):
    posts = Post.objects.filter(slug=tag_slug).order_by('-created')
    tags = Post.objects.order_by('slug').values_list('slug', flat=True).distinct()
    
    context = {
        'posts': posts,
        'tags': tags,
    }

    return render(request, "index.html", context)

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('index')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'add_post.html', context)

def delete_post(request, pk):
    if request.method == 'POST':
        if 'delete_button' in request.POST:
            posts = get_object_or_404(Post, post_id=pk)

            # Delete all comments (parent and child) related to the post
            comments = Comment.objects.filter(post_id=pk)
            reply_comments = ReplyComments.objects.filter(post_id=pk)
            comments.delete()
            reply_comments.delete()

            posts.delete()
            return redirect('index') 
    else:
        return HttpResponseBadRequest("Invalid request method.")

def update_post(request, pk):
    post = get_object_or_404(Post, post_id=pk)

    if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            form.instance.author = post.author
            if form.is_valid():
                form.save()
                return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form, 'post': post})

@login_required
def user_page(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_page')

    else:
        form = UserProfileForm(instance=user)

    context = {
        'user': user,
        'posts': posts,
        'form': form,
    }
    return render(request, 'user_page.html', context)


def ajaxPostDetail(request, pk):
    post = get_object_or_404(Post, post_id=pk)
    ip_address = request.META.get('REMOTE_ADDR')
    comments = Comment.objects.filter(post=pk)
    reply_comments = ReplyComments.objects.filter(post=pk)
    data = {
        'post': {
            'title': post.title,
            'created': post.created.strftime('%Y-%m-%d %H:%M:%S'),
            'author': post.author.username,
            'total_likes': post.total_likes,
            'total_unlikes': post.total_unlikes,
        },
        'comments': [
            {
                'author': comment.author.username,
                'created': comment.created.strftime('%Y-%m-%d %H:%M:%S'),
                'content': comment.content,
                'reply_comments': [
                    {
                        'author': r_comment.author.username,
                        'created': r_comment.created.strftime('%Y-%m-%d %H:%M:%S'),
                        'content': r_comment.content,
                    }
                    for r_comment in reply_comments if r_comment.parent_comment_id == comment.id
                ],
            }
            for comment in comments
        ],
    }
    print(data)
    return JsonResponse(data)


def postDetails(request, pk):
    post = get_object_or_404(Post, post_id=pk)
    ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
    comments = Comment.objects.filter(post=pk)
    reply_comments = ReplyComments.objects.filter(post=pk)
    user_has_liked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('like')[0]['like']
    user_has_unliked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('unlike')[0]['unlike']
    data = {
        'post': {
            'title': post.title,
            'created': post.created.strftime('%Y-%m-%d %H:%M:%S'),
            'author': post.author.username,
            'total_likes': post.total_likes,
            'total_unlikes': post.total_unlikes,
        },
        'comments': [
            {
                'author': comment.author.username,
                'created': comment.created.strftime('%Y-%m-%d %H:%M:%S'),
                'content': comment.content,
                'reply_comments': [
                    {
                        'author': r_comment.author.username,
                        'created': r_comment.created.strftime('%Y-%m-%d %H:%M:%S'),
                        'content': r_comment.content,
                    }
                    for r_comment in reply_comments if r_comment.parent_comment_id == comment.id
                ],
            }
            for comment in comments
        ],
    }
    # print(data)
    
    if ip_address not in post.viewed_ips:
        post.views += 1 
        post.viewed_ips.append(ip_address)
        post.save()
    comments = post.comment_set.all().order_by('-created')
    reply_comments = ReplyComments.objects.all().order_by('-created')

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'content' in request.POST:
                content = request.POST['content']
                Comment.objects.create(post=post, author=request.user, content=content)
            if 'reply_content' in request.POST:
                parent_comment_id = request.POST.get('parent_comment_id')
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)
                content = request.POST.get('reply_content')
                ReplyComments.objects.create(parent_comment=parent_comment, post=post, author=request.user, content=content)

    context = {
        'data':data,
        'post': post,
        'comments': comments,
        'reply_comments': reply_comments,
        'user_has_liked': user_has_liked,
        'user_has_unliked': user_has_unliked

    }
    # return JsonResponse(context)
    return render(request, 'post_detail.html', context)

def share_on_facebook(request):
    current_url = request.build_absolute_uri()
    facebook_share_url = f'https://www.facebook.com/sharer/sharer.php?u={current_url}'
    return redirect(facebook_share_url)
                                                                                         
def add_comment(request, pk):
    post = get_object_or_404(Post, post_id=pk)

    if request.method == 'POST':
        if 'add_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('postDetails', pk=pk)
        elif 'add_reply' in request.POST: 
            parent_comment_id = request.POST.get('parent_comment_id')
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)
            content = request.POST.get('reply_content')
            ReplyComments.objects.create(parent_comment=parent_comment, post=post, author=request.user, content=content)
            return redirect('postDetails', pk=pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'post_detail.html', context)


def edit_comment(request, pk, comment_id):
    post = get_object_or_404(Post, post_id=pk)

    if request.method == 'POST':
        if 'edit_comment' in request.POST:
            comment = get_object_or_404(Comment, id=comment_id)
            comment_id = request.POST.get('comment_id')
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('postDetails', pk=pk)
        if 'edit_reply_comment' in request.POST:
            comment = get_object_or_404(ReplyComments, id=comment_id)
            comment_id = request.POST.get('comment_id')
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('postDetails', pk=pk)

    else:
        form = CommentForm(instance=comment)

    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }

    return render(request, 'post_detail.html', context)

def delete_comment(request, pk, comment_id):
    if request.method == 'POST':
        if 'delete_comment' in request.POST:
            comment = get_object_or_404(Comment, id=comment_id)

            # Delete child comments of the parent comment
            child_comments = ReplyComments.objects.filter(parent_comment=comment)
            child_comments.delete()

            comment.delete()
            return redirect(reverse ('postDetails', args=[pk]))
        if 'delete_reply_comment' in request.POST:
            comment = get_object_or_404(ReplyComments, id=comment_id)
            comment.delete()
            return redirect(reverse ('postDetails', args=[pk]))
    else:
        return HttpResponseBadRequest("Invalid request method.")

@api_view(['GET'])
def postsList(request):
    posts = Post.objects.all()
    posts_serializer = PostSerializer(posts, many=True)
    return Response(posts_serializer.data)

@api_view(['GET'])
def commentsList(request):
    comments = Comment.objects.all()
    comments_serializer = CommentSerializer(comments, many=True)
    return Response(comments_serializer.data)

@api_view(['GET'])
def replyCommentsList(request):
    replyComments = ReplyComments.objects.all()
    replyComments_serializer = ReplyCommentsSerializer(replyComments, many=True)
    return Response(replyComments_serializer.data)

@api_view(['GET'])
def allDataList(request):
    posts = Post.objects.all()

    # Serialize the posts
    posts_serializer = PostSerializer(posts, many=True)
    data = posts_serializer.data

    # Retrieve and serialize comments and replyComments
    for post_data in data:
        post_id = post_data['post_id']

        # Retrieve comments for the current post
        comments = Comment.objects.filter(post=post_id)
        comments_serializer = CommentSerializer(comments, many=True)
        post_data['comments'] = comments_serializer.data

        # Retrieve replyComments and organize them under their parent comments
        for comment_data in post_data['comments']:
            comment_id = comment_data['id']
            reply_comments = ReplyComments.objects.filter(parent_comment=comment_id)
            reply_comments_serializer = ReplyCommentsSerializer(reply_comments, many=True)
            comment_data['replyComments'] = reply_comments_serializer.data

    return Response(data)


@api_view(['GET'])
def postDetail(request, pk):
    try:
        post = Post.objects.get(post_id=pk)
    except Post.DoesNotExist:
        return HttpResponseBadRequest("Invalid request method.")

    post_serializer = PostSerializer(post)
    data = post_serializer.data

    # Retrieve comments for the current post
    comments = Comment.objects.filter(post=post)
    comments_serializer = CommentSerializer(comments, many=True)
    data['comments'] = comments_serializer.data

    # Retrieve replyComments and organize them under their parent comments
    for comment_data in data['comments']:
        comment_id = comment_data['id']
        reply_comments = ReplyComments.objects.filter(parent_comment=comment_id)
        reply_comments_serializer = ReplyCommentsSerializer(reply_comments, many=True)
        comment_data['replyComments'] = reply_comments_serializer.data

    return Response(data)


def like_unlike_post(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_authenticated:
                    post = Post.objects.get(post_id=pk)
                    user = request.user
                    action, created = Likes_Unlikes.objects.get_or_create(post_id=post.post_id, author=user)
                    if 'like-button' in request.POST:
                        if action.like==0 and action.unlike==0:
                            action.like = 1
                            action.unlike = 0
                            action.save()
                            post.total_likes += 1
                            post.save()
                        elif action.like==0 and action.unlike==1:
                            action.like = 1
                            action.unlike = 0
                            action.save()
                            post.total_likes += 1
                            post.total_unlikes -= 1
                            post.save()
                        else:
                            pass
                    elif 'unlike-button' in request.POST:
                        if action.like==0 and action.unlike==0:
                            action.like = 0
                            action.unlike = 1
                            action.save()
                            post.total_unlikes += 1
                            post.save()
                        elif action.like==1 and action.unlike==0:
                            action.like = 0
                            action.unlike = 1
                            action.save()
                            post.total_likes -= 1
                            post.total_unlikes += 1
                            post.save()
                        else:
                            pass

                    return redirect(postDetails, pk=pk)
        else:
            return JsonResponse({'error': 'User not authenticated'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



def contact(request):
    return render(request, 'contact.html')

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