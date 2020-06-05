from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver


# Create your models here.


def upload_to(instance, filename):
    file_path = 'Blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id),
        title=str(instance.title),
        filename=str(filename)
    )

    return file_path


class BlogPost(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    body = models.TextField(max_length=5000, blank=False, null=False)
    image = models.ImageField(upload_to=upload_to, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=BlogPost)
def add_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + instance.title)


@receiver(post_delete, sender=BlogPost)
def delete_submit(sender, instance, **kwargs):
    instance.image.delete(False)
