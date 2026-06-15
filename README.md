# Cosmecca 코드 압축본 실행 가이드

이 문서는 `cosmecca_frontend_backend_code_only.zip` 압축 파일을 받은 사람이 로컬 PC에서 프론트엔드와 백엔드를 실행하기 위한 작업 순서입니다.

압축 파일에는 코드만 포함되어 있으며, 문서, 환경변수 파일, DB 파일, 빌드 결과물, 캐시, 의존성 폴더는 제외되어 있습니다.

## 1. 사전 준비

아래 프로그램이 설치되어 있어야 합니다.

- Node.js 20 이상
- Python 3.11 이상
- npm

압축을 풀면 다음 폴더가 있어야 합니다.

```bash
frontend/
backend/
```

## 2. 압축 해제

```bash
unzip cosmecca_frontend_backend_code_only.zip
cd cosmecca
```

압축을 푼 위치에 따라 `cd cosmecca` 경로는 달라질 수 있습니다. 중요한 것은 `frontend`, `backend` 폴더가 있는 루트에서 작업하는 것입니다.

## 3. 백엔드 실행

### 3.1 가상환경 생성 및 패키지 설치

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Windows PowerShell에서는 가상환경 활성화 명령이 다릅니다.

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 3.2 로컬 환경변수 파일 생성

압축 파일에는 `.env`가 포함되어 있지 않으므로 필요하면 `backend/.env`를 새로 만듭니다.

```env
APP_ENV=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite+aiosqlite:///./cosmecca.db
SECRET_KEY=local-dev-secret-key-change-me
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

개발 확인만 할 경우 기본값으로도 실행할 수 있지만, `DEBUG=true`를 넣으면 Swagger 문서를 볼 수 있습니다.

### 3.3 SQLite DB 생성

DB 파일은 압축에서 제외되어 있으므로 최초 1회 테이블을 생성해야 합니다.

```bash
python - <<'PY'
import asyncio

import app.models
from app.db.base import Base
from app.db.session import engine

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

asyncio.run(main())
PY
```

이 명령을 실행하면 `backend/cosmecca.db`가 생성됩니다.

### 3.4 백엔드 서버 실행

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

확인 URL:

- API 루트: `http://localhost:8000/`
- Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/api/v1/openapi.json`

## 4. 프론트엔드 실행

새 터미널을 열고 루트에서 진행합니다.

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 기본적으로 Vite 개발 서버 `http://localhost:5173`에서 실행됩니다.

프론트 API 요청은 `/api` 경로로 나가며, 개발 서버 설정에서 `http://localhost:8000` 백엔드로 프록시됩니다. 따라서 백엔드를 먼저 실행한 뒤 프론트를 실행하는 것을 권장합니다.

확인 URL:

- 프론트 메인: `http://localhost:5173/`
- 작업자 동선 관리: `http://localhost:5173/worker-flow`
- MES 연동: `http://localhost:5173/mes-integration`

## 5. 빌드 확인

프론트 빌드:

```bash
cd frontend
npm run build
```

백엔드 import 확인:

```bash
cd backend
source .venv/bin/activate
python -c "from app.main import app; print(app.title)"
```

## 6. 자주 생기는 문제

### `ModuleNotFoundError: No module named 'app'`

백엔드 명령은 반드시 `backend` 폴더 안에서 실행해야 합니다.

```bash
cd backend
uvicorn app.main:app --reload
```

### `no such table` 오류

DB 테이블이 아직 생성되지 않은 상태입니다. `3.3 SQLite DB 생성` 명령을 다시 실행한 뒤 서버를 재시작합니다.

### 프론트에서 API 호출이 실패하는 경우

백엔드가 `http://localhost:8000`에서 실행 중인지 확인합니다.

```bash
curl http://localhost:8000/
```

또한 프론트 개발 서버는 `frontend/vite.config.ts`의 프록시 설정을 사용합니다.

### Swagger가 열리지 않는 경우

`backend/.env`에 `DEBUG=true`가 들어가 있는지 확인한 뒤 백엔드 서버를 재시작합니다.

## 7. 운영 또는 PostgreSQL 사용 시

현재 빠른 로컬 실행 가이드는 SQLite 기준입니다. PostgreSQL을 사용하려면 다음 항목을 별도로 설정해야 합니다.

- `backend/.env`의 `DATABASE_URL`
- PostgreSQL DB 생성
- 필요한 DB 계정/권한
- Alembic 설정 또는 마이그레이션 실행 방식

운영 배포에서는 `SECRET_KEY`를 반드시 안전한 랜덤 문자열로 교체하고, `DEBUG=false`로 설정합니다.
