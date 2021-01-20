from rest_framework import serializers

from blog.models import Post
from blog.models import Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "author",
            "title",
            "text",
            "img_url",
            "publish_date"
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"