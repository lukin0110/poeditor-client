FROM python:3.6.6-jessie

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH $PYTHONPATH:/poeditor-client/

WORKDIR /poeditor-client/

# Install postgres client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unzip zip wget gettext && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --user --upgrade twine==1.13.0

# Create Docker entrypoint.
COPY deployment/entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

COPY . ./
