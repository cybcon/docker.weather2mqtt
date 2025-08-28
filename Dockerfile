FROM alpine:3.22.1

LABEL maintainer="Michael Oberdorf <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.0.0"

ENV TZ="UTC" \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    DEBUG="false" \
    MODE="current" \
    LATITUDE="48.72592" \
    LONGITUDE="9.11446" \
    MQTT_SERVER="test.mosquitto.org" \
    MQTT_PORT="1883" \
    MQTT_TLS="false" \
    MQTT_TLS_INSECURE="false" \
    MQTT_PROTOCOL_VERSION="5" \
    MQTT_TOPIC="com/github/cybcon/docker.weather2mqtt.git/weather" \
    MQTT_RETAIN="false"

COPY --chown=root:root /src /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.12.11-r0 \
       py3-pip=25.1.1-r0 \
       ca-certificates=20250619-r0 \
       tzdata=2025b-r0 \
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
