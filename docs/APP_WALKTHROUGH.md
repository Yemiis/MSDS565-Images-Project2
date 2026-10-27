# App walkthrough for the progress report

| Part | What I did | Why |
|---|---|---|
| Artifact checks | I verify probe hashes, preprocessing metadata and the saved label order. | A mismatched model or label order can silently change predictions. |
| Upload | I decode the photograph in memory and display the original and resized version. | The user can see exactly what the app analyzes. |
| Geometry | I call the same shared RGB/padding function as Notebook 2. | Training and uploaded photos need identical geometry. |
| Model loading | I rebuild all three frozen ImageNet applications and join each to its saved probe. | This matches Notebook 3; I do not train or choose a single model in the app. |
| Cache | I cache the immutable models and retain results in the user's session. | I avoid reloading weights and rerunning expensive maps on every interaction. Uploads are not cached globally or written to files. |
| Prediction | I use xai.predict_proba on raw 0–255 RGB pixels. | The supplied helper applies model-specific scaling once. |
| Display | I give every model one row with sorted probabilities and three overlays. | The comparison stays visible without a model picker. |
| Explanation | I use raw saliency, 32-sample SmoothGrad and Grad-CAM from the unchanged instructor helper. | The assignment asks me to apply and explain these methods, not implement replacements. |
| Uncertainty | I show probabilities, entropy and agreement, while explaining the closed-set limitation. | High confidence or agreement does not verify class membership. |

Grad-CAM starts from 7×7 maps for these backbones. Upsampling does not create precise boundaries. Heatmaps are normalized separately, so I compare locations rather than color strength.

Task: classify a new photograph with all three models. Decision: reuse saved artifacts and exact preprocessing. Steps: upload, prepare, predict, explain, compare. Interpretation: compare the object regions with model confidence; treat unexpected confidence on unrelated images as a limitation, not successful recognition.
