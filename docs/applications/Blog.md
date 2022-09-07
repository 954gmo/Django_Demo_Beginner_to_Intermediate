# setting up environment
- Installing Django
- Creating and configuring a Django project
- Creating a Django application

# Building a blog application
## topic included
In this simple application, some basic concepts will be demonstrated. 
The detail commencement will give necessary description of key concepts encountered, 
more detail and explanation can be found in the link to official docs

- model, QuerySet, model manager, 
- ForeignKey, many-to-one relationship
- function view, class-based view
- template, template tags, template filters, custom template tags and filters
- URLconf, url converters
- Django administration site

## Design and Coding
- Designing models and generating model migrations
  - [Models](https://docs.djangoproject.com/en/4.1/ref/models/)
  - [Field & Field types](https://docs.djangoproject.com/en/4.1/ref/models/fields/#field-types)
  - [ForeignKey and Many-to-one Relationship](https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/)
  - Summary_Notes/002.Model.md
  - defined in file `blog/models.py` 
    - codes between quoted-docstring 'define fields for the database table'
- Activating the application by adding `blog.apps.BlogConfig` to `INSTALLED_APPS`, here it is in `config.blog.base.py`
- Creating and applying migrations
  - `python manage.py makemigrations blog`
  - `python manage.py migrate`
  
  the following is not part of Django, it is custom module to populate the database for testing purpose.
  - or `docs.DB_sample_data.populate_database.makemigrations_and_migrate()`
  - run `docs.DB_sample_data.populate_database.populate_sample_database()` to populate the database
- Django Administration site
  - [Django Admin Site](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/)
  - `blog/admin.py`
    - Adding Models to the administration site
    - Customize the way that models are displayed
- Working with QuerySets and managers
  - [QuerySets](https://docs.djangoproject.com/en/4.1/ref/models/querysets/)
  - [Model Manager](https://docs.djangoproject.com/en/4.1/topics/db/managers/)
  - When QuerySets are evaluated
  - Summary_Notes/002.Model.md
  - Summary_Notes/003.Advance_Model.md
  - `python manage.py shell` for interacting with database 
  - Creating Model Manager
    - `blog.models.PublishedManager`
- Building views, templates, and URLs
  - [ListView & DetailView](https://docs.djangoproject.com/en/4.1/ref/class-based-views/generic-display/)
  - [Built-in template tags and filters](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/)
  - [Template](https://docs.djangoproject.com/en/4.1/ref/templates/)
  - [Template language](https://docs.djangoproject.com/en/4.1/ref/templates/language/)
  - [Path converter](https://docs.djangoproject.com/en/4.1/topics/http/urls/#path-converters)
  - [URL namespace](https://docs.djangoproject.com/en/4.1/topics/http/urls/#url-namespaces)
  - [URL Resolver](https://docs.djangoproject.com/en/4.1/ref/urlresolvers/)
  - [re_path](https://docs.djangoproject.com/en/4.1/ref/urls/#django.urls.re_path)
  - [class-based view](https://docs.djangoproject.com/en/4.1/topics/class-based-views/intro/)
  - Summary_Notes/004.View.md
  - Summary_Notes/006.Template.md
  - function view: `blog/views/post.py`
  - class based view: `blog/views/post.py`
  - URL patterns `blog/urls.py, config.blog.urls`
  - Canonical URLs for models (`blog/models.py`)
- Creating forms and handling them in views
  - [Forms](https://docs.djangoproject.com/en/4.1/ref/forms/fields/)
  - [Forms API](https://docs.djangoproject.com/en/4.1/ref/forms/api/)
  - Model Forms
  - `blog/forms.py, blog/views/post.py`
  - Summary_Notes/008.Forms.md
- Sending emails with Django
  - local SMTP server
  - external SMTP server
    - `settings.py`
    - `EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_USE_SSL`
    - `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend`
- Integrating third-party applications
  - [many-to-many relationship](https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/)
- Building complex QuerySets
  - [Aggregation Functions](https://docs.djangoproject.com/en/4.1/topics/db/aggregation/)
- Creating custom template tags and filters
  - [Built-in filter](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#built-in-filter-reference)
  - [custom-template tags](https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/#writing-custom-template-filters)
- Adding a sitemap and post feed
  - Django comes with a sitemap framework.  It allows you to generate sitemaps for your site dynamically. 
  a sitemap is an XML file that tells search engines the pages of your websites, their relevance and how frequently they are updated
  - using a sitemap will make your site more visible in search engine ranking: sitemaps help crawlers to index your website's content.
  - [sitemaps](https://docs.djangoproject.com/en/4.1/ref/contrib/sitemaps/)
  - [syndication](https://docs.djangoproject.com/en/4.1/ref/contrib/syndication/)
- Implementing full-text search with PostgreSQL
  full-text search examines the actual key words against
  - [postgresql textsearch](https://www.postgresql.org/docs/12/textsearch.html)
  - [Django postgres search](https://docs.djangoproject.com/en/4.1/ref/contrib/postgres/search/#performance)
