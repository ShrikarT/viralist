# Persona behavior benchmark: rationale and preregistration

Task V01-DIV follows the owner's instruction to test meaningful persona differences before replacing the repeated-profile cast. The canonical executable protocol is [PROTOCOL.md](../../experiments/behavior/PROTOCOL.md), with a separate analysis-only plan and frozen inference-safe inputs. This is a local experiment, not a human calibration or production validation claim.

## Primary-source basis

[PersonaLLM (NAACL Findings 2024)](https://arxiv.org/abs/2305.02547) investigates whether prompted traits appear in questionnaires and generated writing. Its setting supports measuring expressed traits; it does not establish that a collection of prompt descriptions reproduces independent real audience judgments.

[How Well Do Large Language Models Capture Human Personality? (2026 preprint)](https://arxiv.org/abs/2606.18263) reports that adding rich persona detail can reduce behavioral separation in its studied settings. This motivates measuring responses rather than counting unique attribute rows. It is not evidence about this specific Spark setup.

[Eval4Sim (CIKM 2026)](https://arxiv.org/abs/2603.02876) separates adherence, consistency and naturalness and uses human corpora as reference baselines. The present experiment has no such corpus, so it claims only synthetic, within-model behavioral differentiation and explicitly withholds human-fidelity scores.

## Design choices and evidence limits

Six fictional decision hypotheses cover attention/clarity, proof, disclosure/privacy, friction, recovery and exploratory interaction. A generic baseline and its identical-card alias help expose response noise or ID effects. The model sees only its own fixed policy, current real frame, verbatim rendered content and prior impression. Expected contrasts, split labels and other policies are absent.

Fourteen counterfactual pairs cover seven factors in a development text-cleanup task and an unseen row-deduplication task. Each pair changes one field in the generator configuration. Style, duration, sound and canvas are constant; proof data are computed from deterministic toy operations. Universal controls permit agreement. These deliberately simple static-card videos isolate content/pacing cues; they do not cover natural actor delivery, complex motion, music, real product authenticity or human behavior.

The protocol is frozen before inference. Primary checks compare repeated edit sensitivity with a preregistered reference policy; generic quality improvements cannot by themselves pass as persona diversity. Stable decision signatures use watch-through, ordinal interest and willingness to try, not expressive wording. The final distinct prototype subset must also separate pairwise beyond observed identical-card noise, including heldout clips. Missing data remains missing; agreement and negative findings are allowed.

No automatic policy tuning uses heldout results. Unproven profiles are demoted or provisionally grouped only within the observed benchmark; absence of detected difference is not proof of universal equivalence. Even six differentiated prototypes would not establish fifty distinguishable behaviors.

Orca was unavailable (`orca` not recognized); no research worker or independent reviewer ran. Primary-source review and subsequent checks are author-level evidence. All provider calls retain the original cumulative $10 owner limit, prior usage and the existing unknown-charge reserve.
