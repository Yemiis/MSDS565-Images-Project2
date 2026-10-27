# Saved deployment artifacts

The three supplied .keras files are trained single-Dense linear probes, not full pretrained backbones. They are under 100 KB each and are included directly in Git. The app rebuilds the exact frozen ImageNet applications and joins each to its probe.

label_to_index.json fixes the class order. preprocessing.json fixes the RGB/padding contract. training_metadata.json records the probe and preprocessing hashes and the original training framework versions. Do not edit hashes to accept a different model file.

P2_N3_comparison.csv and the classification/confusion/history tables preserve Notebook 3's recorded results. P2_N4_shortcut_ablation.csv preserves the border-sensitivity results. Final Notebook 4 visual-review and deployment-judgment exports were absent in the source upload and are not fabricated here.
