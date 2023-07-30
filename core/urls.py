from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    index,
    add_post,
    delete_post,
    update_post,
    postsList,
    register,
    loginView,
    logout_view,
    user_page,
    contact,
    index_by_tag,
    postDetails
)

urlpatterns = [
    path("", index, name="index"),
    path("add_post", add_post, name="add_post"),
    path('delete_post/<str:pk>/', delete_post, name='delete_post'),
    path('update/<str:pk>/', update_post, name='update_post'),
    path('user_page/', user_page, name='user_page'),
    path('post/<str:pk>/', postDetails, name='postDetails'),
    path('login/', loginView, name='login'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('logout_view/', logout_view, name='logout_view'),
	path('post-list/', postsList, name="post-list"),
    path('tag/<str:tag_slug>/', index_by_tag, name='index_by_tag'),
] + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)