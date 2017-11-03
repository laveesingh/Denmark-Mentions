# -*- coding: utf-8 -*-

from django.db import models


class Ytcomment(models.Model):
    comment_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    video = models.CharField(max_length=100, default="", null=True)
    # channel = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return str(self.username) + ": " + str(self.message)

class Fbpost(models.Model):
    post_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    pagename = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    
    def __str__(self):
        return self.pagename.encode('utf-8') + ": " + str(self.timestamp)


class Fbcomment(models.Model):
    comment_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    # post = models.ForeignKey(Fbpost, on_delete=models.CASCADE)

    def __repr__(self):
        return str(self.username) + ": " + str(self.message)


class ObjectHash(models.Model):
    hash_value = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return self.hash_value
