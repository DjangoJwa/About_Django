from django.db import models

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=30)
    text=models.TextField()
    created_date=models.DateField(auto_now_add=True)