"""Offline regression tests of the actual experimental scheduler/validators.

Only the external model is replaced; scheduler, projection and validation run.
"""
import concurrent.futures
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest

from PIL import Image
from meta_pipeline import (audio_state, compose_thumbnail, persona_prompt, simulate,
                           thumbnail_allowed, validate_analysis, validate_notes, validate_verdict)


class ExternalStub:
    def __init__(self, out):
        self.out = out
        self.lock = threading.Lock()
        self.current = 0
        self.max_active = 0
        self.calls = []

    def safe(self, value):
        return str(value)

    def text(self, label, prompt, schema, file_id=None, max_output=0, audit=None):
        with self.lock:
            self.current += 1
            self.max_active = max(self.max_active, self.current)
            self.calls.append((label, prompt, file_id))
        time.sleep(.003)
        person = json.loads(prompt[prompt.index('{'):])["viewer"]
        # p001 stops immediately; p002 continues through the final secret cue.
        keep = person["id"] != "p001"
        audit.update(model="muse-spark-1.3", file_id=file_id, prompt=prompt, previous_response_id_present=False)
        with self.lock:
            self.current -= 1
        return {"verdicts": [{"persona_id": person["id"], "still_watching": keep,
                              "reason": "Specific scene response", "impression": "Own impression", "actions": []}]}


def scenes():
    return [{"index": i, "start_sec": i*3, "end_sec": (i+1)*3, "file_id": f"scene-{i}",
             "sha256": f"video-hash-{i}", "audio_sha256": f"audio-hash-{i}",
             "audio": {"speech_transcript": "LATE_ONLY_SECRET_CUE" if i == 2 else "current words"}}
            for i in range(3)]


class PipelineRegression(unittest.TestCase):
    def test_actual_scheduler_no_future_peer_or_post_skip_input(self):
        with tempfile.TemporaryDirectory() as temp:
            client = ExternalStub(Path(temp))
            summary, records = simulate(client, {"scenes": scenes()}, "test", 2, workers=2)
            self.assertEqual(summary["failed_personas"], 0)
            self.assertEqual(summary["reached_final_segment"], 1)
            self.assertEqual(summary["still_watching_after_final_segment"], 1)
            self.assertGreater(client.max_active, 1)
            p1 = [(label, prompt, fid) for label, prompt, fid in client.calls if label.endswith("p001")]
            self.assertEqual(len(p1), 1)
            self.assertNotIn("p002", p1[0][1])
            self.assertNotIn("LATE_ONLY_SECRET_CUE", p1[0][1])
            self.assertEqual(p1[0][2], "scene-0")
            self.assertEqual(len({(r["persona_id"], r["scene"]) for r in records}), len(records))

    def test_current_transcript_projection(self):
        early = persona_prompt({"id": "p001", "impression": ""}, scenes()[0])
        late = persona_prompt({"id": "p001", "impression": "own past"}, scenes()[2])
        self.assertNotIn("LATE_ONLY_SECRET_CUE", early)
        self.assertIn("LATE_ONLY_SECRET_CUE", late)

    def test_wrong_and_duplicate_persona_rejected(self):
        verdict = {"persona_id": "p002", "still_watching": True, "reason": "reason", "impression": "own"}
        with self.assertRaises(ValueError):
            validate_verdict({"verdicts": [verdict]}, "p001")
        with self.assertRaises(ValueError):
            validate_verdict({"verdicts": [verdict, verdict]}, "p002")

    def test_non_silent_audio_never_becomes_absent(self):
        state = audio_state({"audio_track_present": True, "audio_stats": {"non_silent": True}}, {"transcript": ""})
        self.assertTrue(state["audio_track_present"])
        self.assertTrue(state["non_silent"])
        self.assertFalse(state["speech_detected"])

    def test_contradictory_product_timestamp_rejected(self):
        value = {"product_demonstrated": False, "product_first_shown_sec": 5.8,
                 "product_evidence": [], "visible_text": [], "cta": {"at_sec": None}}
        with self.assertRaises(ValueError):
            validate_analysis(value, 17)
        value["product_first_shown_sec"] = None
        validate_analysis(value, 17)

    def test_note_quotes_times_and_fake_proof_rejected(self):
        record = {"evidence_id": "e1", "reason": "No actual workflow shown", "start_sec": 3, "end_sec": 8}
        note = {"start_sec": 3, "end_sec": 8, "evidence_ids": ["e1"], "quotes": [record["reason"]],
                "suggested_edit": "Capture the actual workflow"}
        validate_notes({"notes": [note]}, [record])
        for field, value in (("quotes", ["Invented quote"]), ("end_sec", 9), ("suggested_edit", "Show synthetic UI")):
            broken = dict(note, **{field: value})
            with self.assertRaises(ValueError):
                validate_notes({"notes": [broken]}, [record])

    def test_private_or_irrelevant_frames_cannot_be_selected(self):
        safe = {"identity_document_visible": False, "private_data_visible": False, "relevant_product_or_result": True}
        self.assertTrue(thumbnail_allowed(safe))
        for field in ("identity_document_visible", "private_data_visible"):
            self.assertFalse(thumbnail_allowed(dict(safe, **{field: True})))
        self.assertFalse(thumbnail_allowed(dict(safe, relevant_product_or_result=False)))

    def test_headline_and_mobile_layout_fit(self):
        with tempfile.TemporaryDirectory() as temp:
            source, dest = Path(temp)/"background.png", Path(temp)/"thumb.png"
            Image.new("RGB", (1024, 1536), "gray").save(source)
            value = compose_thumbnail(source, dest, "Document accepted", True)
            left, top, right, bottom = value["title_bounds"]
            w, h = value["canvas_size"]
            self.assertGreaterEqual(left, 64)
            self.assertLessEqual(right, w-64)
            self.assertGreaterEqual(top, 0)
            self.assertLess(bottom, h-64)
            self.assertTrue(Path(value["mobile_preview"]).exists())


if __name__ == "__main__":
    unittest.main()
