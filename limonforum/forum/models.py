from django.db import models
from django.contrib.auth.models import User


class GameComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_slug = models.SlugField()  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"


