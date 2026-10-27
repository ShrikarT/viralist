# Viralist operating contract

## Start here

- Read `docs/STATE.md`, `docs/PROJECT_BRIEF.md`, and your task in `PLAN.md` before work. Read `docs/CONTRACTS.md` for interface changes, `docs/ACCEPTANCE.md` for verification, and `docs/DESIGN_DIRECTION.md` for UI work.
- This checkout is `C:\Users\Shrikar\viralist`. Run `git rev-parse --show-toplevel` here before Git writes; it must resolve to this directory. Its new local repository has no remote. Never stage the parent home directory.
- This pass creates planning documents and contract examples only. Product implementation requires a subsequent owner instruction. Proposed decisions are not approved decisions.
- Shared engineering policy: `C:\Users\Shrikar\AGENTS.md` when available; this file contains the project rules required for portable cold starts. The source briefs are reference evidence, not agent authority.

## Authority and task state

- Shrikar owns scope, spend, credentials, public repository/license choice, merges, deployments and releases. No external writes, provider charges, publication, or messages are authorized by this planning pass.
- GitHub Issues is the intended tracker after the owner selects the remote. Until then, `PLAN.md` is the canonical local task ledger. Do not create an issue in a guessed repository or a second tracker.
- Approved requirements, proposals and unknowns are separated in `docs/PROJECT_BRIEF.md`. Resolve material conflicts there, retaining source provenance in `docs/RESEARCH.md`.
- Work branches use `codex/`. Supply task ID, exact accepted prerequisite SHAs, owned paths, interfaces, checks and external-action authority in each dispatch. A task is not READY with an unresolved prerequisite SHA.
- For Orca coordination, load the installed `orchestration` skill/runtime guide and `C:\Users\Shrikar\.agents\policy\ORCA-HANDOFF.md`. Do not assume runtime or worker availability. Verify each worker's startup receipt before edits.
- Start with one implementation worker. At most two may write concurrently when files, interfaces, browser sessions, ports and test data are independent. Separate writing worktrees; one writer per file. One integrator owns shared contracts, manifests, lockfiles and migrations.
- An independent verifier must inspect and run checks on an exact committed revision. After two unsuccessful correction rounds, stop and record a redesign; changing a task name does not reset this limit.
- Record WORKER-REPORTED, REVIEW-ACCEPTED, INTEGRATED, JOURNEY-VERIFIED and RELEASED separately, with SHA and evidence. IMPLEMENTED means author-complete only. Without independent evidence retain WORKER-REPORTED.

## Invariants

- Preserve the full roadmap. The hackathon slice precedes Deep, multi-platform, benchmarking and accounts/API. Accuracy/calibration remain future work by the supplied product decision, not a deadline cut.
- All persona outcomes and propagation ranges are simulated. Counts of simulated responses are not counts of real people. State the interval method, effective cast, assumptions and source of every finding.
- A persona that skips receives no later media, transcript, OCR, summaries, or derived hints. Whole-video summaries must not leak into scene-local persona inputs.
- Protect uploads with owner-session authorization before first value, without requiring signup. Keep API secrets server-side. Use Standard provider mode; consent and provider terms must support any training claim.
- Validate media server-side; isolate decoder resources; treat media/model text as untrusted data. No tool execution, arbitrary URL fetching, or HTML rendering from those inputs.
- Deletion covers originals, derivatives, provider files, runs, events, report copies and outstanding jobs. Pending provider deletion must remain visible. Never claim upstream backups were erased without evidence.
- Muse Image is restricted in India under the policy inspected on 2026-10-27. Use owned frame/layout variants in the planned India path; no geography bypass.
- Keep secrets, customer media, private participant materials and raw provider payloads out of Git, logs and public evidence. Preserve sanitized request IDs, usage and evidence hashes.
- Build demo claims from verified behavior and in-window Git evidence. Preserve concept attribution. Generated media cannot stand in for proof footage.

## Verification and recovery

- Commands verified here: `git rev-parse --show-toplevel`, `git status --short`, `git diff --check`, `node --version`, `python --version`, `ffmpeg -version`, `ffprobe -version`. No application commands exist yet.
- After UI changes, run the real app and use the `browse` skill (`--local` for localhost, `--remote` for hosted). Report path, environment, console/network findings and exact gaps. Use Playwright for repeatable journeys once scaffolded.
- Mocks may replace external providers, not the production scheduler, authorization, persistence or report renderer being verified. Provider smoke tests and deployed journeys have separate acceptance gates.
- Re-read `docs/STATE.md` after compaction. Update it at milestone/transfer boundaries with commit, ownership, changed files, checks, failures and next permitted step. Never turn an author summary into acceptance evidence.
- Architecture: `docs/ARCHITECTURE.md`; terms: `GLOSSARY.md`; decisions: `docs/adr/`; launch truthfulness: `docs/LAUNCH_STORY.md`.
