
from django.db import models


class Ytcomment(models.Model):
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=True)
    video = models.CharField(max_length=100, default="", null=True)
    channel = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return str(self.username) + ": " + str(self.message)

class Fbpost(models.Model):
    content = models.TextField(default="", null=True)
    pagename = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=True)
    
    def __str__(self):
        return self.pagename.encode('utf-8') + ": " + str(self.timestamp)


class Fbcomment(models.Model):
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField(unique=True)
    # post = models.ForeignKey(Fbpost, on_delete=models.CASCADE)

    def __repr__(self):
        return str(self.username) + ": " + str(self.message)


class ObjectHash(models.Model):
    hash_value = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return self.hash_value
