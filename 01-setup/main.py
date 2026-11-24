# 01-setup: Environment setup

# Initialize environment variables and basic configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Basic configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

print("Environment setup complete")