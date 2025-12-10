# Auth/SSO Integration Plan: giz → occam5
> purpose: giz-occam5 인증 통합 전략 | keywords: auth, sso, jwt, oauth, migration

## 현황 비교

| 항목 | giz (NestJS) | occam5 (FastAPI) |
|------|--------------|------------------|
| Framework | @nestjs/jwt | python-jose + FastAPI Users |
| JWT Secret | `GIZ_MASTER_KEY` | `SECRET_KEY` |
| Algorithm | HS256 | HS256 |
| Password | bcrypt | argon2 (bcrypt fallback) |
| Google OAuth | `965458515537-...` | `965458515537-...` (동일) |
| Token Expiry | 20m access, 365d refresh | configurable |

## 통합 전략

### Phase 1: JWT Secret 통일 (즉시)
```bash
# occam5/.env
SECRET_KEY=IamYourFather!  # giz GIZ_MASTER_KEY와 동일
```
- 효과: giz 토큰이 occam5에서도 유효
- 리스크: 낮음 (같은 알고리즘)

### Phase 2: 사용자 DB 마이그레이션
- giz: `giz_principal` 테이블 (bcrypt password)
- occam5: `user` 테이블 (argon2, bcrypt fallback)
- 마이그레이션 스크립트 필요

### Phase 3: 도메인 연결
1. giz.ai 랜딩 → occam5 앱 링크
2. 공통 인증 쿠키 (`.giz.ai` 도메인)
3. 또는 JWT 토큰 URL 파라미터 전달

## 구현 우선순위

1. **P0**: JWT Secret 통일 (5분)
2. **P1**: 테스트 - giz 토큰으로 occam5 API 호출 검증
3. **P2**: 사용자 마이그레이션 스크립트
4. **P3**: 도메인/쿠키 설정

## 코드 위치

### giz
- `platform/server/src/auth/auth.module.ts:38` - JWT secret 설정
- `platform/server/src/auth/auth.service.ts` - 인증 로직
- `platform/web2/src/services/authApi.ts` - 프론트엔드 API

### occam5
- `backend/app/auth/jwt_handler.py` - JWT 처리
- `backend/app/auth/fastapi_users_setup.py` - FastAPI Users 설정
- `.env` - SECRET_KEY

## 진행 상황

### Phase 1: JWT Secret 통일 ✅ DONE (CYCLE 184)
- [x] occam5 SECRET_KEY 변경: `IamYourFather!` (giz와 동일)
- [x] gunicorn HUP reload로 적용 완료
- [x] occam5 로그인 테스트 성공: JWT 발급 정상

### JWT 구조 차이 발견
| 항목 | giz | occam5 |
|------|-----|--------|
| Payload | 전체 User 객체 | `{sub, aud, exp}` |
| `sub` | user.id | UUID |
| `aud` | 없음 | `["fastapi-users:auth"]` |

**문제**: Secret은 동일해도 payload 구조가 달라 상호 검증 불가

### 해결 옵션
1. **giz 수정**: occam5 JWT 구조 인식 (giz middleware 수정)
2. **occam5 수정**: giz JWT 구조로 발급 (fastapi-users 커스텀)
3. **Proxy/Gateway**: 별도 인증 서버에서 토큰 변환

**권장**: 옵션 1 (giz가 레거시, occam5가 신규)

## Phase 2: JWT 상호 인식 ✅ DONE (CYCLE 186)

### 구현 완료
- [x] `giz/platform/server/src/auth/jwt.strategy.ts` 수정
  - `payload.id ?? payload.sub` 로 양쪽 형식 인식
  - occam5 토큰 (sub만 있는 경우) → id 필드에 복사하여 giz 형식으로 정규화
- [x] `giz/platform/server/src/auth/jwt.middleware.ts` 수정
  - JWT 검증 후 `sub` → `id` 정규화 로직 추가

### 결과
- giz 서버가 occam5 JWT (`{sub, email, role}`) 인식 가능
- 동일 Secret 사용 (IamYourFather!)
- 양방향 SSO 기반 완료

## Phase 3: 사용자 마이그레이션 (CYCLE 197)

### migrate_giz_users.py dry-run 성공
```bash
DATABASE_URL="postgresql://occam:occam_password@localhost:5432/occam" \
  python scripts/migrate_giz_users.py --dry-run --limit 5
# Found 5 users in Giz - all would be created
```

### 실제 마이그레이션 명령
```bash
cd /home/user/occam5/backend
DATABASE_URL="postgresql://occam:occam_password@localhost:5432/occam" \
  python scripts/migrate_giz_users.py
```

### 다음 액션
- [x] JWT secret 통일 (Phase 1)
- [x] JWT 상호 인식 코드 (Phase 2)
- [x] migrate_giz_users.py dry-run 테스트 (Phase 3)
- [x] giz JWT SSO 코드 커밋 (ca61d7cf9) - CYCLE 198
- [ ] **BLOCKED - 인간 필요**: giz 서버 배포 (원격 서버 SSH 접근 필요)
- [ ] **BLOCKED - 인간 확인 후**: 실제 사용자 마이그레이션 실행

## 현재 상태 (CYCLE 200)
- **코드 완료**: giz JWT SSO 커밋됨 (ca61d7cf9)
- **배포 대기**: 원격 giz 서버에 SSH 접근 불가
- **다음 단계**: 인간이 `ssh giz-server && pm2 restart all` 실행 필요
