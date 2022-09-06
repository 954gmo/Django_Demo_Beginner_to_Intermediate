from django.contrib import admin
from blog.models import Post, Comment
# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/


# Register your models here.
#
# register model to the Django Admin sites
#
# admin.site.register(Post)
#
# OR
# use @admin.register decorator
# Customize the way that models are display
#
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # set teh fields of your model that you want to display on the administration object list page
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')