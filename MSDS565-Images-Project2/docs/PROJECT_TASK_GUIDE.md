# Pipeline task guide

| Stage | Task and decision | Output to inspect |
|---|---|---|
| Notebook 1 | I declare related hammer classes, predict claw/ball-peen confusion and scrape with multiple exact queries. | Manifest URLs, labels, queries, readability and acquisition accounting |
| Notebook 2 | I clean subjects and duplicates manually, measure the retained dataset, preserve shape with RGB padding and split before balancing/augmentation. | Removed/retained counts, eight images/class, dimensions, mean images, class counts, external raw arrays and mapping |
| Notebook 3 | I compare frozen small/medium/large backbones using the same simple probe settings. | Accuracy/F1, class recall, confusion matrices, parameter/time comparison and saved probes |
| Notebook 4 | I compare actual correct/error maps and quantify sensitivity to border occlusion. | Three map types, same-image comparison, ablation table; finish the external case-review and deployment files |
| Streamlit | I reuse exact geometry and trained artifacts, classify an upload with every model and explain its predictions. | One row/model, sorted probabilities, raw saliency, SmoothGrad 32 and Grad-CAM |
| Submission | I export the real environment, run the live demo, maintain real minutes and submit individual peer feedback privately. | README, actual environment export, executed notebooks and authentic human records |

For app operation, follow RUN_STREAMLIT_WINDOWS.md. For exact remaining submission gaps, follow SUBMISSION_STATUS.md.

Notebook 4's external P2_xai_review.csv needs actual observations for raw_vs_smoothgrad, gradcam_region, shortcut_evidence, mean_image_link, methods_agree and interpretation. Link mean_image_link to an observation from Notebook 2, not a guessed URL. P2_deployment_judgment.json needs the six actual deployment-review answers. Blank templates are not completed evidence.
