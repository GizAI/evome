# Drive Sharing Analysis (Occam5)
> purpose: Drive 공유/권한 기능 현황 | keywords: drive, sharing, acl, permissions

## 현황 요약 (CYCLE 202)

### 구현 완료 ✓
- Share DB 모델: `ResourceShare`, `ResourceShareGrant`
- 공개 링크 (Public links)
- 이메일 공유 (초대 토큰)
- 그룹 공유
- 경로 기반 접근 (longest match)

### 버그 수정 ✓
- `check_user_access()`: `principal_id` → `principal_user_id`/`principal_group_id` 수정
- Location: `share_service.py:1010, 1030`

### 미구현 ⚠️
1. **Access level enforcement**: viewer/editor/commenter 구분 저장만 됨, 실제 적용 안됨
2. **Link expiration**: 필드만 있음, 체크 없음
3. **External restrictions**: 필드만 있음
4. **Share 테스트**: 없음

## 핵심 파일
| 파일 | 역할 |
|------|------|
| `models/share.py` | DB 모델 |
| `services/share_service.py` | 비즈니스 로직 |
| `api/share.py` | REST API |
| `auth/share_auth.py` | 인증 |
