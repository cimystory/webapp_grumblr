from django.db import models
from django.db.models import Max
from django.utils.html import escape
from django.template.loader import render_to_string

# User class for built-in authentication module
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(time__gt=time).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_items(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(deleted=False,
                                   time__gt=time).distinct()

    # Generates the HTML-representation of a single to-do list item.
    @property
    def html(self):
        return render_to_string("grumblr/posts.html", {"post": self}).replace("\n","")

    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(Max('time'))['time__max'] or "1970-01-01T00:00+00:00"

    def __str__(self):
        return self.text

# User information Model
class UserInfo(models.Model):
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to = "profile_pictures", blank = True)
    age = models.CharField(max_length=20, default='', blank=True)
    bio = models.CharField(max_length=420, default='', blank=True)
    firstname = models.CharField(max_length = 20, default= '', blank = True)
    lastname = models.CharField(max_length = 20, default= '', blank = True)
    followee = models.ManyToManyField(User, related_name='followee')
    password = models.CharField(max_length = 40, default = '', blank = True)
    token = models.CharField(max_length = 200, blank = True)

    def __str__(self):
        return self.firstname

class Comment(models.Model):
    text = models.CharField(max_length=200)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User, null = True, blank = True)
    time = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(post_id, time="1970-01-01T00:00+00:00"):
        post = Post.objects.get(id = post_id)
        return Comment.objects.filter(post = post, time__gt=time).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_comments(post_id, time="1970-01-01T00:00+00:00"):
        post = Post.objects.get(id=post_id)
        return Comment.objects.filter(post = post, deleted=False,
                                   time__gt=time).distinct()

    # Generates the HTML-representation of a single to-do list item.
    @property
    def html(self):
        return render_to_string("grumblr/comments.html", {"comment": self}).replace("\n", "")

    @staticmethod
    def get_max_time():
        return Comment.objects.all().aggregate(Max('time'))['time__max'] or "1970-01-01T00:00+00:00"

    def __str__(self):
        return self.text