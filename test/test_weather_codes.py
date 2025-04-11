import unittest
from lib.weather_codes import translate_weather_code

class TestWeatherCodes(unittest.TestCase):
    def test_translate_weather_code(self):
        # Example test cases for translate_weather_code
        self.assertEqual(translate_weather_code(0), "Clear sky")
        self.assertEqual(translate_weather_code(1), "Mainly clear")
        self.assertEqual(translate_weather_code(3), "Overcast")
        self.assertEqual(translate_weather_code(99), "Unknown code")

if __name__ == "__main__":
    unittest.main()