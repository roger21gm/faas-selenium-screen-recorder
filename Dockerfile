FROM ghcr.io/openfaas/classic-watchdog:0.1.5 as watchdog
FROM selenium/standalone-chrome:91.0

USER root

# Get watchdog binary
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Install python
RUN apt-get update \
    && apt-get install -y ca-certificates python3-pip vim \
    && rm -rf /var/lib/apt/lists/

# Set home directory
WORKDIR /home/app/

# Copy script
COPY index.py .
RUN mkdir -p function
COPY screen-recording function

# Install selenium & other requierements
RUN pip3 install -r /home/app/function/requirements.txt

# Configure entrypoint
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Set watchdog process
ENV fprocess="python3 index.py"
EXPOSE 8080


## VIDEO RECORDING ##

# Customize sources for apt-get
RUN  echo "deb http://archive.ubuntu.com/ubuntu focal main universe\n" > /etc/apt/sources.list \
  && echo "deb http://archive.ubuntu.com/ubuntu focal-updates main universe\n" >> /etc/apt/sources.list \
  && echo "deb http://security.ubuntu.com/ubuntu focal-security main universe\n" >> /etc/apt/sources.list

# No interactive frontend during docker build
ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true

# ffmpeg
RUN apt-get -qqy update \
  && apt-get -qqy --no-install-recommends install \
    x11-xserver-utils ffmpeg \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Add Supervisor configuration files
COPY video-supervisor.conf /etc/supervisor/conf.d/
COPY video.sh video_ready.py /opt/bin/
RUN chmod +x /opt/bin/video.sh
RUN pip3 install psutil

RUN  mkdir -p /videos

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["./entrypoint.sh"]

