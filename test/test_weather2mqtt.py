"""
***************************************************************************
test_weather2mqtt.py is a python unit test for the python script
   weather2mqtt.py
Author: Michael Oberdorf
Date:   2025-04-13
Last modified by: Michael Oberdorf
Last modified at: 2026-01-11
***************************************************************************
"""

__author__ = "Michael Oberdorf <info@oberdorf-itc.de>"
__status__ = "production"
__date__ = "2026-01-11"
__version_info__ = ("1", "0", "1")
__version__ = ".".join(__version_info__)

__all__ = ["TestWeather2Mqtt"]

import logging
import os
import unittest

import paho.mqtt.client as mqtt

from src.app.bin.weather2mqtt import (
    initialize_logger,
    initialize_mqtt_client,
    load_config_file,
)


class TestWeather2Mqtt(unittest.TestCase):
    def test_initialize_logger(self):
        self.assertIsInstance(initialize_logger(), logging.RootLogger)
        log = initialize_logger()
        self.assertEqual(log.level, logging.INFO)
        log = initialize_logger(severity=logging.DEBUG)
        self.assertEqual(log.level, logging.DEBUG)
        log = initialize_logger(severity=logging.FATAL)
        self.assertEqual(log.level, logging.FATAL)

    def test_load_config_file(self):
        os.environ["MODE"] = "current"
        config = load_config_file()
        self.assertIsInstance(config, dict)
        self.assertIn("data", config)
        self.assertIsInstance(config["data"], dict)

        self.assertIn("latitude", config["data"])
        self.assertIsInstance(config["data"]["latitude"], float)
        self.assertEqual(config["data"]["latitude"], 1.0)

        self.assertIn("longitude", config["data"])
        self.assertIsInstance(config["data"]["longitude"], float)
        self.assertEqual(config["data"]["longitude"], 2.0)

        self.assertIn("elevation", config["data"])
        self.assertIsInstance(config["data"]["elevation"], float)
        self.assertEqual(config["data"]["elevation"], 3.0)

        self.assertIn("models", config["data"])
        self.assertIsInstance(config["data"]["models"], str)
        self.assertEqual(config["data"]["models"], "FooBar")

        self.assertIn("timezone", config["data"])
        self.assertIsInstance(config["data"]["timezone"], str)
        self.assertEqual(config["data"]["timezone"], "UTC")

    def test_initialize_mqtt_client(self):
        mqtt_client = initialize_mqtt_client()
        self.assertIsInstance(mqtt_client, mqtt.Client)
        self.assertEqual(mqtt_client._client_id, b"")
        self.assertIsNone(mqtt_client._username)
        self.assertIsNone(mqtt_client._password)
        self.assertEqual(mqtt_client._host, "")
        self.assertEqual(mqtt_client._port, 1883)


if __name__ == "__main__":
    unittest.main()
