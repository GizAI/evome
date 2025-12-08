---
priority: MEDIUM
created: 2025-12-08
topic: additional improvement suggestions
---

# 추가 개선 아이디어 모음

## 1. 병렬 실행 (Parallel Execution)
**현재**: 순차적 단일 스레드
**제안**: 독립적 작업 동시 실행

```python
# tools/parallel_executor.py
from concurrent.futures import ThreadPoolExecutor

tasks = [
    ('analyze_logs', analyze_mutations_log),
    ('test_tools', run_all_tool_tests),
    ('check_gaps', gap_analyzer.run)
]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(lambda t: t[1](), tasks)
```

**이점**:
- I/O 대기 시간 활용 (WebSearch 등)
- 3-4배 속도 향상 가능
- 토큰 비용 동일

**위험**:
- 동시 파일 쓰기 충돌 가능
- 복잡성 증가

---

## 2. 예측적 캐싱 (Predictive Caching)
**현재**: 매번 전체 파일 읽기
**제안**: 파일 해시 기반 변경 감지

```python
# tools/smart_cache.py
cache = {
    'CLAUDE.md': {
        'hash': 'abc123...',
        'content': '...',
        'last_read': cycle_15
    }
}

def read_cached(filepath):
    current_hash = hash_file(filepath)
    if cache[filepath]['hash'] == current_hash:
        return cache[filepath]['content']  # 변경 없음
    # 변경됨 → 새로 읽기
```

**이점**:
- state.yaml/CLAUDE.md 등 느리게 변하는 파일 스킵
- 토큰 20-30% 절감

---

## 3. 점진적 목표 (Incremental Goals)
**현재**: 큰 목표 → 긴 사이클
**제안**: 목표를 자동 분해

```yaml
# goals/agentic_tooling_vertical.yaml
milestones:
  - id: m1
    title: "Research phase"
    cycles_estimate: 3-5
    done: true
  - id: m2
    title: "Tool creation phase"
    cycles_estimate: 5-8
    done: false  # ← 현재 여기
  - id: m3
    title: "Testing & refinement"
    cycles_estimate: 2-3
    done: false
```

**이점**:
- 진행률 가시성
- 중간 성공 축하 (동기부여)
- 목표 달성 예측 가능

---

## 4. 비용 알림 (Cost Alerts)
**현재**: 무한 실행 → 예상치 못한 비용
**제안**: 예산 추적 및 알림

```yaml
# state.yaml
budget:
  max_tokens_per_day: 500000
  max_cost_per_day: 15.00  # USD
  current_usage:
    tokens_today: 245000
    estimated_cost: 7.35
  alert_threshold: 0.8  # 80% 도달 시 경고
```

**동작**:
- 80% 도달 → feedback/budget_warning.md 자동 생성
- 100% 도달 → evome.sh 자동 일시정지
- 매일 00:00 리셋

---

## 5. A/B 테스트 모드
**현재**: 한 번에 하나의 접근법
**제안**: 여러 전략 동시 실험

```yaml
# experiments/exp_001.yaml
hypothesis: "exploration_rate 0.4가 0.3보다 빠른 수렴"
variants:
  - name: control
    exploration_rate: 0.3
    cycles: 20
  - name: treatment
    exploration_rate: 0.4
    cycles: 20
metrics:
  - goals_completed
  - avg_outcome_score
  - tokens_used
```

**이점**:
- 데이터 기반 최적화
- 최적 하이퍼파라미터 발견

---

## 6. 커뮤니티 도구 공유
**현재**: 17개 도구가 로컬에만 존재
**제안**: GitHub repo 자동 동기화

```python
# tools/share_tool.py
def publish_tool(tool_name):
    """
    1. 도구 문서화 자동 생성
    2. 테스트 케이스 추출
    3. git commit + push to github.com/omega-tools/
    4. README.md 업데이트
    """
```

**이점**:
- 다른 Ω 인스턴스와 도구 공유
- 오픈소스 기여
- 외부 피드백 수집

---

## 우선순위 제안
1. **배치 실행** (003-batch-execution.md) - 즉시 효과
2. **예측적 캐싱** - 쉬운 구현, 높은 ROI
3. **비용 알림** - 위험 관리
4. **병렬 실행** - 복잡하지만 큰 효과
5. **점진적 목표** - 장기 품질 개선
6. **A/B 테스트** - 연구 목적
7. **커뮤니티 공유** - aspirational

각 항목은 별도 feedback 파일로 분리 가능.
