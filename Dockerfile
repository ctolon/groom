# Set Python version
ARG PYTHON_VERSION=3.10.2

FROM python:${PYTHON_VERSION}
LABEL maintainer="Cevat Batuhan Tolon <cevat.batuhan.tolon@cern.ch>"

# Set the working directory for Process Monitoring later
ARG APP_VOL=/groom_vol

# Install some useful system dependencies (For Python 3.6 Image)
# Update stretch repositories
#RUN sed -i -e 's/deb.debian.org/archive.debian.org/g' \
#           -e 's|security.debian.org|archive.debian.org/|g' \
#           -e '/stretch-updates/d' /etc/apt/sources.list


# Install some useful system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      bash \
      vim \
      nano \
      unzip \
      coreutils \
      procps \
      unzip \
      software-properties-common \
      netcat \
      gcc \
      wget

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the docker image
COPY ./requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt \
    && rm -rf /root/.cache/pip

# Copy the application files to the docker image for CI/CD
COPY ./app ${APP_VOL}

# Fix Protobuf Builder.py (For Python 3.6)
# RUN curl https://raw.githubusercontent.com/protocolbuffers/protobuf/main/python/google/protobuf/internal/builder.py > /usr/local/lib/python3.6/site-packages/google/protobuf/internal/builder.py

WORKDIR ${APP_VOL}