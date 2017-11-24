# -*- coding: utf-8 -*-

from django.db import models


class Ytcomment(models.Model):
    channel_id = models.CharField(max_length=100, default='', null=True)
    video_id = models.CharField(max_length=100, default='', null=True)
    comment_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    video = models.CharField(max_length=100, default="", null=True)


class Fbpost(models.Model):
    page_id = models.CharField(max_length=100, default='', null=True)
    post_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    pagename = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)

    def __repr__(self):
        return self.post_id if self.post_id else "FBPOST"

    def __unicode__(self):
        return self.post_id if self.post_id else "FBPOST"


class Fbcomment(models.Model):
    page_id = models.CharField(max_length=100, default='', null=True)
    comment_id = models.CharField(max_length=100, default='', null=True)
    post_id = models.CharField(max_length=100, default='', null=True)
    user_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)

    def __repr__(self):
        return self.comment_id if self.comment_id else "FBCOMMENT"

    def __unicode__(self):
        return self.comment_id if self.comment_id else "FBCOMMENT"


class Tweet(models.Model):
    user_id = models.CharField(max_length=100, default='', null=True)
    tweet_id = models.CharField(max_length=100, default='', null=True)
    message=models.TextField(default="", null=True)
    username=models.CharField(max_length=100, default="", null=True)
    timestamp=models.DateTimeField(unique=False)
    
    def __repr__(self):
        return str(self.tweet_id) + ': ' + str(self.timestamp)

    def __unicode__(self):
        return str(self.tweet_id) + ': ' + str(self.timestamp)
