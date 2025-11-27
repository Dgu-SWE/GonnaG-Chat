import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

OPEN_API_KEY = os.getenv("OPEN_API_KEY")

SPRING_BASE_URL = os.getenv("SPRING_BASE_URL", "")

if not OPEN_API_KEY:
    print("Warning: OPEN_API_KEY is missing")
