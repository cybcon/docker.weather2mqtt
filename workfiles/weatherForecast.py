"""
###############################################################################
# Actual weather and weather forecast - TEST
# seeAlso: https://github.com/open-meteo/open-meteo
# seeAlso: https://open-meteo.com/en/docs
# seeAlso: https://geohack.toolforge.org/geohack.php?pagename=Renningen&language=de&params=48.766111111111_N_8.9347222222222_E_region:DE-BW_type:city(18603)
# seeAlso: https://github.com/open-meteo/open-meteo/issues/287
#------------------------------------------------------------------------------
# Author: Michael Oberdorf
# Date: 2025-03-30
# Last modified by: Michael Oberdorf
# Last modified at: 2025-04-14
###############################################################################
"""

import datetime

import numpy
import openmeteo_requests
import pytz
import requests_cache  # seeAlso: https://pypi.org/project/requests-cache/
from retry_requests import retry  # seeAlso: https://pypi.org/project/retry-requests/

# some datetime calculations
__local_tz__ = pytz.timezone("Europe/Berlin")
today = datetime.datetime.now(__local_tz__)
tomorrow = today + datetime.timedelta(days=1)


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 48.766111,
    "longitude": 8.934722,
    "elevation": 409.0,
    "models": "icon_d2",
    "cell_selection": "land",
    "timezone": "Europe/Berlin",
    "forecast_days": 3,
    "past_days": 0,
    "daily": [
        "weather_code",
        "temperature_2m_max",
        "temperature_2m_min",
        "daylight_duration",
        "sunshine_duration",
        "rain_sum",
        "showers_sum",
        "snowfall_sum",
        "precipitation_sum",
        "precipitation_hours",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "wind_direction_10m_dominant",
        "shortwave_radiation_sum",
        "et0_fao_evapotranspiration",
    ],
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "is_day",
        "precipitation",
        "rain",
        "showers",
        "snowfall",
        "weather_code",
        "cloud_cover",
        "pressure_msl",
        "surface_pressure",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
    ],
}
responses = openmeteo.weather_api(url, params=params)
# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

print("---------------------------------------------------------")
# Current values. The order of variables needs to be the same as requested.
current = response.Current()

if current:
    weather_current_timestamp = datetime.datetime.fromtimestamp(current.Time(), tz=__local_tz__).strftime(
        "%Y-%m-%d %H:%M"
    )
    print(f"Current weather from {weather_current_timestamp}")
    for i in range(0, len(params["current"])):
        print(params["current"][i], current.Variables(i).Value())


print("---------------------------------------------------------")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
if daily:
    daily_forecast_starts_at = datetime.datetime.fromtimestamp(daily.Time(), tz=__local_tz__)
    daily_forecast_ends_at = datetime.datetime.fromtimestamp(daily.TimeEnd(), tz=__local_tz__)
    delta = daily_forecast_ends_at - daily_forecast_starts_at
    interval = datetime.timedelta(seconds=daily.Interval())

    # print("Range from", daily_forecast_starts_at.strftime('%Y-%m-%d'), "to", daily_forecast_ends_at.strftime('%Y-%m-%d'), "with interval", interval.days, "days")
    date_range = list()
    tomorrow_index = None
    for i in range(delta.days):
        day = (daily_forecast_starts_at + i * interval).strftime("%Y-%m-%d")
        if day == tomorrow.strftime("%Y-%m-%d"):
            tomorrow_index = i
        date_range.append(day)
        # print(day.strftime('%Y-%m-%d'))

    if tomorrow_index:
        print("Forecast for tomorrow,", tomorrow.strftime("%Y-%m-%d"))
        for i in range(0, daily.VariablesLength()):
            values = daily.Variables(i).ValuesAsNumpy()
            if isinstance(values, numpy.ndarray):
                values = values.tolist()[tomorrow_index]

            print(params["daily"][i], values)
