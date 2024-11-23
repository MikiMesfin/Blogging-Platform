from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post, Category, Tag

@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_slug = base_slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = unique_slug

@receiver(pre_save, sender=Category)
def create_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

@receiver(pre_save, sender=Tag)
def create_tag_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name) 