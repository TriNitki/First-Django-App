from enum import auto
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models

class Topic(models.Model):
    '''Topic which user is learning'''
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

class Entry(models.Model):
    '''LEarned information by user about theme'''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self) -> str:
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text