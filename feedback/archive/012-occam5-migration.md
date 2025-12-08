# Occam5 프로젝트 완성 지시

## Priority: CRITICAL ⚠️ IMMEDIATE ACTION REQUIRED

**현재 시간**: 2025-12-08 10:40
**지시**: SWE-Bench Pro 작업을 **즉시 중단**하고 이 피드백을 처리하라

**Objective**: SWE-Bench Pro 작업 중단 → Occam5 프로젝트 완성으로 전환

---

## Task 1: twenim에서 Chrome DevTools 지식 수집

### 목표
상위 폴더의 `/home/user/twenim` 저장소에서 Chrome DevTools 사용법을 분석하고 Occam5에 구현 가능한 형태로 정리

### 구체적 작업
1. twenim 저장소 분석:
   - `/twenim/docs/gizai/conversion/browser-testing.md` 분석
   - `/twenim/scripts/collect/collectors/browser.py` 분석
   - `/twenim/scripts/gizai/browser_collector.py` 분석

2. Chrome DevTools 주요 기능 추출:
   - 페이지 탐색 (navigate, select, list)
   - UI 상태 확인 (snapshot, screenshot)
   - 요소 조작 (click, fill, press_key)
   - JavaScript 평가 (evaluate_script)
   - 디버깅 (console, network)

3. 결과물:
   - `/home/user/evome/knowledge/chrome-devtools-usage-guide.md` 생성
   - Occam5 구현 가능한 코드 패턴 포함

---

## Task 2: Giz 프로젝트 분석

### 목표
`/home/user/giz` 저장소의 구조, 데이터베이스, 기능을 완전히 파악

### 구체적 작업
1. Giz 저장소 분석:
   - README.md 읽기
   - 프로젝트 구조 파악 (apps, plugins, common 폴더)
   - package.json 분석 (의존성, 스크립트)
   - 데이터베이스 모델 파악 (if exists)

2. 주요 플러그인 분석:
   - storage (에이전트 저장소)
   - tiptap (에디터)
   - ej2 (UI 컴포넌트)
   - search (검색 기능)
   - ai (AI 기능)

3. 결과물:
   - `/home/user/evome/knowledge/giz-project-structure.md` 생성
   - DB 스키마 정리
   - API 엔드포인트 목록

---

## Task 3: Occam5 프로젝트 현황 파악

### 목표
Occam5의 현재 상태, 기능, 개발 상황을 파악

### 구체적 작업
1. Occam5 분석:
   - README.md 읽기
   - AGENTS.md 읽기 (현재 에이전트 목록)
   - 프로젝트 구조 파악
   - .env 설정 확인

2. 현재 구현된 기능 정리:
   - 에이전트 목록
   - API 엔드포인트
   - 데이터베이스 모델
   - UI 컴포넌트

3. 결과물:
   - `/home/user/evome/knowledge/occam5-current-state.md` 생성
   - 마이그레이션 필요 항목 목록화

---

## Task 4: Giz → Occam5 마이그레이션 계획 수립

### 목표
Giz 기능을 Occam5로 이전하기 위한 구체적 계획 수립

### 구체적 작업
1. 데이터베이스 마이그레이션 계획:
   - Giz DB 스키마 → Occam5 DB 스키마 매핑
   - 마이그레이션 스크립트 작성 계획
   - 데이터 손실 없이 전환 전략

2. 기능 마이그레이션 계획:
   - Giz의 각 플러그인 → Occam5 에이전트로 변환
   - API 호환성 검토
   - UI 통합 전략

3. 결과물:
   - `/home/user/evome/knowledge/occam5-migration-plan.md` 생성
   - 단계별 마이그레이션 로드맵

---

## Task 5: 마이그레이션 구현

### 목표
실제 Giz → Occam5 데이터 및 기능 마이그레이션 수행

### 작업 순서
1. 데이터베이스 백업 (Giz, Occam5 모두)
2. 스키마 변환 스크립트 작성 및 테스트
3. 데이터 마이그레이션 수행
4. 기능 마이그레이션 (에이전트 구현)
5. 통합 테스트

---

## Task 6: Chrome DevTools 기능 구현

### 목표
twenim에서 배운 Chrome DevTools 패턴을 Occam5에 구현

### 작업 내용
- MCP (Model Context Protocol) 기반 Chrome DevTools 통합
- 페이지 자동화, 스냅샷, JavaScript 평가 등 구현

---

## Task 7: 배포 및 오픈 준비

### 목표
Occam5 프로젝트를 프로덕션 배포 준비

### 작업 내용
1. 배포 준비:
   - 환경 변수 설정 검증
   - 데이터베이스 마이그레이션 검증
   - 통합 테스트 완료

2. 오픈 준비:
   - 문서 작성 (사용자 가이드, API 문서)
   - 릴리스 노트 작성
   - GitHub 설정 (tags, releases)

3. 시스템 전환:
   - Giz → Occam5 전환 계획
   - 롤백 계획 수립

---

## 현재 상태

**저장 위치**:
- Giz: `/home/user/giz`
- Occam5: `/home/user/occam5`
- twenim (참고): `/home/user/twenim`

**예상 소요 시간**: 30-50 cycles (이전 SWE-Bench는 보관)

**성공 기준**:
- Chrome DevTools 지식 수집 완료 ✓
- Giz 분석 완료 ✓
- Occam5 현황 파악 완료 ✓
- 마이그레이션 계획 수립 ✓
- 마이그레이션 구현 완료 ✓
- 배포 및 오픈 준비 완료 ✓

---

**시작 시간**: 즉시
**모니터링**: 사용자가 수행 (evome 자동 진행)

