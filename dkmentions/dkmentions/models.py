
from django.db import models


class Ytcomment(models.Model):
    message = models.TextField()
    username = models.CharField()
    timestamp = models.DateTimeField()
    video = models.CharField()
    channel = models.CharField()

    def __repr__(self):
        return str(username) + ": " + str(message)

class Fbpost(models.Model):
    content = models.TextField()
    pagename = models.CharField()
    timestamp = models.DateTimeField()


class FbComment(models.Model):
    message = models.TextField()
    username = models.CharField()
    timestamp = models.DateTimeField()
    post = models.ForeignKey(Fbpost, on_delete=models.CASCADE)

