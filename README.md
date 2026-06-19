# SPLEEN-US Integration Review

This repository reviews the IMPACT student components for the SPLEEN-US project and proposes a practical integration plan.

**GOAL** : Identify which parts of the existing work can be reused, what needs to be checked before reuse, and what shared conventions are needed to connect the pieces into one workflow.

## 1. Summary

The initial integration path is:

```text
Load dataset
    ↓
Automatic segmentation
    ↓
Proofreading / correction
    ↓
Validation and QC
    ↓
Retraining
```

The student projects already cover most of this path. The main missing part is a shared layer that makes the pieces comparable and reusable.

## 2. Decision table

| Component | Team | Pipeline stage | Recommendation | Notes |
|---|---|---|---|---|
| SAM / MedSAM API | Team 2 | Automatic segmentation | Adopt | Strong candidate for the first segmentation baseline. Needs evaluation on the same test set as other models. |
| Dataset loaders | Team 5 | Data layer | Adopt as standard | The shared data format should be defined before comparing models. |
| Proofreading WebApp | Team 4 | Proofreading / QC | Adopt | Directly supports the model → correction → retraining loop. |
| UNet family API | Team 1 | Benchmarking | Conditional | Useful as a baseline framework. Spleen-specific readiness should be confirmed first. |
| Synthetic ultrasound | Team 3 | Augmentation / domain shift | Experimental | Useful for robustness and gap-filling experiments, but should not replace real SPLEEN-US data. |

Full notes are in [`docs/COMPONENTS.md`](docs/COMPONENTS.md).

## 3. Proposed workflow

```text
   Team 5             Team 1 / Team 2                Team 4                 New integration layer
Data loading   →       Segmentation       →       Proofreading     →       Validation / retraining
   (npz)              (rough masks)             (corrected masks)            (QC + model update)
```

The workflow is described in [`docs/WORKFLOW.md`](docs/WORKFLOW.md).

## 4. Main open issues

The current components are useful, but several issues should be addressed before scaling.

- Use same metric scores to directly compare the results across teams.
- The first SPLEEN-US labels will likely be created through a bootstrap process using public-data models and proofreading.
- Corrected masks need label history information and validation status.
- Domain shift should be measured across public, synthetic, and newly collected SPLEEN-US data.
- Expert review should be used selectively, because expert time is limited.

The validation plan is in [`docs/VALIDATION.md`](docs/VALIDATION.md).

## 5. Repository map

| Path | Contents |
|---|---|
| [`README.md`](README.md) | Summary and main decisions |
| [`docs/COMPONENTS.md`](docs/COMPONENTS.md) | Review of each student component |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Proposed shared data, mask, and API conventions |
| [`docs/WORKFLOW.md`](docs/WORKFLOW.md) | How the components connect in the SPLEEN-US loop |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | Validation risks and proposed QC strategy |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Phase-based implementation plan |
| [`examples/`](examples/) | Proposed end-to-end flow |

## 6. Prototype API

Example target usage:

```python
import inia as I

train, test = I.data.load(["roboflow", "deepspv"], split=0.8)
mask = I.segment.predict(test.images[0], prompt="spleen")
I.proofread.export(mask, "case01.nrrd")
score = I.eval.score(mask, test.masks[0])
```

The evaluation utilities are implemented because they are simple and useful for checking the interface. The data, segmentation, and proofreading adapters remain prototypes until the original repositories are connected.

## 7. Suggested first step

Start with a small pilot integration rather than a full rewrite:

1. Define the shared image and mask format.
2. Load one small dataset through the shared data interface.
3. Run one segmentation model through the shared segmentation interface.
4. Export the mask for proofreading.
5. Import the corrected mask.
6. Score the result with one shared evaluation function.

This would make the integration concrete while keeping the original student repositories intact.
