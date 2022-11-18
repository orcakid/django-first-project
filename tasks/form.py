from django.forms import ModelForm
from .models import Task


class TaskCreate(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
