import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.text import slugify
from PIL import Image

User = get_user_model()

class Video(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=150)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.slug = f'{self.slug}-{str(uuid.uuid4())[:8]}'
        super().save(*args, **kwargs)

    def process_thumbnail(self):
        img = Image.open(self.thumbnail.path)
        img = img.convert('RGB')
        img.thumbnail((300, 300))
        img.save(self.thumbnail.path)

    def __str__(self):
        return self.title
    
    def thumbnail_tag(self):
        if self.thumbnail:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;" />', self.thumbnail.url)
        else:
            return 'No thumbnail found'
        
class Comment(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.email} on {self.video.title}"