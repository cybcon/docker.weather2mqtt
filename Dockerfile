FROM alpine:3.21.3

LABEL maintainer="Michael Oberdorf <info@oberdorf-itc.de>"
LABEL site.local.program.version="0.1.0"

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    MODE="current"

COPY --chown=root:root /src /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.12.10-r0 \
       py3-pip=24.3.1-r0 \
       ca-certificates=20241121-r1 \
    && pip3 install --no-cache-dir -r /requirements.txt --break-system-packages

USER 3985:3985

WORKDIR /app

# Start Process
ENTRYPOINT ["python"]
CMD ["-u", "/app/bin/weather2mqtt.py"]
