# Live provider experiment — 2026-10-28

State: **WORKER-REPORTED**. Real Meta API calls from the local experimental harness; no production application, independent reviewer, deployment or publication. Owner explicitly supplied two videos and credentials and authorized testing within a $10 limit. API spend estimate: **$0.50390605**; uncertain reserve $0; actual billing dashboard not inspected. No additional charge is needed to inspect saved evidence.

Main run: `27cff193a646646966a41f8de15d07ea97e790f4`. Corrected image/audio follow-up and artifact verifier: `3ddd86999cdb400ae3c39f98e2fe26d7ec59c368`. Later summary-field correction is not presented as a new live run. Branch: `codex/meta-api-smoke`; owner-selected remote remains unpushed.

Private evidence: `C:/Users/Shrikar/.codex/private-runs/viralist-20261028`. Contains original-input hashes, prepared clips, prompt/dispatch audits, raw provider results, usage ledger, generated images and local reports. Media, private transcripts, credentials and raw payloads are excluded from Git. The key was passed through private child-process stdin, never command arguments.

## Observed checks

| Check | Observation | Limit |
|---|---|---|
| Catalog/auth | HTTP 200; Spark and Muse Image listed | Key/account-specific observation |
| Native video | Both supplied MP4s accepted; full-analysis calls 14.7s and 7.25s | Approximate timestamps; no exhaustive frame/text benchmark |
| Small simulations | Three personas per video; 80.094s and 55.485s; zero failed personas | Five hand-authored archetypes; opinions are synthetic |
| Fifty-person simulation | 199 valid verdicts across 50 cast IDs; 177.688s; estimated $0.3499982 | **Fails 90s target**; 33.78s input, not 60s worst-case; no p95 claim |
| Skip isolation | Actual dispatched file hashes matched current segments; zero post-skip dispatches or duplicate verdicts | Harness proof only; shared batch context is not strict persona isolation |
| Notes | One note per video; quote/reference checks passed against actual stored reactions | Suggestions need manual review; usefulness and stability not established |
| Image API | Four PNGs returned, 11.95–13.67s each; $0.01 each | API success does not imply export-ready quality |
| Audio-only controls | A returned intelligible workflow speech, with incorrect product-name transcription. B returned “No audio provided” | B WAV is non-silent: FFmpeg mean -15.4dB, peak -4.6dB. Treat B audio interpretation as failed/unreliable, not absent audio |
| File deletion | 20/20 DELETE results confirmed deleted; subsequent GET returned 404 | Upstream retention/backups not tested; local artifacts retained privately |
| Budget/secrets | No active/uncertain reservations; persisted-key scan passed | Usage-based estimate, not billing receipt; source chat itself contains the owner-supplied key |

The first two image requests returned HTTP 400 because tool switches were incorrectly placed at the top level. Corrected them to `tool_enablement`, inspected prior failures, then explicitly ran only the failed stage. Four successful generations followed. No automatic charged retries or geographic bypass.

## Product implications

- The two videos concern different products; they cannot prove a paired editing improvement. No matched A/B or thumbnail-voting experiment ran.
- Five archetypes repeated across 50 IDs and three contexts are not 50 independently validated audience profiles. This experiment supports plumbing feasibility, not virality prediction or calibrated retention.
- Viewers reaching successive A segments: 50, 37, 30, 29, 18, 18, 17. The 17 final observed viewers saw the 28–33s CTA then stopped; none received the remaining 33–33.782s segment. Avoid mislabeling this as real audience completion/drop-off. The original `completed` field meant still watching after the loop; later code uses explicit final-segment fields, and the artifact verifier derives them from events.
- The full-video interpreter and note writer have global context; persona requests do not. Each batch of at most five includes those personas' prior impressions, so cross-persona influence remains possible despite prompt instructions. No final-secret-cue adversarial test ran.
- Fixed 3s/5s chunks are temporal segments, not detected scene boundaries. Serial upload/scene barriers and repeated inference contribute to latency; optimize the actual pipeline before promising a 90s verdict. No new latency contract has been approved.
- Visual review rejected both A thumbnails for emphasizing document details; B variant 1 clips text; B variant 2 preserves readable wording and is the preferable experimental preview. Frame selection, sensitive-content screening and crop checks belong before export. Generation was not tested as product-proof footage.
- A note suggests showing the compressed result's readability before the CTA. B needs an actual captured workflow demonstration. Its generated note proposed synthetic UI: reject that part rather than present invented UI as a real product.
- B analysis also supplies a first-product timestamp despite saying no real product was shown. Structured output guarantees shape, not semantic consistency. Keep uncertainty visible and validate cross-field claims.

## Reproduce inspection without spending

From the repository root:

```powershell
python experiments/verify_smoke.py --out C:\Users\Shrikar\.codex\private-runs\viralist-20261028
python -m py_compile experiments/meta_smoke.py experiments/finish_smoke.py experiments/verify_smoke.py
git diff --check
```

Observed author verification: actual dispatch/file hashes, skip audits, unique verdicts, exact note evidence, deletion receipts, budget and persisted credential scan pass. No mocks used for provider calls. The files needed for this inspection remain private and are intentionally absent from a public checkout. Do not rerun paid scripts merely to review results.

REVIEW-ACCEPTED is pending independent exact-revision review. INTEGRATED/JOURNEY-VERIFIED/RELEASED are not earned; no app exists. S1 fidelity remains partial, S2 latency fails, S3 matched comparisons untested. Next product work requires the owner's implementation instruction and a latency/audio approach informed by these observations.

Sources for request formats/rates: [video and audio](https://dev.meta.ai/docs/video-understanding), [structured output](https://dev.meta.ai/docs/structured-output), [images and tool_enablement](https://dev.meta.ai/docs/image-generation), [pricing](https://dev.meta.ai/docs/pricing-rate-limits). Request dates and observed behavior above take precedence over general capability claims.
