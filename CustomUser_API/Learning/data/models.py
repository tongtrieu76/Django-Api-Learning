from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    favorites = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.first_name, self.last_name, self.email)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    vote = models.IntegerField(default=0)
    accountID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
