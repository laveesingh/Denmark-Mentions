# -*- coding: utf-8 -*-

from django.db import models


class Ytcomment(models.Model):
    comment_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    video = models.CharField(max_length=100, default="", null=True)
    # channel = models.CharField(max_length=100, default="", null=True)

    # def __repr__(self):
        # try:
            # return self.username.encode('utf-8') + ": " + self.message.encode('utf-8')
        # except:
            # return "YTCOMMENT"

    # def __unicode__(self):
        # try:
            # return self.username.encode('utf-8') + ": " + self.message.encode('utf-8')
        # except:
            # return "YTCOMMENT"


class Fbpost(models.Model):
    post_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    pagename = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    
    # def __repr__(self):
        # try:
            # return self.pagename.encode('utf-8') + ": " + self.timestamp.encode('utf-8')
        # except:
            # return "FBPOST"

    # def __unicode__(self):
        # return self.pagename.encode('utf-8') + ": " + self.timestamp.encode('utf-8')


class Fbcomment(models.Model):
    comment_id = models.CharField(max_length=100, default='', null=True)
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=False)
    # post = models.ForeignKey(Fbpost, on_delete=models.CASCADE)

    # def __repr__(self):
        # try:
            # return self.username.encode('utf-8') + ": " + self.message.encode('utf-8')
        # except:
            # return "FBCOMMENT"


    # def __unicode__(self):
        # return self.username.encode('utf-8') + ": " + self.message.encode('utf-8')


class ObjectHash(models.Model):
    hash_value = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return self.hash_value
