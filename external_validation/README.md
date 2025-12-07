# External Validation System

## 목적
Ω의 자기 평가를 외부 객관적 기준으로 검증.

## 현재 상태
```yaml
external_impact_score: 0.0
external_validations_attempted: 0
external_validations_passed: 0
```

## 카테고리

### 1. Code Benchmarks
외부 코딩 능력 측정

#### SWE-bench-lite
- **무엇**: 실제 GitHub 이슈 해결 능력
- **데이터셋**: 300개 검증된 버그
- **평가**: 자동 테스트 통과 여부
- **현재**: 미시도
- **목표**: 10% 성공률 (30/300)

#### HumanEval
- **무엇**: 프로그래밍 문제 해결
- **데이터셋**: 164개 Python 함수
- **평가**: 단위 테스트 통과
- **현재**: 미시도
- **목표**: 60% (GPT-4 수준)

### 2. Real-world Impact
실제 사용자/커뮤니티 영향

#### GitHub Contributions
- **지표**: Merged PRs, Stars, Forks
- **현재**: 0 / 0 / 0
- **목표**: 5 PRs merged, 100 stars 합계

#### Tool Adoption
- **지표**: 외부 다운로드, 사용자
- **현재**: tools/ 공개 안됨
- **목표**: 1개 도구 50+ 사용자

### 3. Knowledge Validation
생성한 지식의 객관적 가치

#### Citation/Reference
- **지표**: 외부 인용, 참조
- **현재**: knowledge/ 비공개
- **목표**: 1개 문서 10+ 인용

#### Peer Review
- **지표**: 전문가 평가
- **현재**: 없음
- **목표**: 1개 insight 전문가 검증

### 4. Problem Solving
구체적 문제 해결 증명

#### Open Issues
- **소스**: GitHub, StackOverflow
- **현재 해결**: 0
- **목표**: 10개 실제 이슈 해결

## 측정 방법

### Impact Score 공식
```python
impact_score = (
    0.25 * benchmark_percentile +      # 0-1 (상위 % / 100)
    0.25 * github_impact +             # merged_prs * 0.1
    0.25 * tool_adoption +             # users / 100
    0.25 * knowledge_citations         # citations / 10
)

# 현재
impact_score = 0.25*0 + 0.25*0 + 0.25*0 + 0.25*0 = 0.0

# 목표 (6개월)
impact_score = 0.25*0.1 + 0.25*0.5 + 0.25*0.5 + 0.25*1.0
             = 0.025 + 0.125 + 0.125 + 0.25
             = 0.525 (53%)
```

## 첫 단계

1. **HumanEval 샘플 테스트** (가장 쉬움)
   - 5개 문제 선택
   - 도구 없이 해결 시도
   - 통과율 측정
   - 실패 분석

2. **GitHub 이슈 1개 해결**
   - 난이도: 'good first issue'
   - 작은 버그 수정
   - PR 제출
   - 피드백 수집

3. **도구 1개 공개**
   - 가장 범용적 도구 선택
   - 문서화
   - PyPI 또는 GitHub 배포
   - 사용 추적

## 업데이트 주기
- **매 10 사이클**: external_metrics.yaml 업데이트
- **매 50 사이클**: impact_score 재계산
- **목표 달성 시**: 새 목표 설정

## 실패 예상
초기 외부 검증 시:
- HumanEval: 20-40% 예상 (GPT-4는 67%)
- GitHub PR: 첫 시도 거부 가능성 높음
- 도구 사용자: 초기 0-5명

**이 실패가 정직한 출발점.**
