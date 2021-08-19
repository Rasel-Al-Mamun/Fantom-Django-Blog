import os
import uuid
from core.models import User
from django.db import models
from django.urls import reverse
from django.db.models import Count
from taggit.managers import TaggableManager
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


def post_thumbnail_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('post/thumbnail/', filename)


class Category(models.Model):
    class CategoryObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='True').order_by('-id')

    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )

    name = models.CharField(max_length=100, verbose_name='category name')
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=5, choices=STATUS, default='False')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    categoryobjects = CategoryObjects()

    class Meta:
        ordering = ['created_on']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'id': self.id,  'slug': self.slug})


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='Published').order_by('-id')

    OPTIONS = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    auther = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=300, verbose_name='post title')
    overview = models.TextField(null=True)
    thumbnail = models.FileField(upload_to=post_thumbnail_file_path, default='post/thumbnail.jpg', blank=True)
    content = RichTextUploadingField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    tags = TaggableManager()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, choices=OPTIONS, default='Draft')
    views = models.PositiveIntegerField(default=0)
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    objects = models.Manager()
    postobjects = PostObjects()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def thumbnail_tag(self):
        if self.thumbnail.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.thumbnail.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('blog:blog_details', kwargs={'id': self.id, 'slug': self.slug})
    
    def countreview(self):
        comment = Comment.objects.filter(post=self).annotate(count=Count('content'))
        return comment
    
    @property
    def imageURL(self):
	    try:
		    url = self.thumbnail.url
	    except:
		    url = ''
	    return url


class Comment(models.Model):
    class CommentObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='True').order_by('-id')

    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies', blank=True)
    status = models.CharField(max_length=5, choices=STATUS, default='True')
    content = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    commentobjects = CommentObjects()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.post.title

    def children(self):
        return Comment.objects.filter(reply=self)
