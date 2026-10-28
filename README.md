# Viralist

Test a short product demo with a simulated audience, inspect timestamped editing notes, and compare your next cut.

**Status: local feasibility experiments, updated 28 October 2026.** Real Meta API experiments and offline scheduler/validation tests exist; the application and deployment remain unbuilt. Owner-selected remote: [ShrikarT/viralist](https://github.com/ShrikarT/viralist), configured locally as `origin`; no push performed. The strategy remains a recommendation except for explicitly recorded owner confirmations.

Start with [the planning handoff](docs/START_HERE.md), [the product brief](docs/PROJECT_BRIEF.md), and [the delivery plan](PLAN.md). Current evidence and next actions are in [STATE](docs/STATE.md). Operating rules are in [AGENTS](AGENTS.md).

The hackathon slice is Flash Scan → Director's Notes → edited-cut comparison → Thumbnail Lab, for Instagram Reels. Outputs describe a simulation; they do not predict real-world reach or reproduce Instagram's algorithm. The full product roadmap remains sequenced after this slice.

Experiment evidence: [initial provider spike](docs/evidence/provider-spike.md) and [Spark 1.3 fixes and rerun](docs/evidence/spark13-rerun.md). These are author-reported experimental results, not a deployed product or validated audience forecast. Dependencies observed in the experiment environment are recorded in `experiments/requirements.txt`; FFmpeg/ffprobe must also be available.

Free local regression checks, from this repository root:

```powershell
python -m unittest discover -s experiments -p test_pipeline.py -v
```

The current paid runner is `experiments/meta_pipeline.py`; it requires explicit stage, private output paths and a cumulative prior-spend ledger. Its scale stage requires a passing inspected small-stage gate at the same revision. Credentials use private stdin or `MODEL_API_KEY`; media, raw responses and keys stay outside Git. Do not run a paid stage simply to inspect evidence. No application development commands exist yet; do not run a parent directory's package scripts.
