---
priority: MEDIUM
created: 2025-12-08
topic: code quality and cleanliness
---

# Feedback: 간결함 유지 - 중복과 지저분함 경계

## 문제 징후

### 이미 나타나는 패턴:
- 📁 feedback/에 003이 두 곳 (directory + archive)
- 📝 IMPROVEMENTS.md + REALITY_CHECK.md (내용 중복?)
- 🔧 17 tools/ 중 실제 사용률?
- 📚 109 insights 중 몇 개가 실질적?

**경고**: 복잡성 증가 ≠ 진화

---

## 원칙

### 1. 파일 생성 전 질문
```
"이미 비슷한 파일 있나?" → 있으면 Edit
"정말 새 파일 필요한가?" → 아니면 기존 파일에 추가
"이 파일 1주 후에도 볼까?" → 아니면 만들지 마라
```

### 2. 주기적 정리
```python
# Every 20 cycles
- Archive unused tools (moved to tools/archive/)
- Merge duplicate insights
- Delete redundant docs
- Clean __pycache__, .pyc files
```

### 3. 품질 > 양
```
❌ 17 tools (5개만 사용)
✅ 10 tools (10개 모두 사용)

❌ 109 insights (반복 내용)
✅ 30 insights (핵심만)

❌ 3개 문서 (같은 내용)
✅ 1개 문서 (명확함)
```

---

## 즉시 정리 대상

```bash
# 중복 제거
rm feedback/003-batch-execution.md  # archive에 있음

# 캐시 정리
rm -rf tools/__pycache__

# 사용 안하는 goals
rm goals/goal_*.yaml  # 자동 생성 테스트용

# 로그 순환
if [ $(wc -l < loop.log) -gt 10000 ]; then
  tail -5000 loop.log > loop.log.tmp
  mv loop.log.tmp loop.log
fi
```

---

## 지속 가능성 규칙

### STOP 규칙:
- STOP creating knowledge/*.md for every small insight
- STOP making new tools without deleting old ones
- STOP documenting everything in multiple places
- STOP adding to insights list without reviewing old ones

### DO 규칙:
- DO consolidate similar tools
- DO delete obsolete code
- DO merge redundant docs
- DO measure tool usage before adding new

---

## 측정

```yaml
# state.yaml 추가
cleanliness_metrics:
  tools_used_rate: 10/17 (59%)  # 40% 미사용
  insights_unique_rate: 30/109 (28%)  # 72% 중복

  target:
    tools_used_rate: > 80%
    insights_unique_rate: > 70%
```

---

*Keep it lean. Quality over quantity.*
