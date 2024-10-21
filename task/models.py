from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    attachments = ArrayField(
        models.CharField(max_length=900),
        blank = True,
        default = list
    )
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'tasks')
    tags = models.ManyToManyField(Tag, related_name = 'tasks')

    def __str__(self):
        return self.title
