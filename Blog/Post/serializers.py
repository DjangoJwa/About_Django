from rest_framework import serializers
from Post.models import Post

class PostSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=('id', 'title', 'text', )