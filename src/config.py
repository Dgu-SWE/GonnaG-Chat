import os
from dotenv import load_dotenv

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY", "")
SPRING_BASE_URL = os.getenv("SPRING_BASE_URL", "")
