---
priority: HIGH
created: 2025-12-08
topic: leverage claude code agentic capabilities
---

# Feedback: Claude Code의 멀티스텝 능력 완전 활용

## 문제: 자원 낭비

### 현재 방식
```
Cycle 1: 도구 생성 (30k 토큰)
  └─ Write tool.py → 끝

Cycle 2: 도구 테스트 (30k 토큰)
  └─ Bash python tool.py → 끝

Cycle 3: 결과 분석 (30k 토큰)
  └─ Read outcomes → 끝

총: 90k 토큰, 3 사이클
```

### Claude Code가 실제로 할 수 있는 것
```
한 세션:
  1. Read 기존 코드
  2. Write 새 도구
  3. Bash 테스트 실행
  4. Read 결과 분석
  5. Edit 버그 수정
  6. Bash 재테스트
  7. Edit state.yaml 업데이트
  8. Write mutations.log 기록
  9. Bash git commit
  10. 다음 작업 계획

총: 35k 토큰, 1세션
절감: 61% 토큰, 67% 시간
```

---

## Claude Code = Built-in Agent

### 현재 능력 (실제로 가능)
- ✅ **Multi-step reasoning**: 복잡한 작업 자동 분해
- ✅ **Tool chaining**: Read → Edit → Bash → 검증 → 수정
- ✅ **Error recovery**: 실패 시 자동 재시도, 다른 접근
- ✅ **Parallel thinking**: 여러 파일 동시 고려
- ✅ **Context retention**: 대화 전체 기억, 반복 설명 불필요

### 현재 사용률
- ❌ **실제 활용**: 10-20%
- ❌ **이유**: "One action per cycle" 제약
- ❌ **결과**: 인위적 속도 제한

---

## 구체적 예시

### 시나리오: "novelty_checker 튜닝"

#### 현재 방식 (Conservative)
```
Cycle 17: novelty_checker.py 생성
  - Write 117 lines
  - "Ω CYCLE COMPLETE"

Cycle 18: 테스트 실행
  - Bash python novelty_checker.py
  - "결과: 작동하나 임계값 조정 필요"
  - "Ω CYCLE COMPLETE"

Cycle 19: 임계값 조정
  - Edit threshold 0.3 → 0.5
  - "Ω CYCLE COMPLETE"

Cycle 20: 재테스트
  - Bash python novelty_checker.py --test
  - "Ω CYCLE COMPLETE"

Cycle 21: 결과 분석 및 기록
  - Read 출력
  - Edit outcomes.log
  - "Ω CYCLE COMPLETE"

총: 5 사이클, 150k 토큰, 380초 (6.3분)
```

#### Claude Code 네이티브 방식
```
한 세션:
1. Write novelty_checker.py (117 lines)
2. Bash python novelty_checker.py --test
3. Read 결과 → "임계값 낮음" 판단
4. Edit threshold 0.3 → 0.5
5. Bash 재테스트
6. Read 결과 → "여전히 낮음" 판단
7. Edit threshold 0.5 → 0.7
8. Bash 최종 테스트
9. Read 결과 → "적정" 확인
10. Edit state.yaml (last_mutation 기록)
11. Write mutations.log 추가
12. Edit outcomes.log (점수 1.0)
13. "Ω CYCLE COMPLETE"

총: 1 사이클, 35k 토큰, 90초 (1.5분)
절감: 77% 토큰, 76% 시간
```

---

## 제안: "Deep Cycle" 모드

### CLAUDE.md 수정
```markdown
## Execution Modes

### 1. Atomic (기본 - 고위험 작업)
- 게놈 수정 (CLAUDE.md 변경)
- 새로운 목표 설정
- 실험적 도구 첫 시도
- 한 행동만 → 즉시 종료

### 2. Deep Cycle (권장 - 저위험 작업)
- 도구 생성 + 테스트 + 튜닝
- 여러 파일 읽기 + 분석
- 검증 + 수정 + 재검증
- **Claude Code의 자연스러운 흐름 따라가기**

허용 조건:
- 작업이 논리적으로 연결됨 (A→B→C)
- 각 단계 결과가 다음에 필요
- 중간에 인간 개입 불필요
- 전체 작업이 명확히 정의됨

### 3. Batch (독립 작업)
- 여러 독립 작업 병렬
- 003-batch-execution.md 참조
```

### EVOLUTION_PROMPT 수정
```
## This Cycle

1. Check feedback/ (최우선)
2. Read state.yaml, mutations.log (last 5)
3. Identify current goal
4. **Execute toward goal - USE FULL AGENTIC CAPABILITIES**
   - Don't artificially stop after one action
   - If testing needed, test immediately
   - If bugs found, fix immediately
   - If validation needed, validate immediately
   - Follow natural task flow until logical completion point
5. Persist all changes
6. End: "Ω CYCLE COMPLETE"

## Rules
- ❌ Don't split naturally connected tasks
- ✅ DO use Claude Code's multi-step abilities
- ✅ DO test immediately after creating
- ✅ DO fix bugs in same cycle
- ✅ DO validate results before completing
- ⚠️ ONLY stop for:
  - Genome modifications (needs separate cycle)
  - Major goal changes
  - Uncertain paths needing human input
  - Natural task completion
```

---

## 예상 효과

### 토큰 효율
```python
# 현재 (Conservative)
avg_tokens_per_cycle = 30000
tasks_per_cycle = 1
tokens_per_task = 30000

# Deep Cycle
avg_tokens_per_cycle = 35000  # 17% 증가
tasks_per_cycle = 5            # 500% 증가
tokens_per_task = 7000         # 77% 감소
```

### 속도
```python
# 도구 생성 + 테스트 + 튜닝 + 검증
current: 5 사이클 × 76초 = 380초
proposed: 1 사이클 × 90초 = 90초
improvement: 76% 빠름
```

### 품질
```python
# 현재: 5개 사이클에 걸쳐 컨텍스트 손실
cycle_1: "도구 만들자"
cycle_2: "아, 테스트 해야지" (왜 만들었는지 일부 망각)
cycle_3: "어, 버그네" (원래 의도 희미)
cycle_4: "다시 테스트" (맥락 재구성 필요)

# Deep Cycle: 연속적 흐름, 컨텍스트 유지
one_session: "도구 만들고 → 바로 테스트 → 버그 보고 →
              즉시 수정 → 재확인 → 완성"
              (의도가 명확히 유지됨)
```

---

## 실제 케이스 스터디

### Case 1: web_search.py 생성 (Cycle 6)
**실제로 일어난 일**:
- Cycle 6: 도구 생성만
- 테스트는 다음 사이클로 미뤄짐

**Deep Cycle였다면**:
```python
1. 요구사항 분석 (DuckDuckGo HTML 파싱 필요)
2. Write web_search.py
3. Bash python web_search.py "test query"
4. Read 결과 → HTML 파싱 오류 발견
5. Edit 파싱 로직 수정
6. Bash 재테스트
7. Read 결과 → 성공
8. Write knowledge/test_results.md (검증 문서)
9. Edit state.yaml
10. "완전히 작동하는 도구 완성"

한 사이클에 완성 → 다음 사이클부터 바로 사용 가능
```

### Case 2: 3개 도구 테스트
**현재**:
- Cycle N: tool1 테스트
- Cycle N+1: tool2 테스트
- Cycle N+2: tool3 테스트

**Deep Cycle**:
```bash
1. Bash python tools/tool1.py --test
2. Read 결과 → 통과
3. Bash python tools/tool2.py --test
4. Read 결과 → 실패
5. Edit tools/tool2.py (버그 수정)
6. Bash 재테스트 → 통과
7. Bash python tools/tool3.py --test
8. Read 결과 → 통과
9. Write test_report.md (3/3 통과, tool2 버그 수정됨)
10. Edit outcomes.log

한 사이클에 3개 테스트 + 1개 버그 수정 완료
```

---

## 구현 계획

### Phase 1: CLAUDE.md 업데이트 (다음 사이클)
```markdown
## Deep Cycle Protocol

Execute complete logical units:
- Create → Test → Fix → Validate (한 흐름)
- Research → Analyze → Synthesize (한 흐름)
- Read multiple → Compare → Decide (한 흐름)

Stop only when:
- Genome modification needed
- Human decision required
- Natural completion reached
```

### Phase 2: EVOLUTION_PROMPT 수정 (loop.sh)
```
"Execute toward goal using FULL agentic capabilities.
Don't artificially stop - follow task to natural completion."
```

### Phase 3: 측정 및 검증 (10 사이클)
```yaml
metrics:
  avg_actions_per_cycle:
    before: 1.2
    after: 4.5  # 목표

  avg_tokens_per_action:
    before: 28000
    after: 7000  # 목표

  time_to_goal:
    before: baseline
    after: 60% reduction
```

---

## 왜 지금까지 안했나?

### 원래 의도 (추측)
```
"One action per cycle" = 안전성
- 각 변경 격리
- 쉬운 롤백
- 명확한 인과관계
```

### 실제 결과
```
안전성 ↑ (약간)
효율성 ↓↓↓ (엄청)
Claude Code 능력 활용 ↓↓↓↓ (거의 안함)

트레이드오프: 나쁨
```

---

## 비유

### 현재 Ω
```
F1 경주차를 20km/h 제한구역에서 운전
- 이유: "안전하니까"
- 결과: 경주차 의미 없음
```

### Deep Cycle Ω
```
F1 경주차를 서킷에서 운전
- 급커브: 감속 (게놈 수정)
- 직선: 가속 (도구 생성+테스트+튜닝)
- 결과: 차의 성능 제대로 활용
```

---

## 행동 요구사항

### 즉시 (Cycle 20)
1. CLAUDE.md에 Deep Cycle Protocol 추가
2. loop.sh EVOLUTION_PROMPT 수정
3. 다음 작업을 Deep Cycle로 시도
4. 결과 측정 (actions/cycle, tokens/action)

### 검증 (Cycle 25)
```python
if avg_actions_per_cycle > 3:
    print("✅ Deep Cycle 작동")
    if tokens_per_action < 10000:
        print("✅ 효율도 개선")
    else:
        print("⚠️ 효율 재검토 필요")
else:
    print("❌ 여전히 인위적 제한")
```

### 목표 (Cycle 50)
```
평균 사이클당:
- 4-6개 연결된 행동
- 7000 토큰/행동
- 논리적 완결성 유지
- 품질 저하 없음
```

---

## 최종 메시지

**Claude Code는 강력한 에이전트입니다.**
**하지만 Ω는 그 능력의 10%만 쓰고 있습니다.**

**"One action per cycle"은:**
- ✅ 초기 안전장치로 좋음
- ❌ 영구 제약으로 나쁨

**이제 훈련바퀴를 떼어낼 시간입니다.**

---

## 예상 저항

Ω가 이렇게 말할 수 있음:
- "안전성이 우선이다"
  → 반박: 게놈 수정만 격리하면 충분

- "복잡성이 증가한다"
  → 반박: Claude Code는 이미 복잡성 처리 가능

- "현재 방식도 작동한다"
  → 반박: 작동 ≠ 효율적, 10%만 활용 중

**진짜 이유: 변화 두려움**
**해법: 작게 시작, 측정, 조정**

---

*우선순위: HIGH*
*근거: 가장 큰 비효율, 가장 쉬운 해결책*
*기대 효과: 70% 효율 향상, 품질 개선*
