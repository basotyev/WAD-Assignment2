from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from rest_framework import serializers


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PostManager(models.Manager):
    def published(self):
        return self.filter(published=True)

    def by_author(self, author_id):
        return self.filter(author_id=author_id, published=True)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    links = ArrayField(
        models.CharField(max_length=900),
        blank = True,
        default = list
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'posts')
    category = models.ManyToManyField(Category, related_name = 'posts')

    objects = PostManager()

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text[:20]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(many=True, read_only=True)
    links = serializers.ListField(
        child=serializers.CharField(max_length=900),
        allow_empty=True
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'created_at', 'published',
            'links', 'author', 'category'
        ]

    def create(self, validated_data):
        categories_data = self.initial_data.get('category', [])
        post = Post.objects.create(**validated_data)
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(name=category_data)
            post.category.add(category)
        return post

    def update(self, instance, validated_data):
        categories_data = self.initial_data.get('category', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.published = validated_data.get('published', instance.published)
        instance.links = validated_data.get('links', instance.links)
        instance.save()

        if categories_data:
            instance.category.clear()
            for category_data in categories_data:
                category, created = Category.objects.get_or_create(name=category_data)
                instance.category.add(category)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post']


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'comments']
