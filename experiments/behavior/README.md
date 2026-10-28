# Behavioral-persona experiment

`policies.json` contains six fictional candidate policies and the generic baseline. `retained-policies.json` is the measured prototype subset, once the run has been analyzed. Neither file establishes real audience fidelity or fifty distinct behaviors.

The immutable design is in `PROTOCOL.md`, `freeze.json`, `stimuli-runtime.json` and `analysis-plan.json`. Expectations are analysis-only; `run_benchmark.py` never loads them. The original fifty-instance cast remains unchanged.

Offline commands from the repository root, with Python dependencies from `experiments/requirements.txt` available:

```powershell
python -m unittest discover -s experiments -p 'test_*.py'
python experiments/behavior/verify_benchmark.py --run <private-phase-directory> --assets <private-assets-directory>
python experiments/behavior/analyze_benchmark.py --runs <development-directory> <heldout-directory> <controls-directory> --out <private-results-directory>
```

Verification requires the saved private artifacts. It makes no provider calls. The paid runner rejects an existing ledger rather than silently repeating it; every phase must chain the actual previous ledger. The original cumulative owner ceiling and unknown-charge reserve must survive every continuation. Do not run a paid command to inspect existing results.

Fixture construction uses `build_study.py`, the pinned HyperFrames project in `video-project/`, FFmpeg and `run_benchmark.py prepare`. Static source capture is 1fps; native eight-second clips repeat those exact states at 24fps. All transitions are integer-second cuts. These are controlled toy-operation cards, with no natural motion/audio or production-product claim.

The 2026-10-28 execution retains a disclosed constant footer metadata encoding deviation. Its exact media manifest hash and scope live in the private `assets/encoding-deviation.json`; the verifier checks it explicitly. All task-bearing strings and real frames match the frozen design. Rebuilding fixtures produces correct UTF-8, and must be treated as a new input artifact rather than relabeled evidence from this run.
