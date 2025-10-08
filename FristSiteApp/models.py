from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=50)
 

def __str__(self):
    return self.email
