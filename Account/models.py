from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
import base64
import jwt
from utils import get_md5

# Create your models here.


class BlogUser(AbstractUser):
    nickname = models.CharField('nickname', max_length=100, blank=True)
    created_at = models.DateTimeField('created_at',auto_now_add=True)
    updated_at = models.DateTimeField('updated_at',auto_now=True)
    source = models.CharField(max_length=100,blank=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        # return reverse(
        #     'blog:author_detail',kwargs={
        #         'author_name': self.username
        #     }
        # )
        return 'account/'+self.username+'/'

    def __str__(self):
        return self.username

    def get_full_url(self):
        site = Site.objects.get_current().domain
        url = 'http://{site}{path}'.format(
            site=site,
            path=self.get_absolute_url()
        )
        return url

    # def save(self, *args, **kwargs):
    #     print(self.password)
    #     self.password = get_md5(str(self.id)+self.password)
    #     super().save(*args,**kwargs)

    # def set_password(self, raw_password):

    class Meta:
        ordering = ['-id']
        verbose_name = "User"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
