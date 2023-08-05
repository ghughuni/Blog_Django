from rest_framework import serializers
from .models import Post, Comment, ReplyComments

class ReplyCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComments
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    reply_comments = ReplyCommentsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'
