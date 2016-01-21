from django.db import models

# Create your models here.
from django.utils import timezone
import secretballot

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

secretballot.enable_voting_on(Post)

class Comment(models.Model):
    post = models.ForeignKey('melaongo.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


