FROM ubuntu:16.04

MAINTAINER Hardwire Interactive

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

# Install Package
RUN apt-get update && \
    apt-get install -qy \
    python3 python3-dev python3-pip python-virtualenv && \
    mkdir env && \
    virtualenv -p python3 /env && \
    . /env/bin/activate && \
    pip install -r requirements.txt

# Add entrypoint script
ADD scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
