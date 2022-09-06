collection of settings for different demo app

need to change the pointer in `Django.wsgi.py` or `Django.asgi.py`

for example, if want to test on the blog demo, 

change the line in `Django.wsgi.py` or `Django.asgi.py` 

`os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django.blog.settings')`

in the `the config.app.base.py`
`ROOT_URLCONF = 'Django.config.blog.urls'`