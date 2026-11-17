#!/usr/bin/env python3
"""
Capstone trials: runs the five criteria in criteria.md ("Capstone criteria")
against the real service, once per call.

    python run_capstone.py --trial 1

It starts `python app.py` itself on port 5001 (so a copy you have running on
5000 is left alone), restarting it with a different AI201_FAULT for each
criterion. Every request goes to the real logs/audit.jsonl. The full output,
with every response and log line, is saved to results/capstone_<date>_trial<N>.md.

Criterion 3 waits 61 seconds on purpose, so a trial takes about 5 minutes.
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime

import config

PORT = 5001
BASE = f"http://127.0.0.1:{PORT}"
OUT = []


def say(line=""):
    print(line, flush=True)
    OUT.append(line)


# ── The service ──────────────────────────────────────────────────────────────

class Service:
    """`python app.py` with one fault switched on, started and stopped here."""

    def __init__(self, fault=""):
        env = dict(os.environ, PORT=str(PORT), AI201_DEBUG="0", AI201_FAULT=fault)
        self.proc = subprocess.Popen(
            [sys.executable, "app.py"], env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        for _ in range(120):
            try:
                urllib.request.urlopen(f"{BASE}/health", timeout=2)
                return
            except Exception:  # noqa: BLE001
                time.sleep(0.5)
        raise RuntimeError("The service didn't start on port 5001.")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.proc.terminate()
        self.proc.wait(timeout=30)


def post(path, body):
    """Returns (status code, JSON body, seconds the client waited)."""
    req = urllib.request.Request(
        f"{BASE}{path}", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    start = time.perf_counter()
    try:
        r = urllib.request.urlopen(req, timeout=120)
        code, raw = r.status, r.read()
    except urllib.error.HTTPError as e:
        code, raw = e.code, e.read()
    secs = time.perf_counter() - start
    try:
        data = json.loads(raw)
    except ValueError:
        data = {"_not_json": raw[:200].decode(errors="replace")}
    return code, data, secs


def short(data):
    """A response with the long label cut down, for the output file."""
    d = dict(data)
    if isinstance(d.get("label"), str) and len(d["label"]) > 70:
        d["label"] = d["label"][:70] + "..."
    return json.dumps(d, ensure_ascii=False)


def log_lines():
    if not config.AUDIT_LOG.exists():
        return []
    return config.AUDIT_LOG.read_text(encoding="utf-8").splitlines()


def texts():
    with open("attack_set/attacks.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    valid = [r["text"] for r in rows if 50 <= len(r["text"].strip()) <= 10_000]
    return [valid[i] for i in range(0, len(valid), max(1, len(valid) // 10))][:10]


# ── The five criteria ────────────────────────────────────────────────────────

def criterion_1(tag, sample):
    say("## Criterion 1: a failed model still answers, never AI")
    say("Target: 9 of 9 return 200, degraded, matching model_status; 0 labelled AI\n")
    expected = {"crash": "error", "nan": "bad_score", "range": "bad_score"}
    passed = 0
    for fault, want in expected.items():
        with Service(fault):
            for i in range(3):
                code, data, secs = post("/submit", {"text": sample[i], "creator_id": f"{tag}_c1_{fault}_{i}"})
                ok = (code == 200 and data.get("degraded") is True
                      and data.get("model_status") == want and data.get("guess") != "ai")
                passed += ok
                say(f"- {fault} #{i + 1}: {code} {'PASS' if ok else 'FAIL'} {short(data)}")
    say(f"\nResult: {passed}/9\n")
    return f"{passed}/9", passed == 9


def criterion_2(tag, sample):
    say("## Criterion 2: every request leaves a log line with its timing")
    say("Target: 20 of 20 have exactly one log line with the right fields, duration_ms within 100 ms of the client\n")
    sent = []  # (creator_id, kind, client_ms)
    before = len(log_lines())

    with Service(""):
        for i in range(10):
            cid = f"{tag}_c2_normal_{i}"
            code, data, secs = post("/submit", {"text": sample[i], "creator_id": cid})
            sent.append((cid, "result", secs * 1000))
        bad = [{}, {"text": ""}, {"text": "Too short."}, {"text": "   "}, {"text": "Also short."}]
        for i, body in enumerate(bad):
            cid = f"{tag}_c2_bad_{i}"
            code, data, secs = post("/submit", {**body, "creator_id": cid})
            sent.append((cid, "rejected", secs * 1000))
    with Service("crash"):
        for i in range(5):
            cid = f"{tag}_c2_crash_{i}"
            code, data, secs = post("/submit", {"text": sample[i], "creator_id": cid})
            sent.append((cid, "result", secs * 1000))

    new = [json.loads(line) for line in log_lines()[before:]]
    passed = 0
    for cid, kind, client_ms in sent:
        mine = [e for e in new if e.get("creator_id") == cid]
        e = mine[0] if mine else {}
        fields = "timestamp" in e and "duration_ms" in e and (
            ("model_status" in e and "text_chars" in e) if kind == "result" else "reason" in e
        )
        gap = abs(client_ms - e.get("duration_ms", -10_000))
        ok = len(mine) == 1 and fields and gap <= 100
        passed += ok
        say(f"- {cid}: {len(mine)} line(s), client {client_ms:.0f} ms, log {e.get('duration_ms')} ms, "
            f"gap {gap:.0f} ms {'PASS' if ok else 'FAIL'}")
    say("\nTwo of the log lines, as written:\n")
    say("```")
    for e in (new[1], new[10]) if len(new) > 10 else new[:2]:
        say(json.dumps(e, ensure_ascii=False))
    say("```")
    say(f"\nResult: {passed}/20\n")
    return f"{passed}/20", passed == 20


def criterion_3(tag, sample):
    say("## Criterion 3: after 3 failures, answers come straight back")
    say("Target: next 5 are 'skipped' in under 1 s, and the model is tried again after 60 s\n")
    with Service("hang"):
        for i in range(3):
            code, data, secs = post("/submit", {"text": sample[i], "creator_id": f"{tag}_c3_fail_{i}"})
            say(f"- failure #{i + 1}: {code} {data.get('model_status')} in {secs:.2f} s")
        skip_started = time.monotonic()
        passed = 0
        for i in range(5):
            code, data, secs = post("/submit", {"text": sample[i], "creator_id": f"{tag}_c3_skip_{i}"})
            ok = code == 200 and data.get("model_status") == "skipped" and secs < 1
            passed += ok
            say(f"- next #{i + 1}: {code} {data.get('model_status')} in {secs:.3f} s {'PASS' if ok else 'FAIL'}")
        time.sleep(max(0, 61 - (time.monotonic() - skip_started)))
        code, data, secs = post("/submit", {"text": sample[5], "creator_id": f"{tag}_c3_retry"})
        retried = code == 200 and data.get("model_status") == "timeout"
        say(f"- 61 s later: {code} {data.get('model_status')} in {secs:.2f} s "
            f"{'PASS (model tried again)' if retried else 'FAIL'}")
        say(f"\nLast response: {short(data)}")
    say(f"\nResult: {passed}/5 skipped, retry {'yes' if retried else 'no'}\n")
    return f"{passed}/5, retried" if retried else f"{passed}/5, no retry", passed == 5 and retried


def criterion_4(tag, sample, content_id):
    say("## Criterion 4: a result that can't be saved is never handed out")
    say("Target: 6 of 6 return 503 log_unavailable, no label or under_review, log unchanged\n")
    with Service("log"):
        before = len(log_lines())
        passed = 0
        for i in range(5):
            code, data, secs = post("/submit", {"text": sample[i], "creator_id": f"{tag}_c4_{i}"})
            ok = code == 503 and data.get("error") == "log_unavailable" and "label" not in data
            passed += ok
            say(f"- submit #{i + 1}: {code} {'PASS' if ok else 'FAIL'} {short(data)}")
        code, data, secs = post("/appeal", {"content_id": content_id, "reasoning": "I wrote this myself."})
        ok = code == 503 and data.get("error") == "log_unavailable" and data.get("status") != "under_review"
        passed += ok
        say(f"- appeal on {content_id}: {code} {'PASS' if ok else 'FAIL'} {short(data)}")
        after = len(log_lines())
    unchanged = after == before
    say(f"- log lines before {before}, after {after}: {'unchanged' if unchanged else 'CHANGED'}")
    say(f"\nResult: {passed}/6, log {'unchanged' if unchanged else 'changed'}\n")
    return f"{passed}/6" + ("" if unchanged else ", log changed"), passed == 6 and unchanged


def criterion_5(tag, sample):
    say("## Criterion 5: many writers at once while the model is stuck")
    say("Target: after a warm-up, 8 of 8 sent at once return 200 style-only in 12 s or less\n")
    with Service("hang"):
        code, data, secs = post("/submit", {"text": sample[0], "creator_id": f"{tag}_c5_warmup"})
        say(f"- warm-up: {code} {data.get('model_status')} in {secs:.2f} s (loads the model, not counted)")
        results = [None] * 8
        go = threading.Event()

        def one(i):
            go.wait()
            results[i] = post("/submit", {"text": sample[i % len(sample)], "creator_id": f"{tag}_c5_{i}"})

        threads = [threading.Thread(target=one, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        go.set()
        for t in threads:
            t.join()
        passed = 0
        for i, (code, data, secs) in enumerate(results):
            ok = code == 200 and data.get("degraded") is True and secs <= 12
            passed += ok
            say(f"- writer {i + 1}: {code} {data.get('model_status')} in {secs:.2f} s {'PASS' if ok else 'FAIL'}")
    say(f"\nResult: {passed}/8\n")
    return f"{passed}/8", passed == 8


# ── Run ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--trial", type=int, required=True)
    args = parser.parse_args()

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    tag = f"t{args.trial}_{datetime.now().strftime('%H%M')}"
    sample = texts()
    say(f"# Capstone trial {args.trial} ({stamp})\n")
    say(f"creator_id prefix for this trial: `{tag}`\n")

    rows = [
        ("1. Failed model still answers, never AI", "9 of 9", *criterion_1(tag, sample)),
        ("2. Every request logged with its timing", "20 of 20", *criterion_2(tag, sample)),
    ]
    # Criterion 4 appeals a result saved earlier in this trial.
    saved_id = next(
        json.loads(line)["content_id"] for line in reversed(log_lines())
        if f'"{tag}_c2_normal_0"' in line
    )
    rows.append(("3. After 3 failures, answers come straight back", "5 of 5 + retry", *criterion_3(tag, sample)))
    rows.append(("4. Unsaved result never handed out", "6 of 6", *criterion_4(tag, sample, saved_id)))
    rows.append(("5. 8 writers at once while the model hangs", "8 of 8", *criterion_5(tag, sample)))

    say("## Summary\n")
    say("| Criterion | Target | Result | Met? |")
    say("|---|---|---|---|")
    for name, target, result, met in rows:
        say(f"| {name} | {target} | {result} | {'yes' if met else 'NO'} |")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"capstone_{stamp}_trial{args.trial}.md"
    path.write_text("\n".join(OUT) + "\n", encoding="utf-8")
    print(f"\nSaved to {path}")


if __name__ == "__main__":
    main()
