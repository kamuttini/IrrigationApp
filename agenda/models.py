from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse

RED = 'red'
GREY = 'lightgrey'
BLUE = 'lightblue'
GREEN = 'green'

COLORS = [
    (RED, 'Rosso'),
    (GREY, 'Grigio'),
    (BLUE, 'Blu'),
    (GREEN, 'Verde')
]


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    color = models.CharField(max_length=10, choices=COLORS, default=GREY)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        url = reverse('agenda:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

