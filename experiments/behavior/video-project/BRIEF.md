# Controlled behavioral-diversity fixtures

Purpose: paired, deterministic synthetic media for a viewer-policy benchmark.
Automation/no stops is inherited from the owner's instruction to execute the benchmark.
Every stimulus is 8 seconds, muted, 720x1280 at 24fps, with a 0-3s hook and 3-8s follow-up.
Each pair changes exactly one declared configuration field. Identical style is intentional control, not a launch-film treatment.
Toy results are computed by `clean` and `deduplicate` in the source generator. These fixtures are not real-product proof footage.
No external media, identities, user uploads, music, narration or generated assets are needed.
Development and heldout rows are frozen before inference; expected behavior never appears in the pixels or runtime viewer payload.
