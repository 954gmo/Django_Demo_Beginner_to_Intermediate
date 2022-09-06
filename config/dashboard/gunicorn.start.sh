#!/bin/bash
NAME=""                                  # Name of the application
DJANGODIR=         # Django project directory
SOCKFILE=gunicorn.sock  # we will communicte using this unix socket
USER=                                       # the user to run as
GROUP=                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=           # which settings file should Django use
DJANGO_WSGI_MODULE=                    # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ~/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

export SECRET_KEY=

export DATABASE=   # 'name of your database'
export DB_USER=    # user name of your database'
export DB_PASS=    # password of your database'
export DB_HOST=    # hosting address of the database'
export DB_PORT=    # port of the database'

export QR_CODE= 
export CUSTOMER_IMG= 
export CUSTOMER_ID= 

export LOGO_URL= 
export QR_BASEURL= 
export IMG_BASEURL= 

export SMS_ACCT= 
export SMS_TOKEN= 
export SMS_FROM_NUMBER= 
export SMS_ADMIN_NUMBER= 
export SMS_MGMT_NUMBER= 
export SMS_IMG= 
export SMS_IMG_URL= 

export LOG_DIR= 

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
