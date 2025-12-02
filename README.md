# 나도 졸업할래 챗봇

졸업 요건 계산 및 학사 정보 조회를 지원하는 AI 챗봇 서버입니다.

## 📋 프로젝트 개요

이 프로젝트는 학생들의 졸업 요건을 분석하고, 학사 정보를 조회하며, 수업 추천 및 공지사항 안내를 제공하는 챗봇 서버입니다. DSPy 프레임워크를 활용하여 의도 기반 라우팅과 전문가 에이전트 시스템을 구현했습니다.

### 주요 기능

- **졸업 요건 계산**: 사용자의 성적 정보와 졸업 요건 가이드를 비교하여 졸업 가능 여부 및 부족한 학점을 분석
- **학사 정보 조회**: 사용자의 이름, 학번, 학점, 전공 등 개인 정보 조회
- **공지사항 안내**: 학교 공지사항 및 장학금 정보 제공
- **수업 추천**: 사용자의 전공과 수강 이력을 기반으로 적절한 수업 추천
- **일반 대화**: 학사 관련 질문 외의 일반적인 대화 지원

## 🏗️ 프로젝트 구조

프로젝트는 유지보수성과 확장성을 고려하여 계층형 아키텍처로 설계되었습니다.

```
Gonnag-AI/
├── main.py                 # FastAPI 애플리케이션 진입점
├── requirements.txt        # 프로젝트 의존성
├── README.md              # 프로젝트 문서
└── src/
    ├── __init__.py
    ├── config.py          # 환경 변수 및 설정 관리
    ├── agents/            # AI 에이전트 모듈
    │   ├── __init__.py
    │   ├── orchestrator.py    # 메인 오케스트레이터 (의도별 처리 로직)
    │   ├── router.py          # 의도 분류 라우터
    │   └── signatures.py      # DSPy 시그니처 정의 (각 에이전트의 입출력 스키마)
    ├── api/               # API 라우트
    │   ├── __init__.py
    │   └── routes.py          # FastAPI 엔드포인트 정의
    ├── schemas/           # 데이터 스키마
    │   ├── __init__.py
    │   └── chat.py            # Pydantic 모델 정의
    └── services/          # 외부 서비스 클라이언트
        ├── __init__.py
        └── mcp_client.py      # Spring 서버 MCP 클라이언트
```

## 🔄 시스템 아키텍처

### 요청 처리 흐름

```
사용자 질문
    ↓
[API Layer] routes.py - /api/chat 엔드포인트
    ↓
[Orchestrator] orchestrator.py - process_user_query()
    ↓
[Router] router.py - RouterAgent (의도 분류)
    ↓
[Specialized Agent] signatures.py의 각 Signature
    ↓
[Service Layer] mcp_client.py - Spring 서버 데이터 조회
    ↓
응답 반환
```

### 계층별 역할

#### 1. **API Layer** (`src/api/routes.py`)
- FastAPI 라우터를 통한 HTTP 요청 처리
- 요청 검증 및 에러 핸들링
- 클라이언트와의 인터페이스 담당

#### 2. **Orchestrator Layer** (`src/agents/orchestrator.py`)
- 사용자 질문의 의도를 분석하여 적절한 에이전트로 라우팅
- 각 의도별로 필요한 데이터를 조회하고 전문 에이전트에 전달
- 전체 대화 흐름을 조율하는 중앙 컨트롤러 역할

#### 3. **Router Agent** (`src/agents/router.py`)
- DSPy ChainOfThought를 활용한 의도 분류
- 사용자 질문을 다음 6가지 의도로 분류:
  - `user_info`: 사용자 개인 정보 조회
  - `graduation`: 졸업 요건 계산 및 분석
  - `announcement`: 공지사항 조회
  - `recommendation`: 수업 추천
  - `test`: 시스템 테스트
  - `general`: 일반 대화

#### 4. **Specialized Agents** (`src/agents/signatures.py`)
각 의도별로 전문화된 DSPy Signature를 정의:
- **UserInfoSignature**: 사용자 정보 기반 답변 생성
- **GraduationSignature**: 졸업 요건 분석 및 계산 (핵심 기능)
- **AnnouncementSignature**: 공지사항 요약 및 안내
- **RecommendationSignature**: 수업 추천
- **TestMcpSignature**: MCP 테스트 결과 보고

#### 5. **Service Layer** (`src/services/mcp_client.py`)
- Spring 서버와의 통신 담당
- MCP(Model Context Protocol) 클라이언트 구현
- 제공 함수:
  - `fetch_user_info()`: 사용자 정보 조회
  - `fetch_academic_guide()`: 졸업 요건 가이드 조회
  - `fetch_announcements()`: 공지사항 조회
  - `fetch_class_info()`: 수업 정보 조회

#### 6. **Configuration** (`src/config.py`)
- 환경 변수 관리 (`.env` 파일 로드)
- API 키 및 외부 서버 URL 설정
- 배포 환경별 설정 분리

## 🎯 핵심 기능: 졸업 요건 계산

졸업 요건 계산은 `GraduationSignature`를 통해 수행됩니다.

### 처리 과정

1. **의도 분류**: 사용자 질문에서 "graduation" 의도 감지
2. **데이터 수집**:
   - `fetch_user_info(user_id)`: 사용자의 성적 정보
   - `fetch_academic_guide(user_id)`: 졸업 요건 가이드
3. **분석 및 답변 생성**:
   - DSPy Predict 모듈이 두 데이터를 비교 분석
   - 졸업 가능 여부, 부족한 학점, 이수 현황 등을 종합하여 답변 생성

### 예시 질문
- "나는 졸업할 수 있어?"
- "전공 필수 과목 몇 개 더 들어야 해?"
- "졸업까지 남은 학점이 얼마야?"

## 🛠️ 기술 스택

- **FastAPI**: 비동기 웹 프레임워크
- **DSPy**: 구조화된 LLM 프로그래밍 프레임워크
- **OpenAI GPT-4o**: 언어 모델
- **Pydantic**: 데이터 검증 및 스키마 정의
- **httpx**: 비동기 HTTP 클라이언트
- **python-dotenv**: 환경 변수 관리

## 📦 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 변수를 설정하세요:

```env
OPEN_API_KEY=your_openai_api_key
SPRING_BASE_URL=http://localhost:8080
```

### 3. 서버 실행

```bash
python main.py
```

서버는 `http://0.0.0.0:8000`에서 실행됩니다.

## 🔌 API 사용법

### 채팅 요청

**엔드포인트**: `POST /api/chat`

**요청 본문**:
```json
{
  "user_id": 1,
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "나는 졸업할 수 있어?"
    }
  ],
  "temperature": 0.7
}
```

**응답**:
```json
{
  "role": "assistnt",
  "content": "졸업 요건 분석 결과..."
}
```

## 🎨 설계 원칙

### 1. **관심사의 분리 (Separation of Concerns)**
- 각 계층이 명확한 책임을 가짐
- API, 비즈니스 로직, 데이터 접근이 분리됨

### 2. **확장성 (Extensibility)**
- 새로운 의도나 에이전트를 추가하기 쉬운 구조
- `signatures.py`에 새로운 Signature 추가만으로 기능 확장 가능

### 3. **유지보수성 (Maintainability)**
- 모듈화된 구조로 각 컴포넌트를 독립적으로 수정 가능
- 명확한 파일 구조와 네이밍 컨벤션

### 4. **테스트 용이성 (Testability)**
- 각 계층이 독립적으로 테스트 가능
- 외부 의존성(Spring 서버)을 `services` 계층으로 격리

## 🔧 유지보수 가이드

### 새로운 의도 추가하기

1. **`signatures.py`에 Signature 추가**:
```python
class NewIntentSignature(dspy.Signature):
    """새로운 의도에 대한 설명"""
    input_field = dspy.InputField(desc="입력 필드 설명")
    answer = dspy.OutputField(desc="답변")
```

2. **`router.py`의 RouterSignature에 의도 추가**:
```python
intent: Literal[
    ...,
    "new_intent",
] = dspy.OutputField(desc="의도 분류 결과")
```

3. **`orchestrator.py`에 처리 로직 추가**:
```python
elif "new_intent" in intent:
    # 필요한 데이터 조회
    data = await fetch_data(user_id)
    # 에이전트 실행
    agent = dspy.Predict(NewIntentSignature)
    res = agent(data=data, question=user_query)
    return res.answer
```

### 새로운 외부 API 추가하기

`src/services/mcp_client.py`에 새로운 함수를 추가하세요:

```python
async def fetch_new_data(id: int):
    return await _post("/mcp/new-endpoint", id)
```

## 📝 참고사항

- DSPy의 ChainOfThought를 활용하여 추론 과정을 구조화했습니다.
- Spring 서버와의 통신은 MCP(Model Context Protocol)를 통해 이루어집니다.
- 환경 변수는 배포 환경에 따라 자동으로 로드됩니다.
