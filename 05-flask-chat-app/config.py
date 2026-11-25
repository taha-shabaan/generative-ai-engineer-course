import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-key")
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    DB_URL = os.environ.get("SUPASE_DB_URL")
