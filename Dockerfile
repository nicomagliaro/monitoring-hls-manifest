############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM python:3.5-jessie

# Set the file maintainer (your name - the file's author)
MAINTAINER Nicolas Magliaro

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=website
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/website

ENV INSTALL_PATH /srv

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Install Python dependencies
RUN pip install -r $DOCKYARD_SRVPROJ/requirements.txt

RUN mkdir -p /var/tmp/hls && \
    chmod 777 /var/tmp/hls

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./docker-entrypoint.sh /

CMD gunicorn --name hls-monitoring \
            --bind 0.0.0.0:8000 \
            --timeout 120 \
            --workers 30 \
            --log-level=info \
            --log-file=/srv/logs/gunicorn.log \
            --access-logfile=/srv/logs/access.log \
            "$@"