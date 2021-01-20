from django.db import models
from account.models import Enlightened


# Create your models here.


class UserNews(models.Model):
    idea_source = models.ForeignKey(to=Enlightened, on_delete=models.CASCADE)
    body = models.CharField(max_length=350)
    image = models.ImageField(upload_to='images/attachments/', null=True, max_length=1024, blank=True)
    published = models.DateTimeField()

    class Meta:
        verbose_name_plural = "user news"
        ordering = ['-published']

    def __str__(self):
        return self.idea_source.username + self.published.__str__()
