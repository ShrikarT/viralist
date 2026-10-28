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
from unittest.mock import patch

from PIL import Image
from meta_pipeline import (PipelineClient, audio_state, compose_thumbnail, normalize_scene_features, output_json, persona_prompt, simulate,
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

    def text(self, label, prompt, schema, file_id=None, max_output=0, audit=None, image_path=None):
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
    def test_rounded_endpoint_is_bound_to_source_without_guessing_point_precision(self):
        scene = {'start_sec':18, 'end_sec':23}
        raw = {'observations':[{'at_sec':23.0,'description':'Result visible in final source frame'}]}
        result = normalize_scene_features(raw, scene)
        self.assertEqual(result['source_interval']['start_sec'],18)
        self.assertEqual(result['source_interval']['end_sec'],23)
        self.assertNotIn('at_sec',result['observations'][0])
        self.assertEqual(raw['observations'][0]['at_sec'],23.0)
        with self.assertRaisesRegex(ValueError,'future timestamp'):
            normalize_scene_features({'observations':[{'at_sec':23.1,'description':'outside source'}]},scene)

    def test_full_fifty_cast_scheduler_preserves_ids_and_stop_isolation(self):
        with tempfile.TemporaryDirectory() as temp:
            client = ExternalStub(Path(temp))
            summary, records = simulate(client, {'scenes': scenes()}, 'fifty', 50, workers=32)
            self.assertEqual(summary['requested_personas'], 50)
            self.assertEqual(summary['failed_personas'], 0)
            self.assertEqual(len({r['persona_id'] for r in records}), 50)
            self.assertEqual(summary['valid_verdicts'], 148)
            self.assertEqual(summary['post_skip_dispatches'], 0)
            self.assertGreater(client.max_active, 1)

    def test_current_image_context_is_counted_once_without_sharing_persona_text(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            prior = out/'previous.json'
            prior.write_text(json.dumps({'active_reserve': 0, 'estimated_from_reported_usage': .1, 'uncertain_charge_reserve': 0}))
            image = out/'frame.png'
            Image.new('RGB', (20,20), 'gray').save(image)
            with patch('meta_smoke.sys.stdin.readline', return_value='test-credential\n'):
                client = PipelineClient(out, prior)
            calls = []
            lock = threading.Lock()
            def call(label, method, endpoint, body=None, **kwargs):
                with lock:
                    calls.append((label, endpoint, body, kwargs))
                if endpoint.endswith('input_tokens'):
                    self.assertEqual(body['input'][0]['content'][0]['text'], '')
                    time.sleep(.01)
                    return {'input_tokens': 1400}
                return {'status': 'completed', 'usage': {'input_tokens': 1500}, 'output': [
                    {'type': 'message', 'content': [{'type':'output_text', 'text':'{"ok":true}'}]}]}
            client.call = call
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
                values = list(pool.map(lambda i: client.text(f'p{i}', f'Only viewer p{i}', {'type':'object'}, image_path=image), range(3)))
            self.assertEqual(sum(e[1].endswith('input_tokens') for e in calls), 1)
            self.assertEqual(len(values), 3)
            generation = [e for e in calls if e[1] == '/responses']
            self.assertEqual(len(generation), 3)
            for label, endpoint, body, options in generation:
                self.assertEqual(body['input'][0]['content'][0]['text'], 'Only viewer '+label)
                self.assertGreater(options['reserve'], .01)

    def test_projected_path_keeps_future_observations_and_peer_impressions_out(self):
        with tempfile.TemporaryDirectory() as temp:
            client = ExternalStub(Path(temp))
            segments = scenes()
            for s in segments:
                s.update(features={"scene_summary": 'LATE_ONLY_VISUAL_CUE' if s['index'] == 2 else 'current visual'},
                         features_sha256=f'feature-{s["index"]}', frame_path='current-frame.png')
            summary, records = simulate(client, {'scenes': segments}, 'projected', 2, workers=2)
            self.assertEqual(summary['representation'], 'scene_local_observations_plus_real_frame')
            self.assertFalse(summary['live_native_scene_clips'])
            early = [c for c in client.calls if c[0].endswith('s0-p001')][0]
            self.assertNotIn('LATE_ONLY_VISUAL_CUE', early[1])
            self.assertNotIn('LATE_ONLY_SECRET_CUE', early[1])
            self.assertNotIn('p002', early[1])
            self.assertIsNone(early[2])
            self.assertEqual(summary['post_skip_dispatches'], 0)

    def test_truncated_model_output_never_accepted_as_verdict(self):
        with self.assertRaisesRegex(ValueError, "incomplete model response"):
            output_json({"status": "incomplete", "output": []})

    def test_external_failure_keeps_partial_cast_visible_without_later_dispatch(self):
        with tempfile.TemporaryDirectory() as temp:
            client = ExternalStub(Path(temp))
            original = client.text
            def partial(label, *args, **kwargs):
                if label.endswith('p001'):
                    raise RuntimeError('HTTP 500 terminal test response')
                return original(label, *args, **kwargs)
            client.text = partial
            summary, records = simulate(client, {'scenes': scenes()}, 'test', 2, workers=2)
            self.assertEqual(summary['failed_personas'], 1)
            self.assertEqual(summary['failures'][0]['persona_id'], 'p001')
            self.assertTrue(all(r['persona_id'] == 'p002' for r in records))

    def test_budget_queue_reserves_concurrent_calls_and_releases_capacity(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            prior = out/"previous.json"
            prior.write_text(json.dumps({"active_reserve": 0, "estimated_from_reported_usage": .1, "uncertain_charge_reserve": 0}))
            with patch("meta_smoke.sys.stdin.readline", return_value="test-only-credential\n"):
                client = PipelineClient(out, prior)
            client.limit = 2.11
            active = 0
            maximum = 0
            lock = threading.Lock()

            def request(*args, **kwargs):
                nonlocal active, maximum
                with lock:
                    active += 1
                    maximum = max(maximum, active)
                time.sleep(.01)
                with lock:
                    active -= 1
                class Response:
                    status_code, ok, headers = 200, True, {}
                    def json(self):
                        return {"id": "stub-external-response"}
                return Response()

            with patch("meta_smoke.requests.Session.request", side_effect=request):
                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                    list(pool.map(lambda i: client.call(f"test-{i}", "GET", "/test", reserve=1, fixed_cost=.001), range(8)))
            self.assertEqual(maximum, 2)
            self.assertAlmostEqual(client.spent, .108)
            self.assertAlmostEqual(client.reserved, 0)
            client.uncertain = 2.1
            with self.assertRaisesRegex(RuntimeError, "no safe capacity"):
                client.call("must-not-dispatch", "GET", "/test", reserve=1)

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
        safe_warning = dict(note, suggested_edit="Add a real capture; do not use synthetic or mock UI.")
        validate_notes({"notes": [safe_warning]}, [record])
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
