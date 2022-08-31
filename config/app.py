"""
application global configuration
"""

try:
    from os import path, environ
    from dotenv import load_dotenv

    BASEDIR = path.abspath(path.dirname(__file__) + "/..")
    load_dotenv(dotenv_path=BASEDIR + "/.env")

    TITLE = "Djib NODE PROFILE API"
    HOST = environ.get("FLASK_HOST")
    PORT = int(environ.get("FLASK_PORT"))
    SECRET = environ.get("FLASK_SECRET")

    TELEMETRY_ENDPOINT = environ.get("TELEMETRY_ENDPOINT")

    PROPAGATE_EXCEPTIONS = False
    DEBUG = True

    if environ.get("FLASK_MODE") == "PRODUCTION":
        TESTING = False
        ENV = 'production'
    else:
        TESTING = True
        ENV = 'development'

    DATA_DIR = path.join(BASEDIR, "data")

except Exception as e:
    print(f"Error on reading global config: {str(e)}")
    exit(1)
