from django.db import models

# Create your models here.

class PostCardIDEvent(models.Model):
    cardid = models.IntegerField(null=False)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)
