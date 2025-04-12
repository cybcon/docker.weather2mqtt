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
# Last modified at: 2025-04-12\n
###############################################################################\n
"""
import datetime
import json
#from lib.weather_codes import translate_weather_code
import logging
#import openmeteo_requests
import os
import paho.mqtt.client as mqtt
import pytz
#import requests_cache
import ssl
import sys

__version__ = "0.1.0"
__script_path__ = os.path.dirname(__file__)
__config_path__ = os.path.join(os.path.dirname(__script_path__), "etc")
__local_tz__ = pytz.timezone("UTC")

"""
###############################################################################
# F U N C T I O N S
###############################################################################
"""

def initialize_logger(severity: int = logging.INFO) -> logging.getLogger:
    """
    Initialize the logger with the given severity level.\n
    :param severity int: The optional severity level for the logger. (default: 20 (INFO))\n
    :return logging.getLogger: The initialized logger.\n
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

def initialize_mqtt_client() -> mqtt.Client:
    """
    Initialize the MQTT client with the given configuration from environment.\n
    :return mqtt.Client: The initialized MQTT client.\n
    :raise ValueError: If the MQTT client cannot be initialized.\n
    :raise TypeError: If the MQTT client is not of type mqtt.Client.\n
    :raise Exception: If the MQTT client cannot be initialized.\n
    """
    if os.environ.get("MQTT_CLIENT_ID") is not None:
        log.debug("Use MQTT client ID: {}".format(os.environ.get("MQTT_CLIENT_ID")))

    if os.environ.get("MQTT_PROTOCOL_VERSION") == "5":
        log.debug("MQTT protocol version 5")
        client = mqtt.Client(
            callback_api_version = mqtt.CallbackAPIVersion.VERSION2,
            client_id=os.environ.get("MQTT_CLIENT_ID"),
            userdata=None,
            transport="tcp",
            protocol=mqtt.MQTTv5
        )
    else:
        log.debug("MQTT protocol version 3.1.1")
        client = mqtt.Client(
            callback_api_version = mqtt.CallbackAPIVersion.VERSION2,
            client_id=os.environ.get("MQTT_CLIENT_ID"),
            clean_session=True,
            userdata=None,
            transport="tcp",
            protocol=mqtt.MQTTv311,
        )

    # configure TLS
    if os.environ.get("MQTT_TLS") == "true":
        log.debug("Configure MQTT connection to use TLS encryption.")

        if os.environ.get("MQTT_TLS_INSECURE") == "true":
            log.debug("Configure MQTT connection to use TLS with insecure mode.")
            client.tls_set(ca_certs=os.environ.get("REQUESTS_CA_BUNDLE"), cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            client.tls_insecure_set(True)
        else:
            log.debug("Configure MQTT connection to use TLS with secure mode.")
            client.tls_set(ca_certs=os.environ.get("REQUESTS_CA_BUNDLE"), cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            client.tls_insecure_set(False)

    # configure authentication
    if os.environ.get("MQTT_USERNAME") is not None and os.environ.get("MQTT_PASSWORD") is not None:
        log.debug("Set username ({}) and password for MQTT connection".format(os.environ.get("MQTT_USERNAME")))
        client.username_pw_set(os.environ.get("MQTT_USERNAME"), os.environ.get("MQTT_PASSWORD"))

    return client


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

    # initialize MQTT client and connect to broker
    client = initialize_mqtt_client()
    log.debug("MQTT client initialized")



    # Read environment variables
    """
    MODE="current" \
    LONGITUDE="48.72592" \
    LATITUDE="9.11446" \
    """
    log.debug("Connecting to MQTT server {}:{}".format(os.environ.get("MQTT_SERVER"), os.environ.get("MQTT_PORT")))
    try:
        client.connect(os.environ.get("MQTT_SERVER"), int(os.environ.get("MQTT_PORT")), 60)
    except ssl.SSLCertVerificationError as e:
        log.error("SSL certificate verification error: {}".format(e))
        sys.exit(1)



    # TODO: Add the local time as message_timestamp to payload and publish weather data
    PAYLOAD = {
        "message_timestamp": __local_tz__.localize(datetime.datetime.now()).isoformat(),
        "weather": {
            "temperature": 20,
            "humidity": 50,
            "wind_speed": 5,
            "precipitation": 0,
            "weather_code": 0
        },
        "location": {
            "latitude": float(os.environ.get("LATITUDE")),
            "longitude": float(os.environ.get("LONGITUDE"))
        }
    }
    log.debug("Payload: {}".format(json.dumps(PAYLOAD)))
    log.debug("Publishing weather data to MQTT topic: {}".format(os.environ.get("MQTT_TOPIC")))
    client.publish(topic=os.environ.get("MQTT_TOPIC"), payload=json.dumps(PAYLOAD), qos=0, retain=False)
    
    

    client.disconnect()
    log.debug("Disconnected from MQTT server")

    log.info(f"Stop weather2mqtt version {__version__}")
    sys.exit(0)


