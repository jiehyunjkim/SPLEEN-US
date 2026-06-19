# Validation Strategy

SPLEEN-US is both a segmentation and a dataset construction project. The long-term value of the dataset depends on whether the released masks are reliable and well documented.

A single Dice score is not enough to answer this. The project also needs to track where labels came from, how they were corrected, and which labels were reviewed by humans or experts.

## Main validation risks

| Risk | Problem | How to handle |
|---|---|---|
| Cold-start gap | The first model is trained on public data and may not generalize to SPLEEN-US scans. | Measure performance on a small SPLEEN-US pilot set before scaling. |
| No perfect ground truth | Spleen ultrasound boundaries may be ambiguous, even for experts. | Use inter-rater agreement and a small expert anchor set. |
| Automation bias | Annotators may accept model predictions without fully correcting errors. | Compare a small subset of blank-start vs model-start annotations. |
| Limited expert time | Experts cannot review every frame or subject. | Use QC signals to prioritize cases for expert review. |

## History of Label

Corrected masks should not all be treated as the same type of ground truth. Each mask should include a label status.

Suggested states:

```text
auto_predicted
student_corrected
multi_rater_consensus
expert_reviewed
```

This makes it possible to grow the dataset while documenting how much review each label received.

## Domain shift

The preliminary experiment showed that a model trained on one public dataset performed well on held-out samples from that dataset, but did not generalize to a different dataset. I would treat this as a domain shift warning rather than evidence that synthetic data is unusable.

Possible sources of domain shift include:

- Real vs synthetic ultrasound
- Acquisition device
- Operator technique
- Image preprocessing
- 2D images vs cine loops
- Subject characteristics (e.g., age, sex, ethnicity, BMI, etc.)

Synthetic data may still be useful for augmentation, robustness testing, or targeted gap filling. Its value should be tested by whether it improves performance on real data.


## Inter-rater agreement

For selected cases, more than one annotator should review the same image or cine segment. Agreement can be measured using:

- Dice
- IoU
- boundary distance
- mask area difference
- frame-to-frame consistency

High agreement suggests that the case is relatively clear. Low agreement suggests that the case is ambiguous or that annotation instructions need improvement.

## Expert anchor set

The expert anchor set does not need to cover the entire dataset. Its purpose is to estimate how close the annotation process is to expert review.

Possible use:

1. Select a small but diverse subset.
2. Have an expert review or create reference masks.
3. Compare student-corrected masks to the expert anchor.
4. Use the result to decide which cases need expert review later.

## Automation bias

If annotators begin from a model prediction, they may accept model errors. This matters because corrected model outputs may later become training labels.

A small controlled check could compare:

- blank-start annotation
- model-start proofreading

Useful measurements:

- final mask difference
- annotation/proofreading time
- agreement with expert anchor cases
- types of errors left uncorrected

This does not need to be done for every case. A small subset can estimate whether the workflow introduces bias.

## Final Expert review

Expert review should be used for cases where it is most needed.

Potential review signals:

- high model uncertainty
- low inter-rater agreement
- large frame-to-frame mask jumps
- implausible mask size or location
- large disagreement between model prediction and human correction


Cases flagged by multiple signals should receive higher priority for expert review.

## Connection to prior annotation work

I run a related validation step in my previous annotation-tool work(CTOOL user study): whether non-expert users could produce labels close to expert quality (similar IoU between two groups compared to ground truth) while reducing annotation time.

That experience is relevant here because SPLEEN-US also needs to evaluate both label quality and workflow efficiency. A similar structure could be adapted: compare annotators on a controlled subset, measure overlap with a reference label, and record annotation/proofreading time.

## Practical first validation pilot

A small initial pilot could include:

1. A small SPLEEN-US sample.
2. Initial model predictions from Team 2.
3. Proofreading using Team 4.
4. A subset reviewed by multiple annotators.
5. A small expert anchor set.
6. Shared Dice/IoU and agreement metrics.
7. A short report on domain shift and label reliability.

This would be enough to decide whether the workflow is ready to scale.
