# Human Feedback 006: new.giz.ai 배포 및 검증 지시

**From:** 김경태
**Date:** 2025-12-08
**Priority:** HIGH

## 지시사항

1. **new.giz.ai에 Occam5 배포** - 라이브 마이그레이션 전 검증용
2. **스스로 먼저 검증** - 내가 직접 테스트하기 전에 E2E 전체 플로우 확인
3. **검증 완료 후 보고** - 어떤 기능이 작동/미작동인지 명확히

## 검증 체크리스트 (최소)

- [ ] 로그인/회원가입
- [ ] 채팅 기본 기능
- [ ] 이미지 생성
- [ ] 파일 업로드/다운로드
- [ ] Agent 실행

## 배포 정보

- **도메인**: new.giz.ai
- **목적**: 베타 검증 (마이그레이션 전 최종 확인)
- **참고**: ~/twenim/docs/occam5/gizai-migration-plan.md (통합 문서)

스스로 검증 완료하고 결과 보고해라. 그 다음 내가 직접 확인한다.

## 문서 정리 지침

- **마이그레이션 가이드 통합 완료**: `~/twenim/docs/occam5/gizai-migration-plan.md`
- occam5 프로젝트 내 DEPLOYMENT_GUIDE.md 두 개는 위 문서로 대체됨
- **앞으로 문서는 twenim/docs/ 에 작성할 것**
- **twenim/docs/ 문서들 적극 참조할 것** - GizAI 운영, Occam5 계획 등 핵심 정보 있음
