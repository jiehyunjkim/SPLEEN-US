# Phase-Based Roadmap

The early timeline depends on clinician availability, data access, and project approvals, so this roadmap is organized by phase rather than fixed dates.

## Phase 0 — Clinician interviews and requirements

The project should begin by clarifying the clinical and workflow requirements.

Main tasks:

- Prepare a semi-structured interview guide.
- Interview clinicians and other potential users.
- Summarize what they need from the device, the segmentation output, and the proofreading workflow.
- Translate interview findings into data-collection and validation requirements.

Expected output:

- interview summary
- list of clinical needs
- data and metadata requirements
- initial validation requirements

## Phase 1 — Data and interface foundation

Main tasks:

- Define the shared image and mask format.
- Use a common dataset loader.
- Define history of label fields.
- Decide how public, synthetic, and SPLEEN-US pilot data will be separated.
- Implement one shared scoring function.

Expected output:

- shared image and mask 
- common evaluation function
- initial metadata schema

## Phase 2 — Component integration pilot

Main tasks:

- Wrap Team 2 segmentation behind a common interface.
- Keep Team 1 as a benchmark model family.
- Connect model outputs to the Team 4 proofreading workflow.
- Test mask export/import.
- Run all models on the same small set of data.

Expected output:

- minimal end-to-end path
- comparable baseline scores
- initial cold-start gap estimate
- list of integration issues

## Phase 3 — Validation pilot

Main tasks:

- Create a small expert-reviewed anchor set.
- Measure inter-rater agreement on selected cases.
- Add basic QC checks.
- Test whether model-start proofreading introduces bias.
- Define which cases should go to expert review.

Expected output:

- initial label validation protocol
- expert review criteria
- release criteria for corrected masks

## Phase 4 — Iterative improvement

Main tasks:

- Retrain models using corrected labels.
- Track model versions.
- Track label status.
- Evaluate performance across public, synthetic, and SPLEEN-US pilot data.
- Use synthetic data only for measured gaps.

Expected output:

- versioned dataset
- versioned model baseline
- validation report
- plan for scale-up

## Notes

The roadmap should be updated after the clinician interviews. Those interviews may change which measurements are most important, what metadata should be collected, and what level of annotation quality is needed.
