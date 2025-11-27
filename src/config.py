import os
from pathlib import Path
from dotenv import load_dotenv

# 1. .env 파일 로드 (로컬용)
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# 2. API Key 설정 (사용자님 코드에 맞춰 OPEN_API_KEY로 유지)
# Cloudtype 환경변수 이름과 토씨 하나 안 틀리고 같아야 합니다.
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

# 3. [핵심] Spring 서버 주소 가져오기
# 만약 배포 환경에서 이 값이 안 읽히면, 기본값(localhost)이 들어가게 됩니다.
# Cloudtype의 변수명: SPRING_BASE_URL
SPRING_BASE_URL = os.getenv("SPRING_BASE_URL", "http://localhost:8080")

# [디버깅] 배포 로그에서 확인하기 위해 출력 (중요!)
print(f"Server Start - SPRING_BASE_URL: {SPRING_BASE_URL}")

if not OPEN_API_KEY:
    print("Warning: OPEN_API_KEY is missing")
