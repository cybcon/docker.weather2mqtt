"""
***************************************************************************
test_weather_codes.py is a python unit test for the python module
   weather_codes
Author: Michael Oberdorf
Date:   2025-04-11
Last modified by: Michael Oberdorf
Last modified at: 2026-01-11
***************************************************************************
"""

__author__ = "Michael Oberdorf <info@oberdorf-itc.de>"
__status__ = "production"
__date__ = "2026-01-11"
__version_info__ = ("1", "1", "0")
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
        self.assertEqual(WeatherCodes(language="de").translate(code=45), "Nebel")
        self.assertEqual(WeatherCodes(language="de").translate(code=66), "Leichter Eisregen")
        self.assertEqual(WeatherCodes(language="de").translate(code=81), "Regenschauer")

        # Test case for unsupported language (fallback to English)
        self.assertEqual(WeatherCodes(language="foo").translate(code=77), "Snow Grains")

    def test_invalid_code(self):
        # Check if invalid code returns "Unknown weather code"
        self.assertEqual(WeatherCodes().translate(code=199), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="en").translate(code=199), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="de").translate(code=199), "Unknown weather code")

    def test_negative_code(self):
        # Check if negative code returns "Unknown weather code"
        self.assertEqual(WeatherCodes().translate(code=-1), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="en").translate(code=-5), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="de").translate(code=-10), "Unknown weather code")

    def test_large_code(self):
        # Check if excessively large code returns "Unknown weather code"
        self.assertEqual(WeatherCodes().translate(code=1000), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="en").translate(code=5000), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="de").translate(code=9999), "Unknown weather code")

    def float_code(self):
        # Check if float that is an integer returns correct translation
        self.assertEqual(WeatherCodes().translate(code=2.0), "Partly cloudy")
        self.assertEqual(WeatherCodes(language="en").translate(code=4.0), "Overcast")
        self.assertEqual(WeatherCodes(language="de").translate(code=10.0), "Schneefall schwach")
        # Check if float code returns "Unknown weather code"
        self.assertEqual(WeatherCodes().translate(code=3.5), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="en").translate(code=7.2), "Unknown weather code")
        self.assertEqual(WeatherCodes(language="de").translate(code=12.9), "Unknown weather code")

    def test_non_integer_code(self):
        # Check if non-integer code returns "Unknown weather code"
        self.assertEqual(WeatherCodes().translate(code="abc"), "Unknown weather code")
        self.assertEqual(WeatherCodes().translate(code=None), "Unknown weather code")
        # Check if NaN is handled correctly
        self.assertEqual(WeatherCodes().translate(code=float("nan")), "Unknown weather code")


if __name__ == "__main__":
    unittest.main()
