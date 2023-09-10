from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import UserLoginForm, PostForm, UserProfileForm, CommentForm, UserProfileAddForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Post, Comment, ReplyComments, Likes_Unlikes, User_profiles
from .serializers import PostSerializer, ReplyCommentsSerializer, CommentSerializer, UserProfilesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden

def postDetails(request, pk):
    post = get_object_or_404(Post, post_id=pk)
    ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
    comments = Comment.objects.filter(post=pk)
    comments_count = Comment.objects.filter(post=pk).count()
    if request.user.is_authenticated:
        profile_user=User_profiles.objects.get(author=request.user)
    else:
        profile_user=None
    users=User_profiles.objects.all()
    reply_comments = ReplyComments.objects.filter(post=pk)
    try:
        user_has_liked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('like')[0]['like']
        user_has_unliked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('unlike')[0]['unlike']
    except:
        user_has_liked=0
        user_has_unliked=0
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
        'data':JsonResponse(data),
        'post': post,
        'comments': comments,
        'comments_count': comments_count,
        'reply_comments': reply_comments,
        'user_has_liked': user_has_liked,
        'user_has_unliked': user_has_unliked,
        'profile_user': profile_user,
        'users':users
    }
    return render(request, 'post_detail.html', context)

def index(request):
    search_query = request.GET.get('q')
    top_posts = Post.objects.order_by('-views')[:3]
    if request.user.is_authenticated:
        profile_user=User_profiles.objects.get(author=request.user)
    else:
        profile_user=None
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
        'top_posts': top_posts,
        'profile_user': profile_user,
    }
    return render(request, "index.html", context)

def index_by_tag(request, tag_slug):
    posts = Post.objects.filter(slug=tag_slug).order_by('-created')
    tags = Post.objects.order_by('slug').values_list('slug', flat=True).distinct()
    if request.user.is_authenticated:
        profile_user=User_profiles.objects.get(author=request.user)
    else:
        profile_user=None
    
    context = {
        'posts': posts,
        'tags': tags,
        'profile_user': profile_user,
    }

    return render(request, "index.html", context)

@login_required
def add_post(request):
    profile_user=User_profiles.objects.get(author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('index')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'profile_user': profile_user,
        }
    return render(request, 'add_post.html', context)

@login_required
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

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, post_id=pk)
    profile_user=User_profiles.objects.get(author=request.user)
    if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            form.instance.author = post.author
            if form.is_valid():
                form.save()
                return redirect('index')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post,
        'profile_user': profile_user,
        }
    return render(request, 'update_post.html', context)

@login_required
def user_profile(request):
    user = request.user
    profile_user, created = User_profiles.objects.get_or_create(author=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        profileaddform = UserProfileAddForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid() and profileaddform.is_valid():
            form.save()
            profileaddform.save()
            return redirect('user_profile')

    else:
        form = UserProfileForm(instance=user)
        profileaddform = UserProfileAddForm(instance=profile_user)
    
    context = {
        'user': user,
        'profile_user': profile_user,
        'form': form,
        'profileaddform': profileaddform
    }
    return render(request, 'user_profile.html', context)


@login_required
def user_room(request):
    user = request.user
    profile_user=User_profiles.objects.get(author=request.user)
    posts = Post.objects.filter(author=user).order_by('-created')
    context = {
        'user': user,
        'posts': posts,
        'profile_user': profile_user,
    }
    return render(request, 'user_room.html', context)

# def postDetails(request, pk):
#     post = get_object_or_404(Post, post_id=pk)
#     ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
#     comments = Comment.objects.filter(post=pk)
#     if request.user.is_authenticated:
#         profile_user=User_profiles.objects.get(author=request.user)
#     else:
#         profile_user=None
#     users=User_profiles.objects.all()
#     reply_comments = ReplyComments.objects.filter(post=pk)
#     try:
#         user_has_liked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('like')[0]['like']
#         user_has_unliked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('unlike')[0]['unlike']
#     except:
#         user_has_liked=0
#         user_has_unliked=0
#     data = {
#         'post': {
#             'title': post.title,
#             'created': post.created.strftime('%Y-%m-%d %H:%M:%S'),
#             'author': post.author.username,
#             'total_likes': post.total_likes,
#             'total_unlikes': post.total_unlikes,
#         },
#         'comments': [
#             {
#                 'author': comment.author.username,
#                 'created': comment.created.strftime('%Y-%m-%d %H:%M:%S'),
#                 'content': comment.content,
#                 'reply_comments': [
#                     {
#                         'author': r_comment.author.username,
#                         'created': r_comment.created.strftime('%Y-%m-%d %H:%M:%S'),
#                         'content': r_comment.content,
#                     }
#                     for r_comment in reply_comments if r_comment.parent_comment_id == comment.id
#                 ],
#             }
#             for comment in comments
#         ],
#     }
    
#     if ip_address not in post.viewed_ips:
#         post.views += 1 
#         post.viewed_ips.append(ip_address)
#         post.save()
#     comments = post.comment_set.all().order_by('-created')
#     reply_comments = ReplyComments.objects.all().order_by('-created')

#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             if 'content' in request.POST:
#                 content = request.POST['content']
#                 Comment.objects.create(post=post, author=request.user, content=content)
#             if 'reply_content' in request.POST:
#                 parent_comment_id = request.POST.get('parent_comment_id')
#                 parent_comment = get_object_or_404(Comment, id=parent_comment_id)
#                 content = request.POST.get('reply_content')
#                 ReplyComments.objects.create(parent_comment=parent_comment, post=post, author=request.user, content=content)

#     context = {
#         'data':JsonResponse(data),
#         'post': post,
#         'comments': comments,
#         'reply_comments': reply_comments,
#         'user_has_liked': user_has_liked,
#         'user_has_unliked': user_has_unliked,
#         'profile_user': profile_user,
#         'users':users
#     }

#     return render(request, 'post_detail.html', context)

def share_on_facebook(request):
    current_url = request.build_absolute_uri()
    facebook_share_url = f'https://www.facebook.com/sharer/sharer.php?u={current_url}'
    return redirect(facebook_share_url)

# @login_required                                                                                      
# def add_comment(request, pk):
#     post = get_object_or_404(Post, post_id=pk)

#     if request.method == 'POST':
#         if 'add_comment' in request.POST:
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.post = post
#                 comment.author = request.user
#                 comment.save()
#                 return redirect('postDetails', pk=pk)
#         elif 'add_reply' in request.POST: 
#             parent_comment_id = request.POST.get('parent_comment_id')
#             parent_comment = get_object_or_404(Comment, id=parent_comment_id)
#             content = request.POST.get('reply_content')
#             ReplyComments.objects.create(parent_comment=parent_comment, post=post, author=request.user, content=content)
#             return redirect('postDetails', pk=pk)
#     else:
#         form = CommentForm()

#     context = {
#         'post': post,
#         'form': form,
#     }

#     return render(request, 'post_detail.html', context)

# @login_required
# def edit_comment(request, pk, comment_id):
#     post = get_object_or_404(Post, post_id=pk)

#     if request.method == 'POST':
#         if 'edit_comment' in request.POST:
#             comment = get_object_or_404(Comment, id=comment_id)
#             comment_id = request.POST.get('comment_id')
#             form = CommentForm(request.POST, instance=comment)
#             if form.is_valid():
#                 form.save()
#                 return redirect('postDetails', pk=pk)
#         if 'edit_reply_comment' in request.POST:
#             comment = get_object_or_404(ReplyComments, id=comment_id)
#             comment_id = request.POST.get('comment_id')
#             form = CommentForm(request.POST, instance=comment)
#             if form.is_valid():
#                 form.save()
#                 return redirect('postDetails', pk=pk)

#     else:
#         form = CommentForm(instance=comment)

#     context = {
#         'post': post,
#         'form': form,
#         'comment': comment,
#     }

#     return render(request, 'post_detail.html', context)

# @login_required
# def delete_comment(request, pk, comment_id):
#     if request.method == 'POST':
#         if 'delete_comment' in request.POST:
#             comment = get_object_or_404(Comment, id=comment_id)

#             # Delete child comments of the parent comment
#             child_comments = ReplyComments.objects.filter(parent_comment=comment)
#             child_comments.delete()

#             comment.delete()
#             return redirect('postDetails', pk=pk)
#         if 'delete_reply_comment' in request.POST:
#             comment = get_object_or_404(ReplyComments, id=comment_id)
#             comment.delete()
#             return redirect('postDetails', pk=pk)
#     else:
#         return HttpResponseBadRequest("Invalid request method.")

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
def postDetail(request, pk):
    data = {}  
    try:
        post = Post.objects.get(post_id=pk)
    except Post.DoesNotExist:
        return HttpResponseBadRequest("Invalid request method.")
    post_serializer = PostSerializer(post)
    data = post_serializer.data
    comments = Comment.objects.filter(post=post)
    comments_serializer = CommentSerializer(comments, many=True)
    data['comments'] = comments_serializer.data

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_profile = User_profiles.objects.get(author_id=request.user.id)
        user_authenticated_data = UserProfilesSerializer(user_profile).data
        data['user_authenticated'] = user_authenticated_data['author']
        try:
            user_has_liked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('like')[0]['like']
            user_has_unliked = Likes_Unlikes.objects.filter(author=request.user, post=pk).values('unlike')[0]['unlike']
        except:
            user_has_liked=0
            user_has_unliked=0
        data['user_has_liked'] = user_has_liked
        data['user_has_unliked'] = user_has_unliked
    else:
        data['user_authenticated'] = None

    # Retrieve replyComments and organize them under their parent comments
    for comment_data in data['comments']:
        comment_id = comment_data['id']
        reply_comments = ReplyComments.objects.filter(parent_comment=comment_id)
        reply_comments_serializer = ReplyCommentsSerializer(reply_comments, many=True)
        comment_data['replyComments'] = reply_comments_serializer.data
        # Fetch user's profile data for the comment
        user_profile = User_profiles.objects.get(author=comment_data['author'])
        user_profile_serializer = UserProfilesSerializer(user_profile)
        comment_data['comment_Author_Profile'] = user_profile_serializer.data
        # Fetch user's profile data for each reply comment
        for reply_comment_data in comment_data['replyComments']:
            user_profile = User_profiles.objects.get(author=reply_comment_data['author'])
            user_profile_serializer = UserProfilesSerializer(user_profile)
            reply_comment_data['reply_Author_Profile'] = user_profile_serializer.data
    
    # Fetch profile data of Author of Post
    user_profile = User_profiles.objects.get(author=post.author)
    user_profile_serializer = UserProfilesSerializer(user_profile)
    data['post_Author_Profile'] = user_profile_serializer.data

    return Response(data)

@api_view(['POST'])
def create_comment(request):
    if request.method == 'POST':
        new_serializer = CommentSerializer(data=request.data)
        if new_serializer.is_valid():
            new_serializer.save()
            return Response(new_serializer.data, status=201)
        return Response(new_serializer.errors, status=400)
    
@api_view(['DELETE'])
def delete_comments(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    reply_comments = ReplyComments.objects.filter(parent_comment=pk)

    if request.method == 'DELETE':
        for reply_comment in reply_comments:
            # Delete replies of the main comment
            reply_comment.delete()

        # Delete the main comment
        comment.delete()
        
        return Response('Comment with all Replies successfully deleted!')
    else:
        return Response('Invalid HTTP method')
    
@api_view(['POST'])
def create_reply_comment(request):
    if request.method == 'POST':
        new_serializer = ReplyCommentsSerializer(data=request.data)
        if new_serializer.is_valid():
            new_serializer.save()
            return Response(new_serializer.data, status=201)
        return Response(new_serializer.errors, status=400)
    
@api_view(['DELETE'])
def delete_reply_comments(request, pk):
    try:
        reply_comment = ReplyComments.objects.get(id=pk)
    except ReplyComments.DoesNotExist:
        return Response("Reply comment does not exist")

    if request.method == 'DELETE':
        # Delete reply comment
        reply_comment.delete()
        return Response("Reply comment successfully deleted")
    else:
        return Response("Invalid HTTP method")

@api_view(['POST'])
def update_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({"message": "Comment does not exist"})

    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
    

@api_view(['POST'])
def update_reply_comment(request, pk):
    try:
        reply_comment = ReplyComments.objects.get(pk=pk)
    except ReplyComments.DoesNotExist:
        return Response({"message": "Replycomment does not exist"})

    serializer = ReplyCommentsSerializer(reply_comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
    

@login_required
def like_unlike_post(request, pk):
    if request.method == 'POST':
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
        return JsonResponse({'error': 'Invalid request method'})



def contact(request):
    if request.user.is_authenticated:
        profile_user=User_profiles.objects.get(author=request.user)
    else:
        profile_user=None
    context = {
        'profile_user': profile_user,
        }

    return render(request, 'contact.html', context)

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

def Not_Found(request):
    return render(request, '404.html')

def page_faq(request):
    if request.user.is_authenticated:
        profile_user=User_profiles.objects.get(author=request.user)
    else:
        profile_user=None
    return render(request, 'faq.html',{'profile_user': profile_user})