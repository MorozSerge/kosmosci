from django.db import models
from django.contrib.auth.models import AbstractUser
from news.models import Source

# Create your models here.


class Enlightened(AbstractUser):
    portrait = models.ImageField(upload_to='images/portraits/', max_length=512, null=True)
    about = models.TextField(default='', null=True, blank=True)
    pass


class UserFollow(models.Model):
    idea_source = models.ForeignKey(to=Enlightened, on_delete=models.CASCADE, related_name='author', null=True)
    follower = models.ForeignKey(to=Enlightened, on_delete=models.CASCADE, related_name='follower', null=True)

    def __str__(self):
        return ' '.join([self.idea_source.username, self.follower.username])


class NewsFollow(models.Model):
    news_source = models.ForeignKey(to=Source, on_delete=models.CASCADE, null=True)
    follower = models.ForeignKey(to=Enlightened, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return ' '.join([self.news_source.name, self.follower.username])
