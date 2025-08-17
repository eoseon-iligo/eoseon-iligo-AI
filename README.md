# eoseon

**유후어선 멘토링 연계 서비스**  

> 디렉토리 구조 (Clean Architecture 기반 DDD)
> 이 프로젝튼 PEP8 스타일 가이드를 준수하며, 커밋 시 코드 품질을 자동으로 검증하고 정리하기 위해 pre-commit 훅이 사용 됩니다.

### 사용 도구
- black: Python 코드 자동 포매터
- ruffL Python linter
- pre-commit: 커밋 전 자동 포맷 & 린트 실행

```bash
poetry install
poetry run pre-commit install
```


## 사용한 기술

### 언어
- Python

### 프레임워크
- [FastAPI](https://fastapi.tiangolo.com/ko/)

### 라이브러리
- [SQLAlchemy](https://www.sqlalchemy.org/)

### 의존성 관리
- [Poetry](https://python-poetry.org/)

## 실행 방법

```bash
poetry install
uvicorn app.main:app --reload
```

