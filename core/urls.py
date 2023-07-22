from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    index,
    add_post,
    delete_post,
    postsList,
    register,
    loginView,
    logout_view
)

urlpatterns = [
    path("", index, name="index"),
    path("add_post", add_post, name="add_post"),
    path('delete_post/<str:pk>/', delete_post, name='delete_post'),
    path('login/', loginView, name='login'),
    path('register/', register, name='register'),
    path('logout_view/', logout_view, name='logout_view'),
	path('post-list/', postsList, name="post-list"),
] + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)