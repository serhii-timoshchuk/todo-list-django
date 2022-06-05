from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Todo(models.Model):
    status_choices = [('alert-secondary', 'common'), ('alert-warning', 'important'), ('alert-danger', 'very important')]
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    important = models.CharField(max_length=100,choices=status_choices,default=status_choices[0])
    created = models.DateTimeField(default=timezone.now, editable=True)
    datecomplited = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idx = models.PositiveIntegerField(default=0,blank=False)



    def __str__(self):
        return self.title


