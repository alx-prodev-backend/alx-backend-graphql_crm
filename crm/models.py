from django.db import models
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    last_active = models.DateTimeField()

    def __str__(self):
        return self.name
