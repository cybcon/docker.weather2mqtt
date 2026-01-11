"""
###############################################################################
# Library to translate weather codes to human readable description text
# seeAlso: https://github.com/open-meteo/open-meteo/issues/287
#------------------------------------------------------------------------------
# Author: Michael Oberdorf
# Date: 2025-04-11
# Last modified by: Michael Oberdorf
# Last modified at: 2026-01-11
###############################################################################\n
"""

__author__ = "Michael Oberdorf <info@oberdorf-itc.de>"
__status__ = "production"
__date__ = "2026-01-11"
__version_info__ = ("1", "0", "0")
__version__ = ".".join(__version_info__)

__all__ = ["WeatherCodes"]

import json
import logging
import os


class WeatherCodes:
    """
    Class to translate weather codes to human readable description
    """

    __translations_path = os.path.join(__path__[0], "translations")

    def __init__(self, language: str = "en"):
        self.logger = logging.getLogger(__name__)

        # identify the weather code translation file
        weather_code_translation_file = os.path.join(self.__translations_path, f"{language}.json")
        if not os.path.isfile(weather_code_translation_file):
            self.logger.warning(
                f"Weather code translation file for language '{language}' not found. Falling back to default language 'en'."
            )
            weather_code_translation_file = os.path.join(self.__translations_path, "en.json")

        # load the weather code translations
        with open(weather_code_translation_file, encoding="utf-8") as f:
            self.weather_codes = json.load(f)

    def translate(self, code: int) -> str:
        """
        Translate weather code to human readable description

        :param code: Weather code
        :return: Human readable description
        """
        # transform the code to int and str to fit to the json keys
        code = str(int(code))
        self.logger.debug(f"Translating weather code {code}")
        translation = self.weather_codes.get(code, "Unknown weather code")
        self.logger.debug(f"Weather code {code} translated to '{translation}'")
        return translation
