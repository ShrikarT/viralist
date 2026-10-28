# Behavioral-diversity benchmark — 2026-10-28

**Result: one of six candidate policies met the preregistered cross-task criterion.** The privacy-constrained operator is retained as an experimental prototype. The other five remain unproven on this benchmark. This is evidence against immediately relabeling fifty attribute combinations as fifty distinct behaviors; it is not evidence that the other policies can never differ.

The owner authorized this experiment after asking for genuinely different judgments. All inference used frozen source `3fa326c4a20f9dbc23c77e4152a2a012cdc852db`, Spark 1.3 Standard, isolated viewer requests and the unchanged [protocol](../../experiments/behavior/PROTOCOL.md). [Candidate definitions](../../experiments/behavior/policies.json), [retained subset](../../experiments/behavior/retained-policies.json), [complete diagnostic matrix](persona-diversity-matrix.md), [all-policy comparison CSV](persona-diversity-matrix.csv), and [research rationale](persona-diversity-method.md) are separate artifacts. The original fifty-instance baseline was not replaced.

## Observed results

| Factor / target policy | Development differential interest | Heldout differential interest | Reproduced in both |
|---|---|---|---|
| Proof / evidence-demanding expert | 0, 0 | 0, 0, 0 | No |
| Plain language / time-limited beginner | 0, 0 | 1, 0, 0 | No |
| Early payoff / time-limited beginner | 0, 0 | 1, 1, 0 | No |
| Device processing / privacy-constrained operator | 1, 1 | 2, 2, 2 | **Yes** |
| Fewer actions / convenience-focused operator | 2, -1 | 0, 0, 1 | No |
| Undo / recovery-focused maintainer | 1, 0 | 1, 1, 1 | No |
| Voice interaction / exploratory maker | 0, 0 | 0, 1, 0 | No |

These ordinal vectors are the target's edit response minus its prespecified reference policy's response, not significance tests. Development requires two positive repeats; heldout requires at least two of three, on the same factor. No policies or thresholds were tuned after seeing heldout outputs.

Privacy provides the clearest concrete example: all three heldout repetitions changed from low interest for hosted processing to high interest for device processing. The convenience reference remained high for both. One hosted reaction was “Hosted service means sensitive material leaves device, so I stop.” Its paired device reaction was “On-device processing resolves data-handling worry, workflow looks controllable.” The frames explicitly show the processing location. Recovery shows a weaker counterexample: it passed heldout but one development repeat had the same improvement as its reference; it therefore did not earn retained status.

Different explanations often accompanied the same decision. Final interest was medium in 417/608 trials, high in 72 and low in 119. Of 608 viewer trials, 598 reached the final segment; these very short card clips do not establish useful natural-video attention discrimination. Some expert reasons failed to retain earlier proof in their compressed impression. Treat these as observed limitations, not prompt-tuning targets retrospectively declared successful.

The identical-card baseline and its alternate ID disagreed on stable signatures for **4/30 clips**, demonstrating nonzero model/ID noise. The frozen descriptive separation floor became six clips. Privacy and its convenience reference differed stably on nine clips across both task phases. Only one candidate passed its own replicated anchor, so there is no claim of a multi-policy fully separated cast. The uninformative control allowed consensus: all 24 viewer trials returned low interest. Agreement was never penalized.

## Execution and checks

| Phase | Cohorts | Viewer trials | Scene decisions | Phase estimate | Wall time |
|---|---:|---:|---:|---:|---:|
| Development | 28 | 224 | 444 | $1.72367040 | 117.922s |
| Heldout | 42 | 336 | 670 | $2.48212220 | 164.922s |
| Controls | 6 | 48 | 92 | $0.32651365 | 22.500s |
| Total | 76 | 608 | 1,206 | **$4.53230625** | Separate phases, not a product latency measurement |

No failed cohorts/personas, duplicate accepted decisions, post-skip requests, peer/future input leaks or unreconciled charged decisions were found in the actual saved request audits. Inputs were real current frames plus deterministic card text, without audio. No provider file uploads were used. Inline inference input is not a claim of upstream retention erasure.

The chained cumulative estimate, including all prior experiments, is **$7.72663950**. The earlier unknown-charge reserve remains **$1.31327000**, for a tracked maximum of **$9.03990950** under the original $10 ceiling. Active reservations are zero. Billing-dashboard settlement remains uninspected. No charged retries were made. All three processes are terminal, owned preview stopped, credential memory cleared and persisted-key scan passed.

Author verification exercised the actual scene scheduler and saved artifacts. The artifact verifier reconciles every paid decision, exact own-card/prior-impression prompt, frame/features, skip boundary, frozen design and prior-ledger hash. Injected peer/future text and a reset prior-cost field were both rejected. All 25 offline regressions passed; compilation and diff checks passed. Final revision-specific check receipts remain private.

The first post-commit regression run exposed a timing-dependent test: a 10ms sleep did not reliably create overlap, yielding one observed active request instead of two. The external stub now uses a two-party barrier, directly requiring overlapping reservations. The failing receipt is preserved privately; the corrected offline check makes no paid requests and does not change the inference source or results.

## Limits and next use

- Thirty fixed, eight-second toy-operation videos isolate seven factors across two tasks. They do not validate human fidelity, natural motion/audio, original-video generalization, virality, statistical independence or fifty distinct behaviors.
- A private metadata edit misdecoded the constant disclosure separator, adding U+00C2 in all 60 scene observation lists. The discrepancy was discovered after development and recorded before heldout. All task-bearing text and rendered frames match the frozen design. The exact same inputs were retained in all phases; no paid evidence was rewritten. Future regeneration uses explicit UTF-8 and would be a new input artifact.
- Orca and independent verification were unavailable. Acceptance is **WORKER-REPORTED**. REVIEW-ACCEPTED is pending; product integration, journey verification and release remain inapplicable/pending because the application is unbuilt and nothing was published.
- Keep the supported privacy policy as one prototype. Keep the other five as explicit hypotheses, with their failed/partial comparisons visible. Broader fixtures or revised policies require a new frozen experiment. Any further paid experiment needs room in the same ledger or a newly authorized ceiling; do not erase the unknown reserve.

Private evidence root: `C:/Users/Shrikar/.codex/private-runs/viralist-behavior-20261028`. Each phase contains `verified.json`, exact dispatch audits, reactions and chained ledgers; `results/` contains the complete analysis and diagnostic matrix. The repository includes only derived synthetic-fixture comparisons and definitions, with no supplied customer videos, credentials or raw provider payloads.
