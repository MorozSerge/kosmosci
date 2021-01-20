from django.db import models


# Create your models here.

class Source(models.Model):
    name = models.CharField(unique=True, max_length=512)
    link = models.URLField(null=True)
    description = models.TextField(null=True)
    type_space = models.BooleanField(default=True, verbose_name='Space news source')
    logo = models.URLField(default='')

    def __str__(self):
        return self.name


class New(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, default='')
    link = models.URLField(default='', unique=True)
    image = models.URLField(null=True)
    published = models.DateTimeField()
    source = models.ForeignKey(to=Source, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return ''.join([self.source.name, str(self.published)])
