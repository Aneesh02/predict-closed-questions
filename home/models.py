from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(null=False, blank=False)
    link = models.TextField(null=False, blank=False)
    language = models.CharField(null=False, blank=False, max_length=10)

    def __str__(self):
        return str(self.user)


class Sentence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.ForeignKey(Project, on_delete=models.CASCADE)
    sentence_id = models.IntegerField(null=False, blank=False)
    original = models.TextField(null=False, blank=False)
    translated = models.TextField(null=False, blank=False)

    def __str__(self):
        return str(self.user)
