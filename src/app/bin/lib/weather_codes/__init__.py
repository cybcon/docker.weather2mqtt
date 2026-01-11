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

__all__ = ["translate_weather_code"]

import json
import os

__default_weather_lang = "en"

# identify the path to the translations folder
__translations_path = os.path.join(__path__[0], "translations")
# load the default language weather codes
weather_code_translation_file = os.path.join(__translations_path, f"{__default_weather_lang}.json")
with open(weather_code_translation_file, encoding="utf-8") as f:
    __WEATHER_CODES = json.load(f)


def translate_weather_code(code: int) -> str:
    """
    Translate weather code to human readable description

    :param code: Weather code
    :return: Human readable description
    """
    return __WEATHER_CODES.get(str(int(code)), "Unknown weather code")
