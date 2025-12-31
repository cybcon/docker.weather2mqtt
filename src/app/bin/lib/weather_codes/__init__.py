"""
###############################################################################
# Library to tranlate weather codes to human readable description text\n
# seeAlso: https://github.com/open-meteo/open-meteo/issues/287\n
#------------------------------------------------------------------------------\n
# Author: Michael Oberdorf\n
# Date: 2025-04-11\n
# Last modified by: Michael Oberdorf\n
# Last modified at: 2025-07-01\n
###############################################################################\n
"""

__author__ = "Michael Oberdorf <info@oberdorf-itc.de>"
__status__ = "production"
__date__ = "2025-07-01"
__version_info__ = ("0", "1", "1")
__version__ = ".".join(__version_info__)

__all__ = ["translate_weather_code"]

_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Freezing Fog and depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow Grains",
    80: "Rain showers: Slight intensity",
    81: "Rain showers: Moderate intensity",
    82: "Rain showers: Heavy intensity",
    85: "Snow showers: Slight intensity",
    86: "Snow showers: Heavy intensity",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with hail",
    100: "is not used",
    101: "Tornado",
    102: "Tropical storm",
    103: "Hurricane",
}


def translate_weather_code(code: int) -> str:
    """
    Translate weather code to human readable description\n
    :param code: Weather code\n
    :return: Human readable description\n
    """
    return _WEATHER_CODES.get(code, "Unknown weather code")
