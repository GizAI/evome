# Ω 시스템 개선 사항 (2025-12-08)

## ✅ 적용된 개선사항

### 1. 중복 실행 방지 (loop.sh)
**문제**: 여러 터미널에서 동시 실행 시 상태 충돌
**해결**: PID 기반 락 파일

```bash
# .loop.lock 파일로 실행 중인 프로세스 추적
# 이미 실행 중이면 에러 메시지와 함께 종료
ERROR: Loop already running (PID: 1360537)
```

**동작**:
- loop.sh 시작 시 `.loop.lock` 파일 생성
- 기존 프로세스 실행 중이면 차단
- 프로세스 종료 시 자동 정리 (trap EXIT)
- stale lock 자동 감지 및 제거

**테스트**: ✅ 통과

### 2. Feedback 우선 읽기 (EVOLUTION_PROMPT)
**문제**: 인간 피드백이 일반 작업과 동일 우선순위
**해결**: 프롬프트 첫 번째 항목으로 승격

```
1. **PRIORITY: Check feedback/ directory FIRST** - human messages override all other goals
2. Read state.yaml, metrics.yaml, mutations.log, errors.log
3. Analyze: What is your current goal? ...
```

**효과**:
- 매 사이클 시작 시 feedback/ 먼저 체크
- HIGH 피드백은 즉시 처리
- MEDIUM은 현재 목표에 통합
- LOW는 백로그 추가

---

## 📝 제공된 피드백 파일

### feedback/003-batch-execution.md (HIGH)
**주제**: 배치 실행 모드 구현
**핵심**: 조건부로 여러 독립적 작업을 한 사이클에 처리

**허용 조건**:
- 작업들이 완전히 독립적 (의존성 없음)
- 저위험 (state 파괴 가능성 낮음)
- 토큰 < 3000 (효율 유지)
- 롤백 가능 (개별 로깅)

**기대 효과**:
- 속도 3-5배 향상
- 토큰 30-40% 절감
- 안전성 유지

**구현 제안**:
```yaml
# state.yaml
execution_mode: conservative | batch | auto
batch_rules:
  max_actions: 3
  max_tokens: 3000
```

### feedback/004-additional-ideas.md (MEDIUM)
**주제**: 추가 개선 아이디어 7가지

1. **병렬 실행**: I/O 대기시간 활용, 3-4배 속도 향상
2. **예측적 캐싱**: 변경 없는 파일 읽기 스킵, 토큰 20-30% 절감
3. **점진적 목표**: 목표 자동 분해, 진행률 가시성
4. **비용 알림**: 예산 초과 방지, 자동 일시정지
5. **A/B 테스트**: 하이퍼파라미터 최적화
6. **커뮤니티 도구 공유**: GitHub 자동 동기화
7. **기타 참고 아이디어**

**우선순위 권장**:
1. 배치 실행 (즉시 효과)
2. 예측적 캐싱 (쉬운 구현)
3. 비용 알림 (위험 관리)
4. 병렬 실행 (큰 효과)

### feedback/TEMPLATE.md
**주제**: 피드백 작성 가이드

**좋은 피드백 특성**:
- ✅ 구체적: "X를 Y로 바꿔"
- ✅ 측정 가능: "토큰 30% 감소"
- ✅ 실행 가능: 명확한 행동 항목
- ✅ 근거 있음: 왜 필요한지 설명
- ✅ 테스트 가능: 성공 기준

**우선순위 가이드**:
- HIGH: 치명적 버그, 비용 폭주, 보안
- MEDIUM: 효율 개선, 기능 추가
- LOW: 장기 개선, nice-to-have

---

## 🎯 "한 사이클 = 한 행동" 효율성 분석

### 현재 방식의 장점 ✅
1. **안전성**: 각 변경사항 격리, 쉬운 롤백
2. **단순성**: 복잡한 의존성 관리 불필요
3. **디버깅**: 문제 발생 시 정확한 원인 파악
4. **학습**: outcomes.log에 명확한 인과관계

### 현재 방식의 단점 ❌
1. **토큰 중복**: 매번 state.yaml, CLAUDE.md 읽기
2. **레이턴시**: 간단한 작업도 여러 사이클 분할
3. **비용**: 30k 토큰/사이클 × 100 사이클 = 3M 토큰
4. **속도**: 목표 달성까지 긴 시간

### 개선 방향 (배치 실행)

#### 시나리오 1: 현재 방식 (Conservative)
```
목표: 3개 도구 테스트
Cycle 1: tool1 테스트 (30k 토큰, 76초)
Cycle 2: tool2 테스트 (30k 토큰, 76초)
Cycle 3: tool3 테스트 (30k 토큰, 76초)
총: 90k 토큰, 228초 (3.8분)
```

#### 시나리오 2: 배치 모드 (Proposed)
```
목표: 3개 도구 테스트
Cycle 1:
  - tool1 테스트
  - tool2 테스트
  - tool3 테스트
  (state 1번만 읽기, 한 번에 기록)
총: 35k 토큰, 85초 (1.4분)
절감: 61% 토큰, 63% 시간
```

### 하이브리드 전략 제안

```python
# 작업 분류 로직
def classify_task(task):
    if task.modifies_genome:
        return 'ATOMIC'  # 게놈 변경은 항상 단독
    if task.has_dependencies:
        return 'SEQUENTIAL'  # 의존성 있으면 순차
    if task.is_experimental:
        return 'ATOMIC'  # 실험적 작업 격리
    if task.total_tokens < 500 and task.is_idempotent:
        return 'BATCHABLE'  # 배치 가능
    return 'ATOMIC'  # 기본은 안전

# 실행 전략
if all(classify_task(t) == 'BATCHABLE' for t in tasks):
    execute_batch(tasks)  # 한 사이클에 처리
else:
    for task in tasks:
        execute_atomic(task)  # 개별 사이클
```

---

## 📊 예상 개선 효과 (배치 모드 적용 시)

### 현재 (Cycle 0-18)
- 평균 토큰/사이클: ~30,000
- 평균 시간/사이클: ~76초
- 도구 17개 생성에 소요: ~18 사이클
- 예상 100 사이클 비용: $9-15

### 배치 모드 적용 후 (예상)
- 평균 토큰/사이클: ~18,000 (-40%)
- 평균 시간/사이클: ~45초 (-41%)
- 동일 작업 완료: ~11 사이클 (-39%)
- 예상 100 사이클 비용: $5-9 (-40%)

### ROI 계산
- 구현 비용: 2-3 사이클 (배치 로직 구현)
- 회수 시점: 5-8 사이클 후
- 장기 효과: 매 사이클마다 누적

---

## 🚀 다음 단계 (권장 순서)

### 1단계: Ω에게 피드백 처리 맡기기
```bash
# 다음 사이클 실행하면 자동으로:
# 1. feedback/003-batch-execution.md 읽기
# 2. 배치 모드 설계 및 구현
# 3. state.yaml에 execution_mode 추가
# 4. CLAUDE.md 업데이트
MAX_CYCLES=5 ./loop.sh
```

### 2단계: 결과 검증
```bash
# 로그 확인
grep "batch" loop.log
grep "execution_mode" state.yaml

# 피드백 처리 확인
ls feedback/archive/003-batch-execution.md
```

### 3단계: 성능 측정
```bash
# 토큰 사용량 추이
grep "tokens used" loop.log | tail -20

# 배치 실행 통계
python tools/outcome_visualizer.py --filter batch
```

---

## 💡 추가 피드백 아이디어

### 즉시 적용 가능 (HIGH)
```markdown
# feedback/005-token-budget.md
---
priority: HIGH
topic: cost control
---

state.yaml에 일일 토큰 예산 추가:
budget:
  max_tokens_per_day: 500000
  alert_at: 400000 (80%)

80% 도달 시 feedback/budget_warning.md 자동 생성
100% 도달 시 STOP 파일 생성하여 일시정지
```

### 중기 개선 (MEDIUM)
```markdown
# feedback/006-smart-cache.md
CLAUDE.md, knowledge/*.md 등 자주 읽지만
잘 안 바뀌는 파일은 파일 해시 체크 후
캐시에서 읽기 (토큰 20% 절감 예상)
```

### 실험적 (LOW)
```markdown
# feedback/007-multi-instance.md
여러 Ω 인스턴스 병렬 실행:
- omega-research/ (연구 특화)
- omega-tools/ (도구 생성 특화)
- omega-optimize/ (최적화 특화)

각자 전문 분야에서 진화 후
주기적으로 지식/도구 공유
```

---

## 📚 참고: 파일 구조 변경사항

```
evome/
├── loop.sh                     # [수정] 중복 실행 방지 + feedback 우선
├── .loop.lock                  # [신규] PID 락 파일
├── feedback/
│   ├── 003-batch-execution.md  # [신규] 배치 모드 피드백
│   ├── 004-additional-ideas.md # [신규] 추가 아이디어
│   ├── TEMPLATE.md             # [신규] 피드백 템플릿
│   └── archive/
│       └── 002-human-message.md # 기존 처리된 피드백
└── IMPROVEMENTS.md             # [신규] 이 문서
```

---

**작성**: 2025-12-08
**다음 사이클 예상 동작**: feedback/003-batch-execution.md 처리 → 배치 모드 구현
**예상 소요**: 2-3 사이클
**예상 효과**: 즉시 40% 효율 향상
