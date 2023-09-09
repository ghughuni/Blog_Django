from rest_framework import serializers
from .models import Post, Comment, ReplyComments, Likes_Unlikes, User_profiles

class ReplyCommentsSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_profile_image_url = serializers.SerializerMethodField()
    
    def get_author_profile_image_url(self, obj):
        try:
            user_profile = User_profiles.objects.get(author=obj.author)
            if user_profile.profile_images:
                return user_profile.profile_images.url
        except User_profiles.DoesNotExist:
            pass  # Handle the case where the user profile does not exist or does not have a profile image
        return None

    class Meta:
        model = ReplyComments
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    reply_comments = ReplyCommentsSerializer(many=True, read_only=True)
    author_profile_image_url = serializers.SerializerMethodField()
    
    def get_author_profile_image_url(self, obj):
        try:
            user_profile = User_profiles.objects.get(author=obj.author)
            if user_profile.profile_images:
                return user_profile.profile_images.url
        except User_profiles.DoesNotExist:
            pass  # Handle the case where the user profile does not exist or does not have a profile image
        return None

    class Meta:
        model = Comment
        fields = '__all__'


class LikesUnlikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes_Unlikes
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'

class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_profiles
        fields = '__all__'