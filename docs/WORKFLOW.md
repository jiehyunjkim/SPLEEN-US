# Workflow

This document maps the SPLEEN-US workflow to the student components.

## Full loop

```text
1. Data loading
        ↓
2. Automatic segmentation
        ↓
3. Proofreading / correction
        ↓
4. Quality Control for scaling
        ↓
5. Retraining
        ↓
repeat with improved model
```

## Component mapping

| Step | What happens | Component |
|---|---|---|
| Data loading | Load public, synthetic, and SPLEEN-US data in one format | Team 5 |
| Segmentation | Generate rough spleen masks | Team 2 primary, Team 1 benchmark |
| Proofreading | Correct model-generated masks | Team 4 |
| Validation | Check label quality and route difficult cases | New integration layer |
| Retraining | Use corrected/validated labels to improve the model | Team 1 / Team 2 + new glue code |

## Cold-start problem

SPLEEN-US begins without its own validated masks. The first model will likely be trained or fine-tuned on public data, then applied to new SPLEEN-US scans.

A practical loop is:

1. Train or select an initial model using public data.
2. Run that model on new SPLEEN-US scans.
3. Treat the output as a rough mask, not ground truth.
4. Proofread and correct the mask.
5. Save the corrected mask with history of label.
6. Use validated corrected masks for retraining.

The first reliable labels are created through proofreading and validation.

## Main risks in the loop

Two issues should be handled early.

### 1. Weak first model

If the first model does not find the spleen reliably on SPLEEN-US data, annotators will need to draw from scratch. That would reduce the value of model-assisted proofreading.

Early check:

- Run the public-data model on a small SPLEEN-US pilot set.
- Measure how often the model creates a usable rough mask.
- Break performance down by source and subgroup when metadata is available.

### 2. Over-trusting the model

If annotators start from a model prediction, they may accept incorrect boundaries. Those errors could then become part of the training set.

Early check:

- Use a small subset to compare blank-start annotation with model-start proofreading.
- Measure time and mask difference.
- Use the result to decide how much human review is needed.

## Minimal end-to-end pilot

A small pilot should answer whether the pieces connect.

```text
Load one dataset through Team 5
        ↓
Generate a mask with Team 2
        ↓
Export mask to Team 4 WebApp format
        ↓
Proofread and export corrected mask
        ↓
Load corrected mask back
        ↓
Score with shared Dice/IoU
```

This pilot does not need to solve the full project. It only needs to prove that the integration path is possible.
