from django.db import models

# Create your models here.

class Owner(models.Model):
  name = models.CharField(max_length=10)
  password = models.CharField(max_length=10)


class Goods(models.Model):
  name = models.CharField(max_length=10)
  price = models.CharField(max_length=10)
  picture = models.CharField(max_length=100)
  owner = models.ForeignKey('Owner',on_delete=models.CASCADE,)


