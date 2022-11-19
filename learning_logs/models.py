from django.db import models
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField

class Topic(models.Model):
    '''Topic which user is learning'''
    text = models.CharField(max_length = 20)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    descr = models.TextField()

    def __str__(self) -> str:
        return self.text

class Entry(models.Model):
    '''Learned information by user about theme'''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', blank=True)
    url = EmbedVideoField()

    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self) -> str:
        if len(self.text) == 0:
            return f"{self.date_added}"
        elif len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text