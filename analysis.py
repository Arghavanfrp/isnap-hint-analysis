"""Reproduce the session-level iSnap analysis used in the dissertation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu


TASK_NAME = "guess1Lab"
USE_COLUMNS = [
    "Anon Student Id",
    "Session Id",
    "Duration (sec)",
    "Student Response Type",
    "Problem Name",
    "Action",
]
MEASURES = [
    "n_events",
    "aggregated_recorded_duration_sec",
    "n_run_actions",
    "n_block_grabbed",
    "n_block_snapped",
    "n_input_edits",
    "n_recorded_errors",
    "n_category_changes",
]


def build_session_summary(dataset_path: Path) -> tuple[pd.DataFrame, dict]:
    events = pd.read_csv(
        dataset_path,
        sep="\t",
        usecols=USE_COLUMNS,
        low_memory=False,
    )
    events["Duration (sec)"] = pd.to_numeric(
        events["Duration (sec)"], errors="coerce"
    )
    task_events = events.loc[events["Problem Name"].eq(TASK_NAME)].copy()

    sessions = task_events.groupby("Session Id").agg(
        anon_student_id=("Anon Student Id", "first"),
        n_events=("Session Id", "size"),
        aggregated_recorded_duration_sec=("Duration (sec)", "sum"),
        n_hint_requests=(
            "Student Response Type",
            lambda values: values.eq("HINT_REQUEST").sum(),
        ),
        n_run_actions=("Action", lambda values: values.eq("Block.clickRun").sum()),
        n_block_grabbed=("Action", lambda values: values.eq("Block.grabbed").sum()),
        n_block_snapped=("Action", lambda values: values.eq("Block.snapped").sum()),
        n_input_edits=("Action", lambda values: values.eq("InputSlot.edited").sum()),
        n_recorded_errors=("Action", lambda values: values.eq("Error").sum()),
        n_category_changes=(
            "Action",
            lambda values: values.eq("IDE.changeCategory").sum(),
        ),
    ).reset_index()
    sessions["has_hint"] = sessions["n_hint_requests"].gt(0)
    sessions["group"] = sessions["has_hint"].map(
        {False: "Non-hint", True: "Hint"}
    )

    grouped = sessions.groupby("group")[MEASURES]
    tests = {}
    for measure in MEASURES:
        non_hint = sessions.loc[~sessions["has_hint"], measure]
        hint = sessions.loc[sessions["has_hint"], measure]
        result = mannwhitneyu(hint, non_hint, alternative="two-sided")
        tests[measure] = {
            "u_statistic": float(result.statistic),
            "p_value": float(result.pvalue),
        }

    summary = {
        "task": TASK_NAME,
        "task_event_count": int(len(task_events)),
        "session_count": int(len(sessions)),
        "learner_count": int(task_events["Anon Student Id"].nunique()),
        "hint_request_count": int(sessions["n_hint_requests"].sum()),
        "group_counts": {
            key: int(value) for key, value in sessions["group"].value_counts().items()
        },
        "means": grouped.mean().to_dict(orient="index"),
        "medians": grouped.median().to_dict(orient="index"),
        "mann_whitney_u": tests,
    }
    return sessions, summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create the iSnap guess1Lab session-level analysis."
    )
    parser.add_argument("dataset", type=Path, help="Path to the tab-separated dataset")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Output directory (default: outputs)",
    )
    args = parser.parse_args()

    if not args.dataset.is_file():
        parser.error(f"Dataset not found: {args.dataset}")

    sessions, summary = build_session_summary(args.dataset)
    private_dir = args.output_dir / "private"
    private_dir.mkdir(parents=True, exist_ok=True)
    sessions.to_csv(private_dir / "session_summary_guess1lab.csv", index=False)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
