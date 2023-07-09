from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    index,
    add_post,
    postsList,
    postDetail,
    logout_view

)

urlpatterns = [
    path("", index, name="index"),
    path("add_post", add_post, name="add_post"),
    path('logout_view/', logout_view, name='logout_view'),
	path('post-list/', postsList, name="post-list"),
	path('post-detail/<str:pk>/', postDetail, name="post-detail"),
] + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)