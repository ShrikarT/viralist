"""Inspect actual smoke-run artifacts. Author check, not independent verification."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify(out):
    media = read(out / "media.json")
    report = read(out / "report.json")
    ledger = read(out / "ledger.json")
    uploads = {}
    for path in out.glob("response-*-upload.json"):
        value = read(path)
        uploads[value["id"]] = value["filename"]
    result = {"run_source_sha": report["source_sha"], "author_check_only": True,
              "scope": "experiment harness, not production app", "simulations": {}}
    for path in out.glob("*-dispatch-audit.json"):
        prefix = path.name.removesuffix("-dispatch-audit.json")
        name = prefix.split("-")[0]
        dispatch = read(path)
        reactions = read(out / (prefix + "-reactions.json"))
        summary = read(out / (prefix + "-summary.json"))
        stops = {r["persona_id"]: r["scene"] for r in reactions if not r["still_watching"]}
        last = len(media[name]["scenes"]) - 1
        seen = set()
        for r in reactions:
            pair = (r["persona_id"], r["scene"])
            assert pair not in seen, "duplicate accepted verdict"
            seen.add(pair)
        for d in dispatch:
            scene = media[name]["scenes"][d["scene"]]
            clip = Path(scene["path"])
            assert uploads[d["sent_file_id"]] == clip.name, "wrong/full-video file dispatched"
            assert hashlib.sha256(clip.read_bytes()).hexdigest() == d["media_sha256"] == scene["sha256"]
            assert d["start_sec"] == scene["start_sec"] and d["end_sec"] == scene["end_sec"]
            assert d["previous_response_id_present"] is False
            for pid in d["persona_ids"]:
                assert pid not in stops or d["scene"] <= stops[pid], "post-skip dispatch"
            assert "Whole-video observations" not in d["prompt"]
        result["simulations"][prefix] = {
            "requested": summary["requested_personas"], "failed": summary["failed_personas"],
            "post_skip_dispatches": 0, "correct_scene_files": True, "duplicate_verdicts": 0,
            "stopped_before_final_segment": sum(s < last for s in stops.values()),
            "reached_final_segment": len({r["persona_id"] for r in reactions if r["scene"] == last}),
            "said_stop_after_final_segment": sum(s == last for s in stops.values()),
            "wall_sec": summary["wall_sec"],
        }
    for name in ("a", "b"):
        path = out / f"{name}-notes.json"
        if not path.exists():
            continue
        notes = read(path)["notes"]
        reactions = {r["evidence_id"]: r for r in read(out / f"{name}-3-reactions.json")}
        for note in notes:
            assert set(note["evidence_ids"]) <= set(reactions)
            assert all(q in {reactions[i]["reason"] for i in note["evidence_ids"]} for q in note["quotes"])
        result[name + "_note_evidence"] = "PASS" if notes else "NO_SUPPORTED_NOTE"
    cleanup = read(out / "cleanup.json")
    assert len(cleanup) == len(read(out / "provider-files.json"))
    result["provider_file_deletion"] = {
        "uploaded": len(cleanup),
        "confirmed_unretrievable": sum(x.get("retrieval_status") == 404 and x.get("delete_response", {}).get("deleted") is True for x in cleanup),
        "pending": [x for x in cleanup if x.get("retrieval_status") != 404 or not x.get("delete_response", {}).get("deleted")],
    }
    result["estimated_cost_usd"] = ledger["estimated_from_reported_usage"]
    result["uncertain_charge_reserve_usd"] = ledger["uncertain_charge_reserve"]
    assert ledger["active_reserve"] < .000001
    assert result["estimated_cost_usd"] + result["uncertain_charge_reserve_usd"] <= 10
    result["provider_failures"] = report["failures"]
    result["image_count"] = len(report["thumbnails"])
    # No keys in any tracked file, or in persisted experiment JSON/logs.
    secret = re.compile(r"LLM_[A-Za-z0-9]{8,}_[A-Za-z0-9]{10,}")
    tracked = subprocess.check_output(["git", "ls-files"]).decode().splitlines()
    for path in [Path(p) for p in tracked] + list(out.glob("*.json")) + list(out.glob("*.log")):
        assert not secret.search(path.read_text(encoding="utf-8")), "credential found in persisted artifact"
    result["persisted_credential_scan"] = "PASS"
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.out)
    (args.out / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
