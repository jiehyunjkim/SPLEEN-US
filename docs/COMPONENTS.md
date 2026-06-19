# Component Review

## Summary table

| Team | Component | Recommendation | Main role |
|---|---|---|---|
| Team 2 | SAM / MedSAM models | Adopt | Primary automatic segmentation baseline |
| Team 5 | Dataset tools | Adopt as standard | Shared data layer |
| Team 4 | Proofreading WebApp | Adopt | Human correction and QC |
| Team 1 | UNet family | Conditional | Benchmarking and fallback models |
| Team 3 | Synthetic ultrasound | Experimental | Augmentation and domain-shift research |

---

## Team 2 — SAM / MedSAM models

### What I can confirm

- Provides a unified prediction interface for SAM / MedSAM-style models.
- Reported results suggest that the fine-tuned MedSAM model is a strong candidate baseline.


### What I recommend

Use Team 2 as the first automatic segmentation baseline.

The model output should be treated as a rough mask for proofreading rather than final ground truth. This is especially important at the beginning, because the model is trained on data outside the SPLEEN-US collection.

### What to check first

- Re-score the model on the same dataset used for all other models.
- Document the prompt or bounding-box strategy, because it affects reproducibility.

---

## Team 5 — Dataset tools

### What I can confirm

- The dataset plan uses `npz` files and a common loading/combining API.
- Define shared image, mask, metadata, and split conventions.

### What I recommend

Adopt Team 5 as the shared data standard.

The data layer should be defined before model comparison. Otherwise, each team may evaluate on a different split, with different preprocessing and different mask conventions.

### What to check first

- Define shape and dtype for image and mask.
- Add metadata fields for data source, label status, reviewer status, and model version.
- Keep public, synthetic, and SPLEEN-US pilot data separate in metadata.

---

## Team 4 — Proofreading WebApp

### What I can confirm

- Runs in the browser.
- Supports mask painting and erasing.
- Exports masks as NRRD.
- Supports the key human correction step in the SPLEEN-US loop.

### What I recommend

Adopt Team 4 as the proofreading and QC interface.

This component is important because it turns model outputs into corrected labels that can later be used for retraining. It also creates a natural place to record who reviewed a mask and what kind of review it received.

### What to check first

- Add data history fields where possible: model version, reviewer, review time, and label status.

---

## Team 1 — UNet family

### What I can confirm

- Test multiple UNet-style models which is useful for benchmarking.
- Documentation I reviewed appears to reference a cardiac ultrasound use case, while the project slides show spleen-related results.

### What I recommend

Use Team 1 as a benchmarking framework, not as the primary SPLEEN-US segmentation model until the spleen-specific setup is confirmed. A UNet-style baseline is still valuable for comparison, sanity checks, and ablation.

### What to check first

- Confirm which dataset, weights, and configuration correspond to spleen ultrasound.
- Re-run the model on the same held-out test set as Team 2.
- Use the same Dice/IoU implementation for all models.

---

## Team 3 — Synthetic ultrasound

### What I can confirm

- Includes several synthetic image generation approaches, including CycleGAN, DDPM, and Stable Diffusion / LoRA-style generation.

### What I recommend

Keep Team 3 as an experimental module. Synthetic data should not replace real SPLEEN-US data. Its value should be tested in a specific way: whether adding synthetic data improves performance on real data.

### What to check first

- Identify which real-data gaps synthetic data is meant to address.
- Compare training with and without synthetic augmentation.

---

## Shared issue: model scores are not yet comparable

The reported Dice scores across teams are useful as early evidence, but they should not be used to choose the final model yet. The scores come from different data splits, model setups, and possibly different metric implementations.

The fix is simple:

1. Use one held-out test set.
2. Use one Dice/IoU implementation.
3. Use same preprocessing and prompt settings.
4. Save predictions for review.

