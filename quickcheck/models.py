import uuid

from django.db import models


class Base(models.Model):

    TYPE_CHOICES = [
        ("job", "job"),
        ("story", "story"),
        ("comment", "comment"),
        ("poll", "poll"),
        ("pollopt", "pollopt"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    HN_id = models.IntegerField(unique=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    by = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)

    class Meta:
        ordering = ["-time"]
    
    def __str__(self):
        return f"{self.type.capitalize()} by {self.by}"


class Job(Base):
    text = models.TextField(null=True)
    title = models.CharField(max_length=255, null=True)
    url = models.URLField(null=True)


class Story(Base):
    descendants = models.IntegerField(null=True)
    score = models.IntegerField(null=True)
    title = models.CharField(max_length=255, null=True)
    url = models.URLField(null=True)


class Comment(Base):
    parent = models.ForeignKey(Base, on_delete=models.CASCADE, null=True, related_name="kids")
    text = models.TextField(null=True)


class Poll(Base):
    descendants = models.IntegerField(null=True)
    score = models.IntegerField(null=True)
    title = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)


class PollOpt(Base):
    parent = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True,related_name="parts")
    score = models.IntegerField(null=True)
