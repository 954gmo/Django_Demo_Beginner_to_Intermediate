Splitting settings into different files/portions, making it more flexible to different environment

`app_installed.py` : make it more flexible and convenient to install/uninstall different tutorial demo app

`base.py` : common settings for the project

`config.ini` : ENV configuration using `configparser`, together with `local_using_config.py`

`local_using_config.py` : Django project setting for local development environment, using `config.ini` to set up ENV

`gunicorn.start.sh` : settings for gunicorn

`local.py` : Django project settings for local development environment, such as database, environment variables

`local_debug_toolbar.py` : Django project settings for local development environment with debug-toolbar

`local_prod_db.py` : Django project settings for local development environment using production database

`logging_conf.py` : settings for logging

`nginx.example.com` : settings for nginx virtual host

`prod.py` : Django project settings for production environment

`setup_env_linux.sh` : shell script for setting up environment variables for app `sites`

`setup_env_windows.bat` : batch file for setting up environment variables for app `sites`

`sitewide_conf.py` : settings/constants for the site 

`supervisor.example.com.conf` : configuration for supervisor

# Places Where Adjustment might be necessary
## `base.py`
`ROOT_URLCONF, WSGI_APPLICATION, AUTH_USER_MODEL, LOGIN_REDIRECT_URL`

create a `media` directory at project's parent directory (`BASE_DIR.parent`)

## `BASE_DIR/settings.py`
`CONFIGS`




