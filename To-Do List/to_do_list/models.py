from django.db import models

# Create your models here.
class Todo(models.Model):
    text = models.CharField(max_length=200)
    added_date = models.DateTimeField()
