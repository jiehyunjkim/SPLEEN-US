"""
Proposed SPLEEN-US end-to-end integration flow.
This script is a design sketch. The purpose is to show the target flow in one place.
"""

import inia as I


def main():
    # 1. Load standardized data. Target wrapper: Team 5.
    train, test = I.data.load(["roboflow", "deepspv"], split=0.8)

    # 2. Generate an initial rough mask. Target wrapper: Team 2.
    prediction = I.segment.predict(test.images[0], prompt="spleen", model="team2_medsam")

    # 3. Export the rough mask for proofreading. Target wrapper: Team 4.
    I.proofread.export(prediction.mask, "outputs/case01_for_review.nrrd")

    # 4. Load the corrected mask after proofreading.
    checked_mask = I.proofread.load_checked("outputs/case01_checked.nrrd")

    # 5. Score through one shared implementation.
    result = I.eval.score(prediction.mask, checked_mask, uncertainty=prediction.uncertainty)
    print(result)

    # 6. Corrected masks can then be added back to the training set for retraining.


if __name__ == "__main__":
    main()
