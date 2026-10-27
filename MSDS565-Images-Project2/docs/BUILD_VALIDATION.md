# Validation of this delivery

## Passed

- Eleven automated tests passed: actual deployment artifacts and class order; changed-probe rejection; raw RGB/padding geometry; invalid-upload handling; existing image/integrity tests; startup with the real metadata; upload/button/results wiring and rerun persistence.
- Real inference used TensorFlow 2.20.0 and Keras 3.15.0 with the three supplied probes and pretrained backbones. Two saved test cases (indices 0 and 6) reproduced Notebook 3's saved predicted labels for every model. Direct preprocessing predictions matched xai predictions within an absolute tolerance of 1e-5.
- A third, unrelated local dog image was processed through every real model. All nine model/image combinations produced finite probabilities and all 27 maps (raw saliency, SmoothGrad with 32 samples, Grad-CAM).
- The unrelated image was assigned ball-peen by MobileNetV2 (~59.77%), claw by ResNet50 (~76.26%) and sledgehammer by EfficientNetV2M (~73.99%). Those are known closed-set errors, not unknown-object detection. No dog image is included in the repository.
- Streamlit AppTest startup had no exceptions or displayed errors. The UI wiring test used a synthetic upload and fixture prediction results to verify all three rows and retained results; it does not substitute for the separate real-backend tests.
- An actual Streamlit server started and its local health endpoint returned `ok`.
- Source syntax, notebook JSON/nbformat structure, model hashes, preprocessing hash, class mapping and original instructor-helper hashes passed. No trained probe or instructor helper was modified.
- Notebook execution outputs were preserved during canonical renaming and removal of unexecuted scratch cells. The repository contains no standalone images, arrays, caches, checkpoint notebooks or files above GitHub's 100 MB limit.

Exact case probabilities and runtime details are in app_validation.json. CPU timings are specific to this test host and are not a guarantee of Windows performance.

## Limits

No browser screenshot or full visual browser walkthrough is claimed; UI checks used Streamlit's app-testing framework. No full end-to-end notebook rerun was performed. Source notebooks retain the user's recorded results, with unexecuted scratch code removed.

The actual Windows conda export was not provided; environment.yml is labeled reconstructed. Finish Notebook 4's human review exports, real meeting minutes and the live class demo. `python scripts/validate_project.py --submission` reports these outstanding requirements rather than treating them as passed. No GitHub remote was created and no public hosting was configured.
