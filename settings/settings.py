import os

DEBUG = os.getenv("DEBUG", False)
if DEBUG:
    print("Starting App in Debug")
    from pathlib import Path
    from dotenv import load_dotenv

    env_path = Path(".") / ".env.debug"
    load_dotenv(env_path)
    from settings.debug import*

    print(f'Serving {APP_NAME} in Debug')
else:
    print("Starting App in Debug")
    from settings.production import*
    load_dotenv()
    print(f'Serving {APP_NAME} in Debug')
    