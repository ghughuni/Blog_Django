from django.db import models
from django.contrib.auth.models import User
import uuid
   
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='img', default='static/default-blog.png')
    body = models.TextField()
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug =models.SlugField()
    views = models.PositiveIntegerField(default=0)
    viewed_ips = models.JSONField(default=list)
    total_likes = models.PositiveIntegerField(default=0)
    total_unlikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title + '|' + str(self.author)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.created}"
    
class ReplyComments(models.Model):
    parent_comment=models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.created}"

class Likes_Unlikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.PositiveIntegerField(default=0)
    unlike = models.PositiveIntegerField(default=0)

class User_profiles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_images = models.ImageField(upload_to='img', default='static/profile_image.jpg')
    phone = models.CharField(max_length=20, default='(436) 486-3538')

    def __str__(self):
        return self.author.username
