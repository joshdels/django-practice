from rest_framework import serializers

from .models import Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'body', 'create_at')
        model = Post
        
        