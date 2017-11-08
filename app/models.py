# -*- coding: utf-8 -*-

from django.db import models


class Ytcomment(models.Model):
    comment_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    video = models.CharField(max_length=100, default="", null=True)


class Fbpost(models.Model):
    post_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    pagename = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)

    def __repr__(self):
        return self.post_id if self.post_id else "FBPOST"

    def __unicode__(self):
        return self.post_id if self.post_id else "FBPOST"


class Fbcomment(models.Model):
    comment_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)

    def __repr__(self):
        return self.comment_id if self.comment_id else "FBCOMMENT"

    def __unicode__(self):
        return self.comment_id if self.comment_id else "FBCOMMENT"


class ObjectHash(models.Model):
    hash_value = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return self.hash_value
