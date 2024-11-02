from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


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

