FROM alpine:3.23.2

LABEL maintainer="Michael Oberdorf <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.2.0"

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
    MQTT_RETAIN="false" \
    CACHE_DIR="/app/cache" \
    CACHE_EXPIRY_AFTER_SEC="600"

COPY --chown=root:root /src /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.12.12-r0 \
       py3-pip=25.1.1-r1 \
       ca-certificates=20251003-r0 \
       tzdata=2025c-r0 \
    # Cleanup APK
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/* \
    && pip3 install --no-cache-dir -r /requirements.txt --break-system-packages \
    # Set Timezone
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone \
    && chmod 666 /etc/localtime /etc/timezone \
    # Create cache directory
    && mkdir -p /app/cache \
    && chmod 755 /app/cache \
    && chown -R 3985:3985 /app/cache

USER 3985:3985

WORKDIR /app

# Start Process
ENTRYPOINT ["python"]
CMD ["-u", "/app/bin/weather2mqtt.py"]
