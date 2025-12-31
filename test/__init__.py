"""
Test initialization
"""

import os
import sys

__script_path__ = os.path.dirname(__file__)
__repo_path__ = os.path.dirname(__script_path__)
__tool_path__ = os.path.join(__repo_path__, "src", "app", "bin")
sys.path.append(__tool_path__)


os.environ["LATITUDE"] = "1.0"
os.environ["LONGITUDE"] = "2.0"
os.environ["ELEVATION"] = "3.0"
os.environ["WEATHER_MODELS"] = "FooBar"
os.environ["TZ"] = "UTC"
