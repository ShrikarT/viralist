# Contract proposal v1

Status: design only. The integrator freezes executable schemas and generated types in V02 after owner decisions and V01 capability evidence. [vertical-slice.v1.json](contracts/vertical-slice.v1.json) is the single synthetic producer/consumer example. It is not a run, provider receipt or production response. All examples use fictitious IDs/media. Its two-person test profile is never a substitute for the 50-person Flash acceptance test.

## Cross-module contracts

| ID | Producer → consumer | Required shape / invariant | Failure |
|---|---|---|---|
| C1 Media accepted | HTTP/storage → feature worker | `video_id, owner_id, media_ref, sha256, duration_ms, width, height, audio_present, bytes`; private references; ≤60,000ms and ≤200,000,000 bytes | 413 size; 422 format/duration; cleanup quarantine; no model call |
| C2 Feature bundle | extractor → scheduler/detectors | `schema_version, video_id, extractor_version, timebase, scenes[], caveats[], provenance[]`; each scene has ordered `[start_ms,end_ms)`, frame/clip refs, scene-local transcript/OCR/measurements and timestamp granularity | Missing audio is a caveat; missing media/timebase is fatal; missing optional observation is null, not zero |
| C3 Persona batch | scheduler → provider adapter → scheduler | Current scene, active persona IDs/cards/checkpoints, allowed past state; verdict for each ID with `still_watching, actions[], impression_update, drop_reason, signals` | Reject unknown IDs, duplicate blocks, invalid times, >60-word impression, unallowed actions; skip requires reason |
| C4 Event/checkpoint | scheduler transaction → event store → SSE/UI | `run_id, sequence, event_id, type, payload`; verdict/checkpoint/event committed atomically, unique accepted persona/scene verdict | Reconnect after sequence; duplicates ignored by event ID; no speculative UI events |
| C5 Report | aggregation/notes → API/UI | effective/requested cast, methodology, ranges, evidence references, ≤3 ranked notes, trust manifest, coverage/caveats | Unsupported note suppressed; unavailable metric null with reason; incomplete cast labeled |
| C6 Comparison | two owned complete/partial runs → compare/UI | base/revised IDs, compatibility reasons, same cast/settings hashes, paired-delta method, note match confidence | Different owner 404; incompatible settings 409; uncertain mapping not marked addressed |
| C7 Thumbnail | owned media → permitted image provider or layout fallback → vote adapter → UI | original + 3 variants; source type/provenance; same 30-person panel per variant; vote/reason/evidence | Muse Image playground owner-confirmed; API/policy discrepancy must be resolved for app use; fallback/failed votes labeled, no inferred winner on tie |
| C8 Deletion | API tombstone → worker/stores/provider adapters → UI | deletion ID, pending targets, access revoked time, completion times; repeat request same operation | Provider failure retains pending target; workers fenced; report never says “fully deleted” early |

## Wire and domain conventions

Server-generated opaque identifiers; milliseconds as nonnegative integers; UTC ISO timestamps; bounded strings; discriminated event/error types; unknown schema versions fail validation. Reject NaN/Infinity and invalid ranges. Ownership stays server-side and is never trusted from a request body. `impression_update` is a bounded summary of past/current content only.

Scenes are contiguous over accepted duration, max five seconds for Flash, with a 0–3s hook boundary (or the video end when shorter). Decoder scene cuts can create shorter intervals. Regular actions are within `[start_ms,end_ms)`; stop decisions may occur exactly at `end_ms`. Transcript overlap is clipped by time. When a segment's semantics span a boundary, do not leak later words into the earlier prompt; flag coarse timing instead.

Action enum: `like, share, save, comment, follow`. Watching/stopping uses `still_watching`, not contradictory action flags. Optional comment has its own evidence ID and filtering status; do not alter a quote and still label it verbatim. Signals: `confused: boolean|null`, `cta_understood: boolean|null`, `matched_trend_rule_ids: string[]`; null means unobserved. Any trend match must reference a stored rule and current/past feature evidence.

FeatureBundle is a storage contract, **not** permission to send the whole bundle to personas. Construct a separate `SceneInput` projection; include an `allowed_media_refs` list and `max_visible_ms` in dispatch audit. Provider caches must never bind a persona to an earlier whole-video request.

## Internal HTTP proposal

All routes are same-origin, session-authorized and rate-limited. Unowned IDs return 404; absent/expired sessions require recovery without revealing object existence. Mutating routes require origin/CSRF validation. `Idempotency-Key` is scoped by owner + route and binds a request hash; reuse with changed input returns 409. Default routes do not expose a public share URL.

| Route | Request | Success / other state |
|---|---|---|
| `POST /sessions` | no signup; server issues opaque capability cookie | 201 expiry/retention disclosure; never return credential in URLs |
| `POST /videos` | multipart owned MP4; validated metadata | 201 `{video_id,status:"uploaded"}`; stream to private quarantine |
| `GET /videos/{id}/analysis` | owned video | 200 stage, completed observations, caveats |
| `POST /runs` | `{video_id,platform:"reels",tier:"flash",audience_preset_id,comparison_group_id?}` | 202 `{run_id,status,events_url}`; duplicate key returns original run |
| `GET /runs/{id}` | owned run | 200 durable status/sequence; poll fallback |
| `GET /runs/{id}/events` | `Last-Event-ID` or `after` cursor | SSE persisted events; heartbeat has no reaction semantics; expired cursor returns snapshot/reset marker |
| `GET /runs/{id}/report` | owned run | 200 report if ready; 202 current stage; 410 deleted |
| `GET /runs/{base}/compare/{revised}` | two owned runs | 200 comparison or 409 incompatible/not-ready with reason |
| `POST /runs/{id}/thumbnails` | owned source frame choice + title | 202 operation; idempotent, bounded to original + 3 variants |
| `GET /runs/{id}/thumbnails` | owned run | 200 pending/result with vote denominators/provenance |
| `GET /videos` | current owner | 200 session history, never other sessions' videos |
| `DELETE /videos/{id}` | confirmation in client, idempotency key | 202 `{deletion_id,status:"pending"}`; immediate access revocation |
| `GET /deletions/{id}` | owned operation | 200 pending targets or complete; redacted target classes only |

Error envelope: `{code,stage,message,retryable,request_id}`. Safe user text only. Raw provider errors may be retained in restricted redacted diagnostics; no authorization headers or content excerpts. Later what-if/PDF/share endpoints are defined by V08 before coding; they are not part of the first slice interface.

## Provider boundary — documented request, untested account

Base `https://api.meta.ai/v1`, Bearer key supplied server-side. The video guide documents `POST /files` with `purpose=user_data`, then `POST /responses` with model and an input user message containing `{type:"input_file",file_id:...}` plus text. A URL video uses `{type:"input_video",video_url:...}`. See [Meta video guide](https://dev.meta.ai/docs/video-understanding). The fixture's `provider_request_shape` contains placeholders and is illustrative only.

Adapter returns our normalized `{request_id,model_id,reported_version,output,usage,latency_ms,status}`. This is **our interface**, not a claimed Meta response shape. V01 must save redacted real response examples and map actual usage/schema/refusal fields before V02 locks serialization. `reported_version` may be null; model ID alone is not an exact immutable backend revision.

No calls in this planning pass. Test supported structured-output behavior, video/audio path, per-account catalog, token counting and cancellation/retrieval capabilities before relying on them. Never guess a second endpoint/model ID after a rejected request. Live retries use ARCHITECTURE's bounded policy.

## Metric and evidence contracts

Each metric has `kind` (`observed_count`, `simulation_range`, `heuristic_index`, `hypothetical_reach`), unit, optional observed value, range/method, denominator and evidence IDs. Count and derived range are different fields. Notes cite both a trigger observation and persona evidence; absence of a supported fix means no negative note. Comparison can legitimately show no supported difference.

Ranges: 200 resamples of whole persona traces; nearest-rank p10/p90 (`ceil(p*n)`, one-based). Fixture supplies three explicit resamples only to make arithmetic hand-checkable; production uses 200 and records seed/method. For paired A/B resample the same indices across cuts. Never subtract independent endpoint bounds and call that a paired interval.

Trend-fit output is unavailable when rules or evidence are missing. A static pack date is distinct from the provider model's training cutoff. Every report carries source Git SHA, media/feature/cast/config/prompt hashes, model IDs/reported versions, observed time, call-usage ledger, replay/live flag and limitations.

## Required negative fixture mutations

- Add a scene-1 request for skipped `p1`: scheduler/audit test must fail; do not replace production scheduler with fixture logic.
- Insert full-video media reference or future transcript in scene 0: projection validator rejects dispatch.
- Duplicate accepted persona verdict/event: persistent result and streamed counts remain unchanged.
- Change a note evidence reference to `missing`: report validator rejects it.
- Change another owner's video ID: no object/report/event/thumbnail/delete access.
- Replay deleted media job with old lease: no new bytes/report created; late provider output enters cleanup.
- Give A/B mismatched model/pack hashes: incompatible comparison, no winner.
- Mark a synthetic fixture as live: provenance validator rejects it.
