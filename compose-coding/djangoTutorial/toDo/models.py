from django.db import models
from django.forms import ModelForm


class ToDo(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name