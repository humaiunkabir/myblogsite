import email
from email.mime import image
from msilib.schema import ODBCAttribute
from sqlite3 import Timestamp
from tkinter import CASCADE
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class author(models.Model):
    DEFAULT = 'defaultuser.png'
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(default=DEFAULT)
    detals = models.TextField()

    def __str__(self):
        return self.name.username


class category(models.Model):
    name = models.CharField(max_length=100)
    catcolor = models.CharField(max_length=100, default='red')

    def __str__(self) -> str:
        return self.name


class article(models.Model):
    DEFAULT = 'default.jpg'
    article_author = models.ForeignKey(author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.FileField(default=DEFAULT)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    postdate = models.DateField(default=Timestamp.now)

    def __str__(self) -> str:
        return f'{self.title} => {self.category}'



class comment(models.Model):
    post = models.ForeignKey(article, on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    post_comment = models.TextField()

    def __str__(self) -> str:
        return self.post.title