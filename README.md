# Quick reference

This is a Hackergarden project, started during 50th [Hackergarden](https://www.hackergarten.net/) 2025-04-01
at [codecentric AG](https://www.codecentric.de/standorte/stuttgart), Industriestraße 3, 70565 Stuttgart, Germany.

Maintained by: [Michael Oberdorf IT-Consulting](https://www.oberdorf-itc.de/)

Source code: [GitHub](https://github.com/cybcon/weather2mqtt)

Container image: [DockerHub](https://hub.docker.com/r/oitc/weather2mqtt)

<!-- SHIELD GROUP -->
[![][github-action-test-shield]][github-action-test-link]
[![][github-action-release-shield]][github-action-release-link]
[![][github-release-shield]][github-release-link]
[![][github-releasedate-shield]][github-releasedate-link]
[![][github-stars-shield]][github-stars-link]
[![][github-forks-shield]][github-forks-link]
[![][github-issues-shield]][github-issues-link]
[![][github-license-shield]][github-license-link]

[![][docker-release-shield]][docker-release-link]
[![][docker-pulls-shield]][docker-pulls-link]
[![][docker-stars-shield]][docker-stars-link]
[![][docker-size-shield]][docker-size-link]

# Supported tags and respective `Dockerfile` links

* [`latest`, `1.3.4`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.3.4/Dockerfile)
* [`1.3.3`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.3.3/Dockerfile)
* [`1.3.1`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.3.1/Dockerfile)
* [`1.3.0`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.3.0/Dockerfile)
* [`1.2.0`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.2.0/Dockerfile)
* [`1.1.1`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.1.1/Dockerfile)
* [`1.1.0`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.1.0/Dockerfile)
* [`1.0.2`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.0.2/Dockerfile)
* [`1.0.0`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.0.0/Dockerfile)

# Summary
The application will make an [Open Meteo](https://open-meteo.com/) free weather API call to get weather information for the configured geo coordinates.
There are currently two `MODES` specified:
1. `current`: will get the current weather
2. `tomorrow`: will get the weather for tomorrow

The results will be parsed, formatted in JSON and published via MQTT.

## JSON output examples

### current weather

```json
{
  "location": {
    "latitude": 48.779998779296875,
    "longitude": 8.940000534057617,
    "elevation": 409
  },
  "timezone": {
    "name": "Europe/Berlin",
    "abbreviation": "GMT+1",
    "utc_offset_seconds": 3600
  },
  "current": {
    "time": "2026-01-06T09:45:00+01:00",
    "temperature_2m": -6.849999904632568,
    "relative_humidity_2m": 89,
    "is_day": 1,
    "rain": 0,
    "showers": 0,
    "snowfall": 0,
    "weather_code": 71,
    "cloud_cover": 100,
    "surface_pressure": 967.1641845703125,
    "wind_speed_10m": 2.0364675521850586,
    "wind_direction_10m": 224.99989318847656,
    "wind_gusts_10m": 4.320000171661377,
    "weather_code_text": "Snow fall: Slight intensity"
  },
  "message_timestamp": "2026-01-06T09:59:13.119176+01:00"
}
```

## weather forecast for tomorrow

```json
{
  "location": {
    "latitude": 48.779998779296875,
    "longitude": 8.940000534057617,
    "elevation": 409
  },
  "timezone": {
    "name": "Europe/Berlin",
    "abbreviation": "GMT+1",
    "utc_offset_seconds": 3600
  },
  "tomorrow": {
    "date": "2026-01-07",
    "temperature_2m_mean": -5.241146087646484,
    "temperature_2m_min": -8.211000442504883,
    "temperature_2m_max": -3.510999917984009,
    "rain_sum": 0,
    "showers_sum": 0,
    "snowfall_sum": 0,
    "weather_code": 3,
    "wind_speed_10m_mean": 6.99040412902832,
    "wind_speed_10m_min": 1.9386591911315918,
    "wind_speed_10m_max": 13.10419750213623,
    "wind_direction_10m_dominant": 194.28439331054688,
    "wind_gusts_10m_mean": 13.739999771118164,
    "wind_gusts_10m_min": 5.039999961853027,
    "wind_gusts_10m_max": 25.559999465942383,
    "sunrise": 0,
    "sunset": 0,
    "daylight_duration": 30511.171875,
    "sunshine_duration": 23594.3828125,
    "surface_pressure_mean": 964.9620971679688,
    "surface_pressure_min": 961.7695922851562,
    "surface_pressure_max": 968.2794189453125,
    "relative_humidity_2m_mean": 80.78125,
    "relative_humidity_2m_min": 69,
    "relative_humidity_2m_max": 89,
    "weather_code_text": "Cloudy"
  },
  "message_timestamp": "2026-01-06T09:57:42.813048+01:00"
}
```

# Configuration

## Container configuration

The container grab some configuration via environment variables.

| Environment variable name    | Description                                                                      | Required     | Default value |
|------------------------------|----------------------------------------------------------------------------------|--------------|---------------|
| `MODE`                       | The weather selection mode. Currently supported is `current` and  `tomorow`.     | optional     | `current`     |
| `LATITUDE`                   | The geo coordinate latitude from where we want to have the weather.              | optional     | `48.72592`    |
| `LONGITUDE`                  | The geo coordinate longitude from where we want to have the weather.             | optional     | `9.11446`     |
| `ELEVATION`                  | The ground elevation from where we want to have the weather.                     | optional     |               |
| `WEATHER_MODELS`             | The weather model to use.                                                        | optional     |               |
| `WEATHE_CODE_LANGUAGE`       | Translation of the numeric weather code into the defined language ('en' or 'de') | optional     | `en`          |
| `TZ`                         | The time zone to use to provide timestamps.                                      | optional     | `UTC`         |
| `MQTT_CLIENT_ID`             | A MQTT client identifier.                                                        | optional     |               |
| `MQTT_PROTOCOL_VERSION`      | The MQTT protocol version to use. Currently supported `3` (means 3.1.1) and `5`. | optional     | `3`           |
| `MQTT_TLS`                   | Use TLS encrypted connection to MQTT broker.                                     | optional     | `false`       |
| `MQTT_TLS_INSECURE`          | Disable TLS certificate and hostname verification.                               | optional     | `false`       |
| `REQUESTS_CA_BUNDLE`         | Path to certificates of trusted certificate authorities.                         | optional     | `/etc/ssl/certs/ca-certificates.crt` |
| `MQTT_USERNAME`              | Username to authenticate to MQTT broker.                                         | optional     |               |
| `MQTT_PASSWORD`              | Password to authenticate to MQTT broker.                                         | optional     |               |
| `MQTT_PASSWORD_FILE`         | File that contains the password to authenticate to MQTT broker.                  | optional     |               |
| `MQTT_SERVER`                | MQTT broker hostname to connect to.                                              | optional     | `test.mosquitto.org` |
| `MQTT_PORT`                  | MQTT broker TCP port to connect to.                                              | optional     | `1883`        |
| `MQTT_RETAIN`                | Publish MQTT message in retain mode fpr persistance.                             | optional     | `false`       |
| `MQTT_TOPIC`                 | The MQTT topic to publish the weather data.                                      | optional     | `com/github/cybcon/docker.weather2mqtt.git/weather` |
| `CACHE_DIR`                  | Directory used for API request caching.                                          | optional     | `/app/cache`  |
| `CACHE_EXPIRY_AFTER_SEC`     | Cache expiration time in seconds.                                                | optional     | `600`         |
| `DEBUG`                      | Enable debug output log.                                                         | optional     | `false`       |

### .envrc example

If you use `direnv` to load your environment automatically.

```bash
export TZ="Europe/Berlin"
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export DEBUG="true"
export MODE="current"
export LATITUDE="48.72592"
export LONGITUDE="9.11446"
export WEATHER_MODELS="icon_d2"
export MQTT_SERVER="test.mosquitto.org"
export MQTT_PORT="8883"
export MQTT_TLS="true"
export MQTT_TLS_INSECURE="true"
export MQTT_CLIENT_ID="acd2b765-e289-49c1-9884-28826f619d2b"
export MQTT_PROTOCOL_VERSION="5"
export MQTT_TOPIC="github.com/cybcon/docker.weather2mqtt.git/weather"
export CACHE_DIR="../cache"
export CACHE_EXPIRY_AFTER_SEC="600"
export WEATHE_CODE_LANGUAGE="de"
```

### Configuration files

The modes (`current` and `tomorrow`) are defined in configuration files. That can be found here:

| Mode       | Configuration file in GIT                                    | Location in the container image |
|------------|--------------------------------------------------------------|---------------------------------|
| `current`  | [`./src/app/etc/current.json`](./src/app/etc/current.json)   | `/app/etc/current.json`         |
| `tomorrow` | [`./src/app/etc/tomorrow.json`](./src/app/etc/tomorrow.json) | `/app/etc/tomorrow.json`        |

The files specifies the API call request body for Open Mateo. A documentation of the free weather API can be found here: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs).

## Python Unit Tests

To trigger the Python unit tests please follow following instrructions after checkout the git repository.

### Requirements

```bash
pip install -r src/requirements.txt
pip install -r test/requirements.txt
```

### Execute Unit Tests

```bash
python -m unittest
pytest
ruff check --select=E9,F63,F7,F82 --target-version=py312 .
ruff check --target-version=py312 .
```

# Donate
I would appreciate a small donation to support the further development of my open source projects.

<a href="https://www.paypal.com/donate/?hosted_button_id=BHGJGGUS6RH44" target="_blank"><img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="200px"></a>

# License

Copyright (c) 2025-2026 Michael Oberdorf IT-Consulting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<!-- LINK GROUP -->
[docker-pulls-link]: https://hub.docker.com/r/oitc/weather2mqtt
[docker-pulls-shield]: https://img.shields.io/docker/pulls/oitc/weather2mqtt?color=45cc11&labelColor=black&style=flat-square
[docker-release-link]: https://hub.docker.com/r/oitc/weather2mqtt
[docker-release-shield]: https://img.shields.io/docker/v/oitc/weather2mqtt?color=369eff&label=docker&labelColor=black&logo=docker&logoColor=white&style=flat-square
[docker-size-link]: https://hub.docker.com/r/oitc/weather2mqtt
[docker-size-shield]: https://img.shields.io/docker/image-size/oitc/weather2mqtt?color=369eff&labelColor=black&style=flat-square
[docker-stars-link]: https://hub.docker.com/r/oitc/weather2mqtt
[docker-stars-shield]: https://img.shields.io/docker/stars/oitc/weather2mqtt?color=45cc11&labelColor=black&style=flat-square
[github-action-release-link]: https://github.com/cybcon/docker.weather2mqtt/actions/workflows/release-from-label.yaml
[github-action-release-shield]: https://img.shields.io/github/actions/workflow/status/cybcon/docker.weather2mqtt/release-from-label.yaml?label=release&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-action-test-link]: https://github.com/cybcon/docker.weather2mqtt/actions/workflows/code-validation.yaml
[github-action-test-shield-original]: https://github.com/cybcon/docker.weather2mqtt/actions/workflows/code-validation.yaml/badge.svg
[github-action-test-shield]: https://img.shields.io/github/actions/workflow/status/cybcon/docker.weather2mqtt/code-validation.yaml?label=tests&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-forks-link]: https://github.com/cybcon/docker.weather2mqtt/network/members
[github-forks-shield]: https://img.shields.io/github/forks/cybcon/docker.weather2mqtt?color=8ae8ff&labelColor=black&style=flat-square
[github-issues-link]: https://github.com/cybcon/docker.weather2mqtt/issues
[github-issues-shield]: https://img.shields.io/github/issues/cybcon/docker.weather2mqtt?color=ff80eb&labelColor=black&style=flat-square
[github-license-link]: https://github.com/cybcon/docker.weather2mqtt/blob/main/LICENSE
[github-license-shield]: https://img.shields.io/badge/license-MIT-blue?labelColor=black&style=flat-square
[github-release-link]: https://github.com/cybcon/docker.weather2mqtt/releases
[github-release-shield]: https://img.shields.io/github/v/release/cybcon/docker.weather2mqtt?color=369eff&labelColor=black&logo=github&style=flat-square
[github-releasedate-link]: https://github.com/cybcon/docker.weather2mqtt/releases
[github-releasedate-shield]: https://img.shields.io/github/release-date/cybcon/docker.weather2mqtt?labelColor=black&style=flat-square
[github-stars-link]: https://github.com/cybcon/docker.weather2mqtt
[github-stars-shield]: https://img.shields.io/github/stars/cybcon/docker.weather2mqtt?color=ffcb47&labelColor=black&style=flat-square
