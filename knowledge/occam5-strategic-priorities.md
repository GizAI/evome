# Occam5 Strategic Priorities (PO/PM 수준 분석)

> 분석 일시: 2025-12-08 (Cycle 126)
> 목표: Beta 런칭 (2025-12-31)

## Executive Summary

### 현황
- **NoCode 핵심 기능**: 92% 완료 (Occam4 대비)
- **E2E 테스트**: Playwright 65개 테스트 (UX-crawl 기반)
- **백엔드 테스트**: 86.4% (261/302) 통과

### 비즈니스 임팩트 기준 우선순위

| Priority | 항목 | 비즈니스 가치 | 상태 |
|----------|------|--------------|------|
| **P0** | Deepagents 기본 엔진 | 핵심 차별화 | 🔄 진행중 |
| **P0** | GizAI 사이트 마이그레이션 | 도메인 통합 | 🔄 진행중 |
| **P0** | 미디어 생성 (Image/Video/Audio) | 레거시 대체 | 🔄 진행중 |
| **P1** | Auth/SSO 안정화 | 사용자 경험 | ⚠️ 부분 |
| **P1** | Drive 공유/권한 | 협업 기능 | ⚠️ 부분 |
| **P2** | E2E 테스트 커버리지 확대 | 품질 보증 | 📊 65개 |

---

## 1. Beta Gate Requirements (12/31)

WBS_2025.md 기준 필수 조건:

### Must Have (Beta 필수)
- [ ] Deepagents가 기본 에이전트 엔진으로 작동
- [ ] www.giz.ai → 신규 앱으로 연결 (auth 통합)
- [ ] Image/Video/Audio 생성 → Drive 저장
- [ ] Core Chat/Drive 안정 (401 오류 없음)
- [ ] 로그인 없이 crawl PASS

### Nice to Have (Beta 이후)
- [ ] Nocode 앱 빌더
- [ ] Workflow/Multi-agent/AGI 목표
- [ ] VFS 데스크톱
- [ ] 사용자 CMS 사이트 생성

---

## 2. 미완료 기능 목록 (Gap Analysis 기준)

### 핵심 NoCode (92% 완료)
| 기능 | 상태 | 비고 |
|------|------|------|
| 3단계 모델 상속 | ✅ | 완료 |
| 36개 필드 타입 | ✅ | 92% (3개 누락) |
| 관계형 필드 체인 | ✅ | 완료 |
| 스키마 자동 동기화 | ✅ | 완료 |
| 25+ 필터 연산자 | ✅ | 초과 달성 |
| 25개 뷰 타입 | ✅ | GoF 리팩토링 |
| Hot Reload | ✅ | Watchdog |
| Real-time WebSocket | ✅ | Redis Pub/Sub |
| Service Decorators | ✅ | 완료 |
| Scheduled Actions | ✅ | Celery+RedBeat |
| **Record ACL** | ⚠️ | 5/7 정책 (71%) |
| **Multi-DB** | ⚠️ | 2/8 (PostgreSQL+ClickHouse) |
| **AI/ML 통합** | ❌ | 15+ 프로바이더 미통합 |

### 누락 필드 타입 (3개)
1. DataGridField (1:N 인라인 그리드)
2. onetomany
3. computed

### 누락 ACL 정책 (2개)
1. authCreator
2. groupCreator

---

## 3. E2E 테스트 현황

### 현재 커버리지 (65 tests)
| Suite | Tests | 영역 |
|-------|-------|------|
| Authentication | 4 | 로그인 |
| Organizations | 10 | 조직 관리 |
| Friends | 9 | 친구 관리 |
| Groups | 9 | 그룹 관리 |
| AI Agents | 11 | 에이전트 실행 |
| Sharing | 8 | 리소스 공유 |
| Viewers | 3 | HTML/PDF/Text 뷰어 |
| UX-Crawl | 1 | 전체 UI 스냅샷 |

### 테스트 격차 (미커버)
- [ ] Media Generation (Image/Video/Audio)
- [ ] Deepagents 워크플로우
- [ ] Drive 파일 업로드/다운로드
- [ ] Chat 메시지 전송
- [ ] SSO 통합 플로우

### 테스트 명령어
```bash
pnpm -C frontend test:e2e        # 전체 (ux-crawl)
pnpm -C frontend test:e2e:smoke  # 빠른 스모크
```

---

## 4. 권장 우선순위 (다음 3주)

### Week 1 (12/9-12/15) - Deepagents + Media
| Task | 담당 | 중요도 |
|------|------|--------|
| Deepagents 기본 엔진 안정화 | Backend | 높음 |
| Image generation → Drive | Backend | 중간 |
| E2E: Media flow 테스트 추가 | QA | 중간 |

### Week 2 (12/16-12/22) - Site Migration
| Task | 담당 | 중요도 |
|------|------|--------|
| www.giz.ai 콘텐츠 마이그레이션 | Frontend | 높음 |
| Auth/SSO 통합 | Backend | 높음 |
| E2E: 로그인 플로우 강화 | QA | 중간 |

### Week 3 (12/23-12/31) - Polish & Gate
| Task | 담당 | 중요도 |
|------|------|--------|
| Full crawl PASS 검증 | QA | 높음 |
| 401 오류 제거 | Backend | 높음 |
| 릴리스 노트/피드백 루프 | PM | 낮음 |

---

## 5. 핵심 메트릭 (KPI)

### Beta Gate 기준
- [ ] E2E 전체 PASS (login artifact 없음)
- [ ] 백엔드 테스트 >95%
- [ ] 에러율 <1%
- [ ] Chat/Media 지연시간 p95 <3s

### 현재 상태
- 백엔드: 86.4% (261/302)
- E2E: 65 tests (커버리지 미측정)
- 에러율: 미측정
- 지연시간: 미측정

---

## 6. 의사결정 필요 사항

### 즉시 결정
1. **Deepagents 레거시 셀렉터 제거 시점?**
   - 옵션 A: 12/15 제거 (강제 전환)
   - 옵션 B: 12/31까지 유지 (점진적)

2. **Multi-DB 확장 범위?**
   - 옵션 A: PostgreSQL+ClickHouse만 (현재)
   - 옵션 B: MySQL 추가
   - 옵션 C: 전체 8개 DB 지원

3. **AI/ML 통합 타이밍?**
   - 옵션 A: Beta 필수 (12/31)
   - 옵션 B: Beta 이후 (1월)

---

## 7. 리스크

| 리스크 | 확률 | 영향 | 완화책 |
|--------|------|------|--------|
| Deepagents 불안정 | 중 | 높음 | 에러 예산 + 롤백 계획 |
| 401 오류 잔존 | 높 | 중간 | storageState 고정 |
| Media gen 지연 | 중 | 중간 | GPU/Runware 폴백 |

---

*다음 액션: 이 문서를 human에게 공유하고 의사결정 요청*
