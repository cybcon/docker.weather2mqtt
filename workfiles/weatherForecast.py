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
# Last modified at: 2025-03-30
###############################################################################
"""
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

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
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
	#"hourly": ["temperature_2m", "relative_humidity_2m", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "uv_index", "is_day", "sunshine_duration"],
	#"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

"""
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
"""

"""						
# Current values. The order of variables needs to be the same as requested.
current = response.Current()

current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_apparent_temperature = current.Variables(2).Value()
current_is_day = current.Variables(3).Value()
current_precipitation = current.Variables(4).Value()
current_rain = current.Variables(5).Value()
current_showers = current.Variables(6).Value()
current_snowfall = current.Variables(7).Value()
current_weather_code = current.Variables(8).Value()
current_cloud_cover = current.Variables(9).Value()
current_pressure_msl = current.Variables(10).Value()
current_surface_pressure = current.Variables(11).Value()
current_wind_speed_10m = current.Variables(12).Value()
current_wind_direction_10m = current.Variables(13).Value()
current_wind_gusts_10m = current.Variables(14).Value()

print(f"Current time {current.Time()}")

print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
print(f"Current apparent_temperature {current_apparent_temperature}")
print(f"Current is_day {current_is_day}")
print(f"Current precipitation {current_precipitation}")
print(f"Current rain {current_rain}")
print(f"Current showers {current_showers}")
print(f"Current snowfall {current_snowfall}")
print(f"Current weather_code {current_weather_code}")
print(f"Current cloud_cover {current_cloud_cover}")
print(f"Current pressure_msl {current_pressure_msl}")
print(f"Current surface_pressure {current_surface_pressure}")
print(f"Current wind_speed_10m {current_wind_speed_10m}")
print(f"Current wind_direction_10m {current_wind_direction_10m}")
print(f"Current wind_gusts_10m {current_wind_gusts_10m}")
"""
"""
# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_rain = hourly.Variables(2).ValuesAsNumpy()
hourly_showers = hourly.Variables(3).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(4).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(5).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(6).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(7).ValuesAsNumpy()
hourly_cloud_cover_mid = hourly.Variables(8).ValuesAsNumpy()
hourly_cloud_cover_high = hourly.Variables(9).ValuesAsNumpy()
hourly_visibility = hourly.Variables(10).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(11).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(12).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(13).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(14).ValuesAsNumpy()
hourly_is_day = hourly.Variables(15).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(16).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["rain"] = hourly_rain
hourly_data["showers"] = hourly_showers
hourly_data["snowfall"] = hourly_snowfall
hourly_data["weather_code"] = hourly_weather_code
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
hourly_data["visibility"] = hourly_visibility
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["uv_index"] = hourly_uv_index
hourly_data["is_day"] = hourly_is_day
hourly_data["sunshine_duration"] = hourly_sunshine_duration

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)
"""
							# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_sunrise = daily.Variables(3).ValuesAsNumpy()
daily_sunset = daily.Variables(4).ValuesAsNumpy()
daily_daylight_duration = daily.Variables(5).ValuesAsNumpy()
daily_sunshine_duration = daily.Variables(6).ValuesAsNumpy()
daily_uv_index_max = daily.Variables(7).ValuesAsNumpy()
daily_uv_index_clear_sky_max = daily.Variables(8).ValuesAsNumpy()
daily_rain_sum = daily.Variables(9).ValuesAsNumpy()
daily_showers_sum = daily.Variables(10).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(11).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(12).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(13).ValuesAsNumpy()
daily_precipitation_probability_max = daily.Variables(14).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(15).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(16).ValuesAsNumpy()
daily_wind_direction_10m_dominant = daily.Variables(17).ValuesAsNumpy()
daily_shortwave_radiation_sum = daily.Variables(18).ValuesAsNumpy()
daily_et0_fao_evapotranspiration = daily.Variables(19).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["sunrise"] = daily_sunrise
daily_data["sunset"] = daily_sunset
daily_data["daylight_duration"] = daily_daylight_duration
daily_data["sunshine_duration"] = daily_sunshine_duration
daily_data["uv_index_max"] = daily_uv_index_max
daily_data["uv_index_clear_sky_max"] = daily_uv_index_clear_sky_max
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["precipitation_hours"] = daily_precipitation_hours
daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant
daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration

daily_dataframe = pd.DataFrame(data = daily_data)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(daily_dataframe)

