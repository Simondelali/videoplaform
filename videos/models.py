import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Video(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=150, null=True)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.slug = f'{self.slug}-{str(uuid.uuid4())[:8]}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title