from django.db import models

# Create your models here

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.CharField(unique=True, max_length=50)
    account_name = models.CharField(max_length=50)
    app_secret_token = models.CharField(max_length=50)
    website = models.URLField(blank=True)

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10)
    headers = models.JSONField()