#!/usr/bin/env python3
"""
Criterion 4, the appeal path, three times.  <- UNIT 8, MILESTONE 3

    python app.py                                # in one terminal
    python eval_appeals.py --label before        # in another

run_eval.py only sends /submit, and an appeal needs a real content_id first,
so this does both: per trial it submits 10 texts, appeals each content_id,
then reads GET /log to check every appeal landed as `under_review`. It also
appeals a made-up content_id and records what came back and what the log
gained.

Like run_eval.py, it records; the verdict is mine to write.
"""

import argparse
import datetime as dt
import json
import sys

import config
import scenarios

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

# Any valid text will do — the point is getting real content_ids.
TEXTS = (scenarios.CLEAR_AI + next(
    s["texts"] for s in scenarios.SCENARIOS if s["name"] == "label coverage"
))[:9] + [scenarios.CLEAR_AI[1]]


def run_trial(requests, url, trial, timeout):
    appealed = []
    for i, text in enumerate(TEXTS, 1):
        sub = requests.post(f"{url}/submit", timeout=timeout,
                            json={"text": text, "creator_id": f"eval_appeal_t{trial}_{i}"})
        content_id = sub.json().get("content_id") if sub.ok else None
        app = requests.post(f"{url}/appeal", timeout=timeout, json={
            "content_id": content_id,
            "reasoning": "I wrote this myself.",
        }) if content_id else None
        appealed.append({
            "submit_status": sub.status_code,
            "content_id": content_id,
            "appeal_status": app.status_code if app is not None else None,
            "appeal_response": app.json() if app is not None else None,
        })

    log = requests.get(f"{url}/log", timeout=timeout).json()["entries"]
    for a in appealed:
        a["appeal_in_log_as_under_review"] = any(
            e.get("content_id") == a["content_id"]
            and e.get("event") == "appeal"
            and e.get("status") == "under_review"
            for e in log
        )

    before = len(log)
    unknown = requests.post(f"{url}/appeal", timeout=timeout, json={
        "content_id": f"made-up-id-trial-{trial}",
        "reasoning": "I wrote this myself.",
    })
    after_log = requests.get(f"{url}/log", timeout=timeout).json()["entries"]
    unknown_result = {
        "status": unknown.status_code,
        "response": unknown.json(),
        "log_entries_added": len(after_log) - before,
        "entries_added": after_log[before:],
        "appeal_recorded_for_made_up_id": any(
            e.get("event") == "appeal" and e.get("content_id") == f"made-up-id-trial-{trial}"
            for e in after_log
        ),
    }
    return {"appeals": appealed, "unknown_id": unknown_result}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    import requests

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    trials = []
    for trial in range(1, args.trials + 1):
        result = run_trial(requests, args.url, trial, args.timeout)
        ok = sum(1 for a in result["appeals"]
                 if a["appeal_status"] == 200 and a["appeal_in_log_as_under_review"])
        u = result["unknown_id"]
        print(f"trial {trial}: {ok}/{len(result['appeals'])} appeals recorded · "
              f"made-up id -> {u['status']}, log +{u['log_entries_added']}")
        trials.append(result)

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeals_{stamp}{label}.md"
    lines = [f"# Appeal path (criterion 4){f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `eval_appeals.py::main`",
             "- Service: `app.py::submit`, `app.py::appeal`", ""]
    for n, result in enumerate(trials, 1):
        lines += [f"## Trial {n}", "", "```json", json.dumps(result, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
