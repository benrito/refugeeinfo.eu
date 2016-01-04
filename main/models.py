from django.db import models

# Create your models here.

class FeedbackClick(models.Model):
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    page = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)