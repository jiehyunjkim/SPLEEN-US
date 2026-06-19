# Architecture

This document proposes a small set of shared conventions for connecting the student components.

The goal is not to rewrite the existing repositories. The goal is to define a common interface so each repository can be wrapped and compared in the same workflow.


## 1. Shared data format

Use `npz` as the shared dataset format.

If a model needs a different format, the conversion should happen inside an adapter rather than being repeated by hand. The source dataset should remain unchanged. The integration layer only creates standardized views of the data.

## 2. Shared mask exchange format

Use NRRD for masks that move between the model pipeline and the proofreading WebApp.

```text
model output
    ↓
export to NRRD
    ↓
proofread in WebApp
    ↓
export corrected NRRD
    ↓
load back into training pipeline
```

This creates the loop needed for model-assisted annotation.

## 3. Shared API namespace

Use one namespace for the integration layer:

```python
import inia as I
```

Suggested calls:

| Call | Purpose | Wraps |
|---|---|---|
| `I.data.load(...)` | Load standardized datasets | Team 5 |
| `I.segment.predict(...)` | Generate a mask | Team 2 initially |
| `I.segment.benchmark(...)` | Compare models on one split | Team 1 + Team 2 |
| `I.proofread.export(...)` | Export mask for WebApp review | Team 4 |
| `I.eval.score(...)` | Compute shared Dice/IoU | New integration utility |
| `I.eval.agreement(...)` | Measure inter-rater agreement | New integration utility |


## 4. Metadata fields

Each image/mask pair should include metadata fields such as:

```python
{
    "subject_id": "...",
    "acquisition_id": "...",
    "frame_id": 0,
    "data_source": "roboflow | synthetic | spleen_us_pilot",
    "label_status": "auto_predicted | student_corrected | multi_rater_consensus | expert_reviewed | released",
    "model_name": "...",
    "model_version": "...",
    "reviewer_id": "...",
    "review_status": "none | reviewed | expert_reviewed"
}
```

The exact fields can change later, but the dataset should track provenance from the beginning.

