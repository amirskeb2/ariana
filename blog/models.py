from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver

CATEGORIES = [
    ('kiri', 'kosher'),
    ('sammi', 'toxic'),
]


def upload_location(instance, filename):
    file_path = 'blog/{category}/{title}-{filename}'.format(
        category=str(instance.category),
        title=str(instance.title),
        filename=filename
    )
    return file_path


class BlogPost(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True,)
    date_updated = models.DateTimeField(auto_now=True,)
    category = models.CharField(max_length=5, choices=CATEGORIES, null=False, blank=False, default='sammi')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return self.title


@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.category + '-' + instance.title)


pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
