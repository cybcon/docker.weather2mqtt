FROM alpine:3.21.3

LABEL maintainer="Michael Oberdorf <info@oberdorf-itc.de>"
LABEL site.local.program.version="0.1.0"

ENV TZ="UTC" \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    DEBUG="true" \
    MODE="current" \
    LATITUDE="48.72592" \
    LONGITUDE="9.11446" \
    MQTT_SERVER="test.mosquitto.org" \
    MQTT_PORT="1883" \
    MQTT_TLS="false" \
    MQTT_TLS_INSECURE="false" \
    MQTT_PROTOCOL_VERSION="5" \
    MQTT_TOPIC="github.com/cybcon/docker.weather2mqtt.git/weather"

COPY --chown=root:root /src /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.12.10-r0 \
       py3-pip=24.3.1-r0 \
       ca-certificates=20241121-r1 \
       tzdata=2025a-r0 \
    && pip3 install --no-cache-dir -r /requirements.txt --break-system-packages \
    # Set Timezone
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone \
    && chmod 666 /etc/localtime /etc/timezone


USER 3985:3985

WORKDIR /app

# Start Process
ENTRYPOINT ["python"]
CMD ["-u", "/app/bin/weather2mqtt.py"]
