from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    index,
    add_post,
    postsList,
    postDetail,

)

urlpatterns = [
    path("", index, name="index"),
    path("add_post", add_post, name="add_post"),
	path('post-list/', postsList, name="post-list"),
	path('post-detail/<str:pk>/', postDetail, name="post-detail"),
] + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)