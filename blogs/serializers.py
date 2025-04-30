from rest_framework import serializers
from .models import Blog, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['id', 'blog', 'comment']

class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True) # Nested serializer to include comments in the blog response and 
    # the name should be related_name of the foreign key in the Blog model
    class Meta:
        model = Blog
        fields = '__all__'
        # fields = ['id', 'blog_title', 'blog_body']
        # exclude = ['created_at', 'updated_at'] -> if you want to exclude fields


