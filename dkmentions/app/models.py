
from django.db import models


class Ytcomment(models.Model):
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField()
    video = models.CharField(max_length=100, default="", null=True)
    channel = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return str(self.username) + ": " + str(self.message)

class Fbpost(models.Model):
    content = models.TextField(default="", null=True)
    pagename = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField()
    
    def __repr__(self):
        return str(self.pagename) + ": " + str(self.timestamp)


class Fbcomment(models.Model):
    message = models.TextField(default="", null=True)
    username = models.CharField(max_length=100, default="", null=True)
    timestamp = models.DateTimeField()
    # post = models.ForeignKey(Fbpost, on_delete=models.CASCADE)

    def __repr__(self):
        return str(self.username) + ": " + str(self.message)


class ObjectHash(models.Model):
    hash_value = models.CharField(max_length=100, default="", null=True)

    def __repr__(self):
        return self.hash_value
