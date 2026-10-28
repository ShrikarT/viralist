# Spark 1.3 corrections and staged live rerun — 2026-10-28

**WORKER-REPORTED: requested experiment fixes and both live stages completed.** Independent review is pending. No product app, deployment or release is claimed.

The owner explicitly requested fixing the observed issues and rerunning both small casts, then 50 personas, using Spark 1.3. All spend carries forward from the original experiment under the same $10 ceiling. Source briefs remain reference evidence; this authority came from the direct request.

## Final frozen source and observed results

Provider execution revision: `04b852728ae22967f408f71e34f274911ab07578`, branch `codex/meta-api-smoke`. Both final stages used this same committed configuration. Later documentation/dependency and legacy-CLI retirement changes did not rerun the provider or relabel the source revision.

| Check | Observed evidence |
|---|---|
| Stage 1 | Both supplied videos, three independently requested personas each; 12 and 7 accepted scene reactions; zero failed personas. Simulation times 23.422s and 13.657s, excluding separately measured preparation. |
| Stage 2 | All 50 requested cast IDs produced valid results: 256 accepted scene reactions; zero failed personas; no automatic inference retries. |
| Final latency | Simulation 37.984s. Provider preparation 10.516s; native scene extraction 29.047s. Complete report 85.000s from experiment start, including catalog, uploads, fresh ASR, native extraction, simulation and notes. Local decode/frame preparation adds 3.192025s: **88.192025s total**. |
| Cleanup latency | Complete process including provider deletion checks: 96.125s, excluding initial local preparation. Deletion is measured separately from time to report. |
| Model routing | `muse-spark-1.3` Standard for native visual interpretation, scene observations, individual reactions and notes; `muse-voice-transcribe-1.0` for speech; `muse-image-1.0` for four generated backgrounds. |
| Isolation | Actual frame/clip/ASR/feature hashes matched current segments; no peer-card context, future transcript/observations or post-skip requests; unique accepted persona/scene verdicts. |
| Audio | Both original non-silent tracks retain correct audio-presence state; separate ASR recovers narration/vocals. Silence and synthetic tone controls produce empty transcripts without claiming absent media. |
| Semantic output | Working product demonstration on A; B remains animated branding with null first-product timestamp and empty product evidence. Notes use exact stored quotes, valid source ranges and actual footage/capture instructions. |
| Thumbnails | Four Muse-generated backgrounds from approved source frames, with separately rendered exact headlines. All four source/output/mobile previews inspected; no visible identity-document details or clipped headlines. |
| Budget | Final 50-person stage estimated **$0.94328385**. Entire investigation, including the earlier run and all diagnostic attempts, estimated **$3.19433325** from reported usage/rates. One earlier HTTP 500 retains **$1.31327** worst-case charge reserve. Tracked total including that reserve: **$4.50760325**, below $10. Actual billing dashboard not inspected. |

Private final artifacts: `C:/Users/Shrikar/.codex/private-runs/viralist-spark13-20261028/stage1-bounded` and `stage2-bounded`. The final `verification.json` files and full chained ledgers are there. Safe thumbnail files remain in `stage1-final`; later stages verify/reuse their exact hashes instead of charging for the same images again. Originals, transcripts, raw responses, rejected images and supplied credentials are excluded from Git.

## What changed

- Extract audio once locally, slice it at known segment boundaries, and transcribe through the dedicated endpoint. Full-video ASR stays with global analysis; personas receive only their current segment's transcript. ASR remains a machine hypothesis: some words/names can be wrong, and vocals are not proof of product narration.
- Interpret each native visual-only segment once. Reuse its source-bound observations and a real current frame in independent persona calls. These observations are lossy, so key-cue review compared them with the original clips/contact sheets: oversized-file rejection, compressed 1.52 MB result, accepted upload, CTA and B's undemonstrated claims remain visible. This is not a claim that frame/observation input is equivalent to watching native video.
- Give each persona its own chronological task and bounded prior impression. A skip ends that task. Concurrency is bounded at 32 independent HTTP tasks; shared media preparation and token counts contain no persona cards or histories.
- Use persistent per-thread HTTP sessions. Warm each image's context count during preparation and share only that immutable media/schema count. Each distinct persona text retains its own request. For image/text requests, reserve a conservative rendered-media context plus UTF-8 text bound, 4096-token margin and capped output; actual usage was checked against the bound. Native video counting proved unreliable, so those calls reserve the entire documented context.
- Select result/artwork frames before image generation and fail closed on private-document screening. Generate backgrounds without text, contain them within margins, render the headline with Pillow, then inspect the mobile preview. Generated illustrations are not product-proof footage.
- Reject contradictory product timestamps, unsupported quotes/time ranges, malformed/truncated responses and fabricated proof suggestions. Bind feature timing to the known clip interval; model-guessed point times stay private/unverified. Rounded end-of-clip timestamps no longer create false failures or pretend to provide precise event timing.
- Retire the legacy paid CLI paths so the older batch/audio/thumbnail behavior is not the default entry point. Preserve historical source commits for inspection.

## Failures preserved and bounded recovery

The diagnostic history is intentionally retained. A native video's input-count result was 616 tokens while returned usage reported 8821; the run stopped and changed to conservative native reservations. A note validator initially rejected a prohibition of mock UI; an observed regression test now accepts the prohibition while rejecting a request to fabricate UI. One 600-token response truncated, so the cap increased to 1200 with incomplete responses still rejected. One terminal HTTP 500 was explicitly repaired only for the failed persona, keeping the original failed request and worst-case reserve. No ambiguous request was silently treated as free.

The first complete Spark 1.3 50-person report passed correctness but took 113.859s. Concurrency and media-count preparation were then improved. A later preparation-only attempt rejected an observation rounded to the clip endpoint before any persona inference ran; a regression now binds descriptions to authoritative source intervals. The final same-revision small/scale sequence passed. A rejected/partial attempt is not counted as a successful run.

## Verification and limits

Free checks from the repository root:

```powershell
python -m unittest discover -s experiments -p test_pipeline.py -v
python experiments/verify_pipeline.py --out C:\Users\Shrikar\.codex\private-runs\viralist-spark13-20261028\stage1-bounded
python experiments/verify_pipeline.py --out C:\Users\Shrikar\.codex\private-runs\viralist-spark13-20261028\stage2-bounded
git diff --check
```

Fifteen scheduler/budget/semantic/layout regressions passed before provider execution; all **16** final handoff regressions passed, including both retired paid entry points stopping before requesting a key or creating output. External models are stubbed only in offline regressions; the two final provider stages used the actual API. Author artifact verification inspects real dispatches, source bytes, response usage, quote references, cleanup and cost lineage. The completion audit reconciled **12 ledgers**, checked **41 local Markdown links**, and passed credential scanning of tracked source plus private JSON/logs. All **157 unique uploaded provider files** across attempts were deleted and subsequently returned 404; this does not claim erasure of upstream backups. The key variable was cleared after the final process exited.

The 88.2s result is one successful local run on a 33.78s video, not p95, a 60s worst-case guarantee, browser verification or deployed performance. Earlier slow requests show provider variance. Five repeated, uncalibrated archetypes remain a thin library; no real audience prediction, paired A/B lift or thumbnail vote winner was established. Independent requests improve isolation but cost more than the original five-person batching: the final ~$0.94 run exceeds the earlier proposed $0.50/run product target, which remains unresolved. Full production journeys and that business/latency contract require separate work.

Primary references: [model catalog](https://dev.meta.ai/docs/models), [Spark audio caveat](https://dev.meta.ai/docs/video-understanding), [dedicated transcription](https://dev.meta.ai/docs/speech-to-text), [token-count limits](https://dev.meta.ai/docs/token-counting), [image request controls](https://dev.meta.ai/docs/image-generation), [rates](https://dev.meta.ai/docs/pricing-rate-limits). The dated private receipts establish the actual behavior measured here.
