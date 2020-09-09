from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Steps(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.IntegerField(null=False, blank=False)
    created_at = models.DateField(max_length=10, null=False, blank=False)

