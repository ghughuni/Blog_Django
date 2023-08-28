from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_post", views.add_post, name="add_post"),
    path('delete_post/<str:pk>/', views.delete_post, name='delete_post'),
    path('update/<str:pk>/', views.update_post, name='update_post'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_room/', views.user_room, name='user_room'),
    path('post/<str:pk>/', views.postDetails, name='postDetails'),
    path('api-post/<str:pk>/', views.postDetail, name='postDetail'),
    path('login/', views.loginView, name='login'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('logout_view/', views.logout_view, name='logout_view'),
	path('api-posts/', views.postsList, name="postsList"),
    path('api-comments/', views.commentsList, name="commentsList"),
    path('api-replyComments/', views.replyCommentsList, name="replyCommentsList"),
    path('api-all-data/', views.allDataList, name="allDataList"),
    path('tag/<str:tag_slug>/', views.index_by_tag, name='index_by_tag'),
    path('post/<uuid:pk>/', views.add_comment, name='add_comment'),
    path('post/<uuid:pk>/<str:comment_id>', views.edit_comment, name='edit_comment'),
    path('post/<uuid:pk>/<str:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like_unlike_post/<uuid:pk>', views.like_unlike_post, name='like_unlike_post'),
    path('share/facebook/', views.share_on_facebook, name='share_facebook'),
    path('Not_Found/', views.Not_Found, name='Not_Found'),
    path('page_faq/', views.page_faq, name='page_faq'),

] + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)