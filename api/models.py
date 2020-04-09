from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class PreviousProject(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    githubURL = models.CharField(max_length=200)
    imageURL = models.CharField(max_length=200)
    # githubURL = models.URLField(max_length=200)
    # imageURL = models.URLField(max_length=200)
    tags = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    # pub_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return "{} {}".format(self.title, self.content)


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=30)
    # we did this so that we don't use the username anymore
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(max_length=13)
