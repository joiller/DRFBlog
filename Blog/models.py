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
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


@receiver(pre_save, sender=BlogPost)
def add_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + instance.title)


@receiver(post_delete, sender=BlogPost)
def delete_submit(sender, instance, **kwargs):
    instance.image.delete(False)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_parents(self, json=False):

        def parse(temp):
            if temp.parent:
                if not json:
                    return {
                        temp: {
                            'parent': parse(temp.parent)
                        }
                    }
                return {
                    temp.slug: {
                        'parent': parse(temp.parent)
                    }
                }
            else:
                return temp if not json else temp.slug

        return parse(self)

    def get_parents_list(self):
        categories = [self]

        while categories[0].parent:
            categories.insert(0, categories[0].parent)

        return categories

    def get_children(self, json=False):
        all_categories = Category.objects.all()

        def parse(category):
            children = all_categories.filter(parent=category)
            print(list(map(lambda x: x.name, children)))
            new = {'children': {}}
            for child in children:
                print(child.slug)
                if not json:
                    new['children'][child] = parse(child)
                else:
                    new['children'][child.slug] = parse(child)
            return new

        return {
            self: parse(self)
        } if not json else {
            self.slug: parse(self)
        }


@receiver(pre_save, sender=Category)
def add_slug(sender, instance, **kwargs):
    if not instance.slug:
        categories = map(lambda x: x.name, instance.get_parents_list())
        instance.slug = slugify('-'.join(categories))


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_blog_quantity(self):
        return BlogPost.objects.filter(tags=self).distinct().count()
