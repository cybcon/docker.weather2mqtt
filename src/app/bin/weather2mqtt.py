"""
###############################################################################
# Tool to get weather information from the Open-Meteo API and publish it to MQTT\n
# seeAlso: https://open-meteo.com/en/docs\n
#------------------------------------------------------------------------------\n
# This is a Hackergarden project, started during 50th Hackergarden 2025-04-01\n
# at codecentric AG, Industriestraße 3, 70565 Stuttgart, Germany\n
# seeAlso: https://www.hackergarten.net/\n
# seeAlso: https://www.codecentric.de/standorte/stuttgart\n
#------------------------------------------------------------------------------\n
# Author: Michael Oberdorf\n
# Date: 2025-04-11\n
# Last modified by: Michael Oberdorf\n
# Last modified at: 2025-04-13\n
###############################################################################\n
"""

import datetime
import json
import logging
import os
import ssl
import sys

# import numpy
import openmeteo_requests
from openmeteo_sdk import Variable
import paho.mqtt.client as mqtt
import pytz
import requests_cache  # seeAlso: https://pypi.org/project/requests-cache/
from lib.weather_codes import translate_weather_code
from retry_requests import retry  # seeAlso: https://pypi.org/project/retry-requests/

__version__ = "1.0.0"
__script_path__ = os.path.dirname(__file__)
__config_path__ = os.path.join(os.path.dirname(__script_path__), "etc")
__local_tz__ = pytz.timezone("UTC")
__open_meteo_api_url__ = "https://api.open-meteo.com/v1/forecast"

"""
###############################################################################
# F U N C T I O N S
###############################################################################
"""


def initialize_logger(severity: int = logging.INFO) -> logging.Logger:
    """
    Initialize the logger with the given severity level.\n
    :param severity int: The optional severity level for the logger. (default: 20 (INFO))\n
    :return logging.RootLogger: The initialized logger.\n
    :raise ValueError: If the severity level is not valid.\n
    :raise TypeError: If the severity level is not an integer.\n
    :raise Exception: If the logger cannot be initialized.\n
    """
    valid_severity = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    if severity not in valid_severity:
        raise ValueError(f"Invalid severity level: {severity}. Must be one of {valid_severity}.")

    log = logging.getLogger()
    log_handler = logging.StreamHandler(sys.stdout)

    log.setLevel(severity)
    log_handler.setLevel(severity)
    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_handler.setFormatter(log_formatter)
    log.addHandler(log_handler)

    return log


def load_config_file() -> dict:
    """
    Load the configuration file and return the configuration as a dictionary.\n
    :return dict: The loaded configuration.\n
    :raise ValueError: If the configuration file is not valid.\n
    :raise TypeError: If the configuration file is not a string.\n
    :raise Exception: If the configuration file cannot be loaded.\n
    """
    if os.environ.get("MODE") is not None:
        config_file = os.path.join(__config_path__, os.environ.get("MODE") + ".json")
        if os.path.isfile(config_file):
            log.debug("Load configuration from file: {}".format(config_file))
            with open(config_file, "r") as f:
                config = json.load(f)
        else:
            raise ValueError(f"Configuration file {config_file} not found.")
    else:
        raise ValueError("No configuration file specified. Please set the MODE environment variable.")
    log.debug("Configuration loaded")

    # Enrich data with environment variables
    if "data" not in config.keys():
        config["data"] = dict()
    if os.environ.get("LATITUDE") is not None:
        config["data"]["latitude"] = float(os.environ.get("LATITUDE"))
    if os.environ.get("LONGITUDE") is not None:
        config["data"]["longitude"] = float(os.environ.get("LONGITUDE"))
    if os.environ.get("ELEVATION") is not None:
        config["data"]["elevation"] = float(os.environ.get("ELEVATION"))
    if os.environ.get("WEATHER_MODELS") is not None:
        config["data"]["models"] = os.environ.get("WEATHER_MODELS")
    if os.environ.get("TZ") is not None:
        config["data"]["timezone"] = os.environ.get("TZ")

    return config


def initialize_mqtt_client() -> mqtt.Client:
    """
    Initialize the MQTT client with the given configuration from environment.\n
    :return mqtt.Client: The initialized MQTT client.\n
    :raise Exception: If the MQTT client cannot be initialized.\n
    """
    if os.environ.get("MQTT_CLIENT_ID") is not None:
        log.debug("Use MQTT client ID: {}".format(os.environ.get("MQTT_CLIENT_ID")))

    if os.environ.get("MQTT_PROTOCOL_VERSION") == "5":
        log.debug("MQTT protocol version 5")
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=os.environ.get("MQTT_CLIENT_ID"),
            userdata=None,
            transport="tcp",
            protocol=mqtt.MQTTv5,
        )
    else:
        log.debug("MQTT protocol version 3.1.1")
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=os.environ.get("MQTT_CLIENT_ID"),
            clean_session=True,
            userdata=None,
            transport="tcp",
            protocol=mqtt.MQTTv311,
        )

    # configure TLS
    if bool(os.environ.get("MQTT_TLS")):
        log.debug("Configure MQTT connection to use TLS encryption.")

        if bool(os.environ.get("MQTT_TLS_INSECURE")):
            log.debug("Configure MQTT connection to use TLS with insecure mode.")
            client.tls_set(
                ca_certs=os.environ.get("REQUESTS_CA_BUNDLE"),
                cert_reqs=ssl.CERT_NONE,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None,
            )
            client.tls_insecure_set(True)
        else:
            log.debug("Configure MQTT connection to use TLS with secure mode.")
            client.tls_set(
                ca_certs=os.environ.get("REQUESTS_CA_BUNDLE"),
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None,
            )
            client.tls_insecure_set(False)

    # configure authentication
    if os.environ.get("MQTT_USERNAME") is not None and os.environ.get("MQTT_PASSWORD") is not None:
        log.debug("Set username ({}) and password for MQTT connection".format(os.environ.get("MQTT_USERNAME")))
        client.username_pw_set(os.environ.get("MQTT_USERNAME"), os.environ.get("MQTT_PASSWORD"))

    return client


def request_weather_data(payload: dict) -> dict:
    """
    Request weather data from the Open-Meteo API with the given configuration.\n
    :param payload dict: The configuration for the Open-Meteo API request.\n
    :return dict: The weather data from the Open-Meteo API.\n
    :raise Exception: If the weather data cannot be requested.\n
    """
    log.debug(f"Request Open-Meteo API {__open_meteo_api_url__} with parameters: {payload}")
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    responses = openmeteo.weather_api(__open_meteo_api_url__, params=payload)
    response = responses[0]

    result = dict()

    # Adding the location specific information
    result["location"] = dict()
    result["location"]["latitude"] = response.Latitude()
    result["location"]["longitude"] = response.Longitude()
    result["location"]["elevation"] = response.Elevation()

    # Adding timezone specific information
    result["timezone"] = dict()
    result["timezone"]["name"] = response.Timezone().decode("utf8")
    result["timezone"]["abbreviation"] = response.TimezoneAbbreviation().decode("utf8")
    result["timezone"]["utc_offset_seconds"] = response.UtcOffsetSeconds()

    if "current" in payload.keys():
        result["current"] = parse_current_weather(data=response.Current(), fields=payload["current"])
    if "daily" in payload.keys():
        result["daily"] = parse_daily_weather(data=response.Daily(), fields=payload["daily"])

    log.debug(f"Received weather data from Open-Meteo API: {json.dumps(result)}")
    return result


def parse_current_weather(data: any, fields: list = []) -> dict:
    """
    Parse the current weather data from the Open-Meteo API response.\n
    :param data openmeteo_requests.VariablesWithTime: The Open-Meteo API response from current weather.\n
    :param fields list: The list of fields to parse from the current weather data. (default: [])\n
    :return dict: The parsed current weather data.\n
    :raise Exception: If the current weather data cannot be parsed.\n
    """
    if not data:
        raise Exception("No current weather data found in the response.")

    log.debug("Parsing current weather data from Open-Meteo API response.")
    parsed_data = dict()

    parsed_data["Time"] = datetime.datetime.fromtimestamp(data.Time(), tz=__local_tz__).isoformat()

    for i in range(0, len(fields)):
        parsed_data[fields[i]] = data.Variables(i).Value()
        log.debug(f"{fields[i]}: {parsed_data[fields[i]]}")

    # Translate weather code
    if "weather_code" in parsed_data.keys():
        parsed_data["weather_code_text"] = translate_weather_code(parsed_data["weather_code"])
        log.debug(f"Translated weather code: {parsed_data['weather_code_text']}")

    log.debug(f"Parsed current weather: {parsed_data}")
    return parsed_data


def parse_daily_weather(data: any, fields: list = []) -> dict:
    """
    Parse the daily weather data from the Open-Meteo API response.\n
    :param data openmeteo_requests.VariablesWithTime: The Open-Meteo API response from current weather.\n
    :param fields list: The list of fields to parse from the current weather data. (default: [])\n
    :return dict: The parsed current weather data.\n
    :raise Exception: If the current weather data cannot be parsed.\n
    """
    if not data:
        raise Exception("No current weather data found in the response.")

    log.debug("Parsing current weather data from Open-Meteo API response.")
    parsed_data = dict()

    forecast_starts_at = datetime.datetime.fromtimestamp(data.Time(), tz=__local_tz__)
    forecast_ends_at = datetime.datetime.fromtimestamp(data.TimeEnd(), tz=__local_tz__)
    delta = forecast_ends_at - forecast_starts_at
    interval = datetime.timedelta(seconds=data.Interval())

    # print("Range from", daily_forecast_starts_at.strftime('%Y-%m-%d'), "to", daily_forecast_ends_at.strftime('%Y-%m-%d'), "with interval", interval.days, "days")
    interval_range = list()
    for i in range(delta.days):
        forecast_interval = (forecast_starts_at + i * interval).strftime("%Y-%m-%d")
        interval_range.append(forecast_interval)

    variables_with_time = [ data.Variables(i) for i in range(0, data.VariablesLength() )]

    for i in range(0, len(fields)):
        # Not sure do we require to varify the field. Does field order matches?
        # And what about sunshine?
        field = parsed_data[fields[i]] = dict()
        for j in range(len(interval_range)):
            field[interval_range[j]] = variables_with_time[i].Values(j)

        # Translate weather code
    if "weather_code" in parsed_data.keys():
        parsed_data["weather_code_text"] = dict()
        for k,v in parsed_data["weather_code"].items():
            parsed_data["weather_code_text"][k] = translate_weather_code(v)

    log.debug(f"Parsed current weather: {parsed_data}")
    return parsed_data


"""
###############################################################################
# M A I N
###############################################################################
"""
# initialize logger
if os.getenv("DEBUG") == "true":
    log = initialize_logger(logging.DEBUG)
else:
    log = initialize_logger(logging.INFO)

if __name__ == "__main__":
    log.info(f"Starting weather2mqtt version {__version__}")
    if os.environ.get("TZ") is not None:
        __local_tz__ = pytz.timezone(os.environ.get("TZ"))
    log.debug(f"Local timezone set to {__local_tz__}")

    # load configuration from file
    config = load_config_file()

    # request weather data from Open-Meteo API
    weather_result = request_weather_data(payload=config["data"])

    # TODO: transform/enhance weather result

    # Add the local time as message_timestamp to payload
    weather_result["message_timestamp"] = __local_tz__.localize(datetime.datetime.now()).isoformat()

    """
    PAYLOAD = {
        "message_timestamp": __local_tz__.localize(datetime.datetime.now()).isoformat(),
        "weather": {
            "temperature": 20,
            "humidity": 50,
            "wind_speed": 5,
            "precipitation": 0,
            "weather_code": 0,
            "weather_code_text": translate_weather_code(0),
        },
        "location": {
            "latitude": float(os.environ.get("LATITUDE")),
            "longitude": float(os.environ.get("LONGITUDE")),
            "elevation": 409.0,
        },
    }
    """
    log.debug("Payload: {}".format(json.dumps(weather_result)))

    # initialize MQTT client and connect to broker
    client = initialize_mqtt_client()
    log.debug("MQTT client initialized")
    log.debug("Connecting to MQTT server {}:{}".format(os.environ.get("MQTT_SERVER"), os.environ.get("MQTT_PORT")))
    try:
        client.connect(os.environ.get("MQTT_SERVER"), int(os.environ.get("MQTT_PORT")), 60)
    except ssl.SSLCertVerificationError as e:
        log.error("SSL certificate verification error: {}".format(e))
        sys.exit(1)

    retain = False
    if os.environ.get("MQTT_RETAIN") is not None:
        retain = bool(os.environ.get("MQTT_RETAIN"))
    log.debug(
        "Publishing weather data to MQTT topic: {}, using retain: {}".format(os.environ.get("MQTT_TOPIC"), retain)
    )
    client.publish(topic=os.environ.get("MQTT_TOPIC"), payload=json.dumps(weather_result), qos=0, retain=retain)

    client.disconnect()
    log.debug("Disconnected from MQTT server")

    log.info(f"Stop weather2mqtt version {__version__}")
    sys.exit(0)
