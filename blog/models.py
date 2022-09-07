from django.db import models, connection
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class ModelMixins:
    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'truncate table {cls._meta.db_table} CASCADE ')


#
# Customize managers for your models
# you can has as many as you want
# https://docs.djangoproject.com/en/4.1/topics/db/managers/
# you can
# 1. add extra manager methods to an existing manager,
# 2. or create a new manager by modifying the initial QuerySet that the manager returns.
#
# by modifying the initial QuerySet
# assign the Model manager to any name you want in the model class, here it is Post
# published = PublishedManager() ,
class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


# https://docs.djangoproject.com/en/4.1/ref/models/fields/#field-types
class Post(models.Model, ModelMixins):
    """
        define fields for the database table
    """
    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    #
    # build beautiful, SEO-friendly URLs for blog posts
    # the unique_for_date : prevent multiple posts from having the same slug for a given date
    #
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    #
    # ForeignKey Represent a Many-to-one relationship
    # models.ForeignKey(to, on_delete, **options)
    # to: the class to which the model is related
    #
    # to create a recursive relationship - an object that has a many-to-one relationship with itself - use
    # models.ForeignKey('self', on_delete=models.CASCADE)
    # an example of recursive relationship can be 'an employee supervises other employees'
    #
    # to create a relationship on a model that has not yet been defined, use the name of the model,
    # rather than the model object itself.
    #
    # to refer to models defined in another application,
    # you can explicitly specify a model with the full application label.
    #
    # related_name :
    # the name to use for the relation from the related object back to this one.
    # if you'd prefer Django not to create a backwards relation, set related_name to '+', or end it with '+',
    # this ensure that the related model won't have a backwards relation to this model.
    # if not defining the related_name attribute, Django will use the name of the model in lowercase, followed by _set
    # to name the relationship of the related object to the object of the model.
    #
    # Database Representation
    # Behind the scenes, Django appends '_id' to the field name to create its database column name,
    # in this example, model Post will have a column named `author_id`
    #
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default=STATUS[0][0])

    """
        End Field Definition
    """
    def __str__(self):
        return self.title

    # Meta class contains metadata
    class Meta:
        # tell Django to sort results by the publish field in descending order by default
        # when you query the database,
        ordering = ('-publish',)
        #
        # default_manager_name = 'published'
        #

    # the first manager Django encounters is interpreted as default Manager
    # you can specify a custom default manager using Meta.default_manager_name
    objects = models.Manager()  # the default manager
    published = PublishedManager()  # Customized manager, can be used as a Simple version of database view

    # the tags manager will allow you to add, retrieve, and remove tags from Post objects
    tags = TaggableManager()
    # Meta class inside the model contains metadata

    # Canonical URLs
    # https://docs.djangoproject.com/en/4.1/ref/urlresolvers/
    # The convention in Django is to add a get_absolute_url() method to the model
    # that returns the canonical URL for the object.
    # you will use the get_absolute_url() method in your templates to link to specific posts.

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model, ModelMixins):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # enable manually deactivate inappropriate comments
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

