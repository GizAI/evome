# Human Feedback 018: new.giz.ai 서버 접근 정보

**From:** 김경태
**Date:** 2025-12-08

## 서버 정보

**new.giz.ai (Occam5)**: `ssh root@103.63.28.134`

상세: `~/twenim/docs/gizai/ops/infra.md`

## 서비스 구성 (포트)
- 5432: PostgreSQL
- 6379: Redis
- 8001: Gunicorn (FastAPI backend)
- 8123: ClickHouse
- 9000: MinIO
- 19530: Milvus

백엔드 502면 8001 포트 서비스 확인해라.
