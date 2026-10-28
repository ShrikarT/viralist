"""Audit v2's actual private artifacts; author verification, no paid calls."""
import argparse
from pathlib import Path
import subprocess

from meta_pipeline import read, digest, validate_analysis, validate_notes, thumbnail_allowed
from meta_smoke import write_json


def verify(out):
    report, ledger, media = read(out/"report.json"), read(out/"ledger.json"), read(out/"provider-media.json")
    assert not report["failures"], report["failures"]
    assert report["model"] == "muse-spark-1.3"
    assert ledger["estimated_from_reported_usage"] + ledger["uncertain_charge_reserve"] <= 10
    assert abs(ledger["active_reserve"]) < 1e-6
    previous = Path(ledger["previous_ledger"])
    assert digest(previous.read_bytes()) == ledger["previous_ledger_sha256"], "prior cost ledger changed"
    assert ledger["previous_spend"] == read(previous)["estimated_from_reported_usage"]
    assert all(c.get("requested_model") == "muse-spark-1.3" for c in ledger["calls"] if c["endpoint"] == "/responses")
    result = {"source_sha": report["source_sha"], "author_check_only": True, "stage": report["stage"],
              "simulations": {}, "cumulative_estimated_usd": ledger["estimated_from_reported_usage"],
              "uncertain_charge_reserve_usd": ledger["uncertain_charge_reserve"]}
    uploads = {read(p)["id"]: read(p)["filename"] for p in out.glob("response-*-upload.json")}
    for name, video in report["videos"].items():
        prefix = f"{name}-{video['simulation']['requested_personas']}"
        path = out/f"{prefix}-dispatch-audit.json"
        dispatch = read(path)
        records = read(out/f"{prefix}-reactions.json")
        summary = read(out/f"{prefix}-summary.json")
        assert summary["failed_personas"] == 0
        stop = {r["persona_id"]: r["scene"] for r in records if not r["still_watching"]}
        lookup = {(r["persona_id"],r["scene"]): r for r in records}
        assert len(lookup) == len(records) == len(dispatch)
        for d in dispatch:
            pid, index = d["persona_id"], d["scene"]
            scene = media[name]["scenes"][index]
            assert d["model"] == "muse-spark-1.3" and d["previous_response_id_present"] is False
            if d.get("representation") == "scene_local_observations_plus_real_frame":
                assert d["file_id"] is None
                assert d["image_sha256"] == scene["frame_sha256"] == digest(Path(scene["frame_path"]).read_bytes())
                assert d["features_sha256"] == scene["features_sha256"]
                features = read(out/f"{name}-scene-{index}-features.json")
                assert uploads[features["audit"]["file_id"]] == Path(scene["path"]).name
                assert features["audit"]["source_sha256"] == scene["sha256"]
                assert features["features"] == scene["features"]
                if "source_interval" in scene["features"]:
                    interval = scene["features"]["source_interval"]
                    assert interval["start_sec"] == scene["start_sec"] and interval["end_sec"] == scene["end_sec"]
                    assert all("at_sec" not in o for o in scene["features"]["observations"])
                    assert all(scene["start_sec"] <= t <= scene["end_sec"] for t in features["audit"]["unverified_model_point_times"])
                else:
                    assert all(scene["start_sec"] <= o["at_sec"] < scene["end_sec"] for o in scene["features"]["observations"])
                if "input_context_upper_bound_with_margin" in d:
                    calls = [c for c in ledger["calls"] if c["label"] == f"{prefix}-s{index}-{pid}" and c["endpoint"] == "/responses"]
                    assert len(calls) == 1 and calls[0]["status"] == "success"
                    assert calls[0]["usage"]["input_tokens"] <= d["input_context_upper_bound_with_margin"]
            else:
                assert uploads[d["file_id"]] == Path(scene["path"]).name
            assert digest(Path(scene["path"]).read_bytes()) == d["media_sha256"] == scene["sha256"]
            assert digest(Path(scene["audio_path"]).read_bytes()) == d["audio_sha256"] == scene["audio_sha256"]
            assert d["audio"] == scene["audio"], "wrong/future transcript projected"
            assert index <= stop.get(pid, 100000), "post-skip request"
            if index:
                prior = lookup[pid, index-1]
                assert prior["still_watching"] and prior["accepted_unix"] <= d["dispatched_unix"]
            assert d["start_sec"] == scene["start_sec"] and d["end_sec"] == scene["end_sec"]
            # Exactly one viewer appears; neither peer impressions nor full analysis.
            import json
            payload = json.loads(d["prompt"][d["prompt"].index('{'):])
            assert set(payload) == {"viewer", "current_segment"}
            assert payload["viewer"]["id"] == pid
            assert payload["current_segment"]["audio"] == scene["audio"]
            if "features" in scene:
                assert payload["current_segment"]["observations"] == scene["features"]
            streams = read_probe(scene["path"])
            assert not any(s["codec_type"] == "audio" for s in streams)
        validate_analysis(report["videos"][name]["analysis"], media[name]["duration_sec"])
        validate_notes(read(out/f"{prefix}-notes.json"), records)
        result["simulations"][prefix] = {"cast": summary["requested_personas"], "valid_verdicts": len(records),
                                        "post_skip_requests": 0, "peer_or_future_context": 0,
                                        "wall_sec": summary["wall_sec"]}
    cleanup = read(out/"cleanup.json")
    uploaded = read(out/"provider-files.json")
    assert set(x["file_id"] for x in cleanup) == set(uploaded)
    assert all(x.get("retrieval_status") == 404 and x.get("delete_response",{}).get("deleted") is True for x in cleanup)
    result["provider_files_deleted_and_404"] = len(cleanup)
    if report["stage"] == "small":
        assert all(v["passed"] for v in read(out/"audio-controls.json").values())
        assert len(report["thumbnails"]) == 4
        for name in ("a", "b"):
            assert thumbnail_allowed(read(out/f"{name}-frame-screen.json"))
        for thumb in report["thumbnails"]:
            assert digest(Path(thumb["path"]).read_bytes()) == thumb["sha256"]
            left, top, right, bottom = thumb["title_bounds"]
            w, h = thumb["canvas_size"]
            assert left >= 64 and right <= w-64 and top >= 0 and bottom < h-64
    result["passed"] = True
    write_json(out/"verification.json", result)
    return result


_probes = {}
def read_probe(path):
    if path not in _probes:
        import json
        _probes[path] = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-of", "json", path]))["streams"]
    return _probes[path]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    import json
    print(json.dumps(verify(args.out), indent=2))
