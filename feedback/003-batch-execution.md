---
priority: HIGH
created: 2025-12-08
topic: batch execution efficiency
---

# Feedback: 배치 실행 모드 구현

## 문제
현재 한 사이클 = 한 행동은 안전하지만 비효율적:
- 간단한 작업도 여러 사이클 소요
- 토큰 중복 (매번 state 읽기, 분석 반복)
- 명확한 멀티스텝 작업에도 강제 분할

## 요구사항
**"배치 모드" 추가 - 조건부로 여러 행동 허용:**

### 허용 조건 (AND 조건):
1. 작업들이 명확히 독립적 (서로 의존성 없음)
2. 각 작업이 저위험 (state 파괴 가능성 낮음)
3. 전체 예상 토큰 < 3000 (여전히 효율 중시)
4. 롤백 가능 (mutations.log에 개별 기록)

### 예시:

**❌ 배치 불가 (순차 의존성)**
```
1. WebSearch로 라이브러리 조사
2. 조사 결과로 도구 생성  ← 1번 결과 필요
3. 도구 테스트             ← 2번 완료 필요
```

**✅ 배치 가능 (독립적 작업)**
```
1. mutations.log 마지막 10개 항목 분석
2. tools/ 디렉토리 모든 도구 테스트 실행
3. knowledge/ 디렉토리 중복 항목 체크
→ 3개 모두 독립적, 읽기 위주, 저위험
```

**✅ 배치 가능 (원자적 시리즈)**
```
목표: novelty_checker.py 튜닝
1. 임계값 0.3 → 0.5 수정
2. 테스트 실행
3. 결과 outcomes.log 기록
→ 하나의 논리적 작업, 쉬운 롤백
```

## 구현 제안

### state.yaml에 모드 추가:
```yaml
execution_mode: conservative  # conservative | batch | auto
batch_rules:
  max_actions: 3
  max_tokens: 3000
  require_rollback_plan: true
```

### CLAUDE.md 업데이트:
```markdown
## Execution Modes

1. **Conservative** (default): One action per cycle
2. **Batch**: Multiple independent actions if:
   - No cross-dependencies
   - Low risk (no genome mutation in batch)
   - Total tokens < 3000
   - Each action logged separately
3. **Auto**: Ω decides based on task analysis
```

## 기대 효과
- 단순 작업 3-5배 속도 향상
- 토큰 30-40% 절감 (중복 state 읽기 제거)
- 여전히 안전성 유지 (조건부 허용)

## 우선순위
HIGH - 현재 가장 큰 효율 병목

## 측정 지표
- 평균 사이클/목표 달성 비율
- 토큰/목표 달성 비용
- 에러율 변화 (안전성 검증)
