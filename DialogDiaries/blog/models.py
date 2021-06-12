from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-")
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_on']



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return self.content

class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Post_Tag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag


class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return self.email