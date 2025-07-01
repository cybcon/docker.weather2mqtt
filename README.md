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

* [`latest`, `1.0.0`](https://github.com/cybcon/docker.weather2mqtt/blob/v1.0.0/Dockerfile)

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
| `TZ`                         | The time zone to use to provide timestamps.                                      | optional     | `UTC`         |
| `MQTT_CLIENT_ID`             | A MQTT client identifier.                                                        | optional     |               |
| `MQTT_PROTOCOL_VERSION`      | The MQTT protocol version to use. Currently supported `3` (means 3.1.1) and `5`. | optional     | `3`           |
| `MQTT_TLS`                   | Use TLS encrypted connection to MQTT broker.                                     | optional     | `false`       |
| `MQTT_TLS_INSECURE`          | Disable TLS certificate and hostname verification.                               | optional     | `false`       |
| `REQUESTS_CA_BUNDLE`         | Path to certificates of trusted certificate authorities.                         | optional     | `/etc/ssl/certs/ca-certificates.crt` |
| `MQTT_USERNAME`              | Username to authenticate to MQTT broker.                                         | optional     |               |
| `MQTT_PASSWORD`              | Password to authenticate to MQTT broker.                                         | optional     |               |
| `MQTT_SERVER`                | MQTT broker hostname to connect to.                                              | optional     | `test.mosquitto.org` |
| `MQTT_PORT`                  | MQTT broker TCP port to connect to.                                              | optional     | `1883`        |
| `MQTT_RETAIN`                | Publish MQTT message in retain mode fpr persistance.                             | optional     | `false`       |
| `MQTT_TOPIC`                 | The MQTT topic to publish the weather data.                                      | optional     | `com/github/cybcon/docker.weather2mqtt.git/weather` |
| `DEBUG`                      | Enable debug output log.                                                         | optional     | `false`       |

### .envrc example

```bash
export TZ="Europe/Berlin"
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export DEBUG="true"
export MODE="current"
export LATITUDE="48.7801"
export LONGITUDE="8.9321"
export ELEVATION="409.0"
export WEATHER_MODELS="icon_d2"
export MQTT_SERVER="test.mosquitto.org"
export MQTT_PORT="8883"
export MQTT_TLS="true"
export MQTT_TLS_INSECURE="true"
export MQTT_CLIENT_ID="acd2b765-e289-49c1-9884-28826f619d2b"
export MQTT_PROTOCOL_VERSION="5"
export MQTT_TOPIC="github.com/cybcon/docker.weather2mqtt.git/weather"
```



# Donate
I would appreciate a small donation to support the further development of my open source projects.

<a href="https://www.paypal.com/donate/?hosted_button_id=BHGJGGUS6RH44" target="_blank"><img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="200px"></a>

# License

Copyright (c) 2025 Michael Oberdorf IT-Consulting

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
