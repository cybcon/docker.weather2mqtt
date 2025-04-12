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
from src.app.bin.lib.weather_codes import translate_weather_code

class TestWeatherCodes(unittest.TestCase):
    def test_translate_weather_code(self):
        # Example test cases for translate_weather_code
        self.assertEqual(translate_weather_code(0), "Clear sky")
        self.assertEqual(translate_weather_code(1), "Mainly clear")
        self.assertEqual(translate_weather_code(3), "Cloudy")
        self.assertEqual(translate_weather_code(199), "Unknown weather code")

if __name__ == "__main__":
    unittest.main()