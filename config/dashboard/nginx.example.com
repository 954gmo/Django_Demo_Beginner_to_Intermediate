upstream <name_whatever> {
  # fail_timeout=0 means we always retry an upstream even if it failed
  # to return a good HTTP response (in case the Unicorn master nukes a
  # single worker for timing out).

  server unix:<path-to>/gunicorn.sock fail_timeout=0;
}

server {

    listen   80;
    server_name <example.com>;

    client_max_body_size 4G;

    access_log <path-to>/logs/nginx-access.log;
    error_log <path-to>/logs/nginx-error.log;

    location /static/ {
        alias <path-to>/staticfiles/;
        try_files $uri $uri/ @staticfiles;
    }

    location @staticfiles {
        root <path-to>;
    }

    location /media/ {
        alias   <path-to>/media/;
    }

    location /images/ {
        alias <path-to>/images/;
    }

    location / {
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host $http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
        if (!-f $request_filename) {
            proxy_pass http://<name_whatever>;
            break;
        }
    }

    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root <path-to>/static/;
    }
}