"""
***************************************************************************\n
test_weather_codes.py is a python unit test for the python module
   weather_codes\n
Author: Michael Oberdorf\n
Date:   2025-04-11\n
Last modified by: Michael Oberdorf\n
Last modified at: 2025-04-12\n
***************************************************************************\n
"""

__author__ = "Michael Oberdorf <info@oberdorf-itc.de>"
__status__ = "production"
__date__ = "2025-04-12"
__version_info__ = ("1", "0", "0")
__version__ = ".".join(__version_info__)

__all__ = ["TestWeatherCodes"]

import unittest

from src.app.bin.lib.weather_codes import WeatherCodes


class TestWeatherCodes(unittest.TestCase):
    def test_translate(self):
        # Test cases for default language (English)
        self.assertEqual(WeatherCodes().translate(code=0), "Clear sky")
        self.assertEqual(WeatherCodes().translate(code=1), "Mainly clear")

        # Test cases for specific languages (English and German)
        self.assertEqual(WeatherCodes(language="en").translate(code=3), "Cloudy")
        self.assertEqual(WeatherCodes(language="en").translate(code=199), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="de").translate(code=45), "Nebel")
        self.assertEqual(WeatherCodes(language="de").translate(code=66), "Leichter Eisregen")
        self.assertEqual(WeatherCodes(language="de").translate(code=81), "Regenschauer")
        self.assertEqual(WeatherCodes(language="de").translate(code=199), "Unknown weather code")

        # Test case for unsupported language (fallback to English)
        self.assertEqual(WeatherCodes(language="foo").translate(code=77), "Snow Grains")


if __name__ == "__main__":
    unittest.main()
