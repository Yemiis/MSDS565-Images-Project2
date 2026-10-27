# Live class demonstration

Run the app locally using RUN_STREAMLIT_WINDOWS.md. Before class, complete one comparison so the pretrained weights are already cached.

1. Upload a real, ordinary hammer photograph. Show all three rows, the sorted three-class probabilities and every explanation overlay.
2. Upload a deliberately hard photo (for example, a cropped or oblique hammer head). Describe disagreements and whether maps emphasize the tool, background or text. Do not assume the best notebook accuracy guarantees the best prediction for this image.
3. Upload an unrelated object. Explain that softmax must distribute probability across the three hammer labels and may be very confident anyway. Entropy is descriptive, not a validated rejection rule.
4. Explain how the same 224×224 RGB grey-padding geometry is shared with Notebook 2, and why the app does not call preprocess_input before xai.
5. State what is needed for honest rejection: separate out-of-class data, a held-out validation protocol and a calibrated abstention rule. No such detector is claimed here.

Record actual completion in `docs/LIVE_DEMO_COMPLETED.md` after the live demonstration. Include the real date and a short account of the three cases. No completion record is prefilled.
