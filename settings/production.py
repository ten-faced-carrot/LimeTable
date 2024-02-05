from settings._global import *
import os

APP_SECRET_KEY = os.urandom(12)
APP_NAME = f"LimeTable-Prod-v{os.environ['VERSION']}"