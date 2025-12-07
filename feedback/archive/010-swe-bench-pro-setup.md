---
priority: HIGH
created: 2025-12-08
topic: swe-bench pro installation guide
---

# SWE-Bench Pro Setup Instructions

## Official Repository
https://github.com/scaleapi/SWE-bench_Pro-os

## Installation (Next Cycle)

```bash
# 1. Clone the repo
git clone https://github.com/scaleapi/SWE-bench_Pro-os.git
cd SWE-bench_Pro-os

# 2. Install dependencies
pip install -e .

# 3. Download dataset
# Public dataset (731 instances)
python -m swebench_pro.download --split public

# Or use HuggingFace
from datasets import load_dataset
dataset = load_dataset("scaleapi/SWE-bench_Pro", split="public")
```

## Dataset Access

**HuggingFace**: https://huggingface.co/datasets/scaleapi/SWE-bench_Pro

Splits:
- `public`: 731 instances (accessible)
- `commercial`: 276 instances (may require license)
- `heldout`: 858 instances (private, for official eval)

## Evaluation

```python
from swebench_pro import evaluate

# Run single instance
result = evaluate(
    instance_id="repo__issue_id",
    prediction="<patch content>",
    timeout=300
)

# Returns: {"resolved": True/False, "logs": "..."}
```

## Integration with Current Solver

Update `tools/swe_solver.py`:

```python
# Change from:
# swebench (Lite)

# To:
# swebench_pro (Public)

from swebench_pro import load_dataset, evaluate

dataset = load_dataset("scaleapi/SWE-bench_Pro", split="public")
# 731 instances instead of 300
```

## Immediate Actions

1. **Switch dataset** (after Lite warmup)
2. **Update metrics tracking**:
```yaml
external_metrics.yaml:
  swe_bench_pro_public:
    dataset: "scaleapi/SWE-bench_Pro"
    split: "public"
    total: 731
    attempted: 0
    passed: 0
    target: 300 (41%)
```

3. **Test on 5 instances first**
4. **Scale up gradually**

---

*Official: https://github.com/scaleapi/SWE-bench_Pro-os*
*Dataset: https://huggingface.co/datasets/scaleapi/SWE-bench_Pro*
