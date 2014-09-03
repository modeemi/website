from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()

    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    poster = models.ForeignKey(User, editable=False, null=True)

    def set_poster(self, request):
        if request.user.is_authenticated:
            self.poster = request.user
            self.save()

    def set_modifier(self, request):
        if request.user.is_authenticated:
            self.modifier = request.user
            self.save()

