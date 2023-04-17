FROM python:3-bullseye

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/rc_hip

COPY rc_hip /opt/app/rc_hip
RUN rm -f /opt/app/rc_hip/data/db.sqlite3

WORKDIR /opt/app

COPY requirements_prod.txt /opt/app/
RUN pip install -r requirements_prod.txt --cache-dir /opt/app/pip_cache

COPY start_server.sh /opt/app/
RUN chmod +x /opt/app/start_server.sh

RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start_server.sh"]
