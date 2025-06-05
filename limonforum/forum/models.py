from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('game', 'Game'),
        ('book', 'Book'),
        ('movie', 'Movie'),
        ('series', 'Series'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    slug = models.SlugField()  # İçerik slug'ı
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"


