from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Topic(models.Model):
    name = models.CharField(max_length=128, unique=True)
    author_id = models.IntegerField(default=0)
    description = models.TextField(default="")
    views = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if self.id is None:
            self.slug = slugify(self.name)

        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
