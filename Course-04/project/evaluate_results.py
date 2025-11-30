"""Evaluation script for multi-agent system results.
Parses test_results.csv and validates rubric conditions:
- At least 3 requests change cash balance
- At least 3 fulfilled (heuristic: contains 'Sale Processed Successfully' or 'Quote' keywords)
- Not all fulfilled (presence of 'not found', 'cannot be fulfilled', or 'ERROR')
Outputs JSON summary to eval_report.json.
"""
from __future__ import annotations
import pandas as pd
import json
import re
from pathlib import Path

RESULTS_FILE = Path("test_results.csv")
OUTPUT_FILE = Path("eval_report.json")

FULFILL_PATTERNS = [
    re.compile(r"Sale Processed Successfully", re.I),
    re.compile(r"Quote prepared", re.I),
    re.compile(r"Final Price", re.I),
]
UNFULFILLED_PATTERNS = [
    re.compile(r"cannot be fulfilled", re.I),
    re.compile(r"not found", re.I),
    re.compile(r"ERROR", re.I),
    re.compile(r"out of stock", re.I),
]


def classify_response(text: str) -> dict:
    fulfilled = any(p.search(text) for p in FULFILL_PATTERNS)
    unfulfilled = any(p.search(text) for p in UNFULFILLED_PATTERNS)
    return {"fulfilled": fulfilled, "unfulfilled": unfulfilled}


def main():
    if not RESULTS_FILE.exists():
        raise SystemExit("test_results.csv not found. Run multi_agent_system.py first.")
    df = pd.read_csv(RESULTS_FILE)
    if df.empty:
        raise SystemExit("test_results.csv is empty.")

    # Ensure numeric changes by tracking previous row
    cash_changes = 0
    prev_cash = None
    fulfilled_count = 0
    unfulfilled_count = 0

    row_summaries = []
    for _, row in df.iterrows():
        response = str(row.get("response", ""))
        metrics = classify_response(response)
        if prev_cash is not None and float(row["cash_balance"]) != prev_cash:
            cash_changes += 1
        prev_cash = float(row["cash_balance"])
        if metrics["fulfilled"]:
            fulfilled_count += 1
        if metrics["unfulfilled"]:
            unfulfilled_count += 1
        row_summaries.append({
            "request_id": int(row["request_id"]),
            "cash_balance": float(row["cash_balance"]),
            "inventory_value": float(row["inventory_value"]),
            "fulfilled": metrics["fulfilled"],
            "unfulfilled": metrics["unfulfilled"],
        })

    total_requests = len(df)
    rubric = {
        "cash_changes": cash_changes,
        "fulfilled_requests": fulfilled_count,
        "unfulfilled_requests": unfulfilled_count,
        "total_requests": total_requests,
        "criteria": {
            "min_3_cash_changes": cash_changes >= 3,
            "min_3_fulfilled": fulfilled_count >= 3,
            "not_all_fulfilled": unfulfilled_count > 0 and fulfilled_count < total_requests,
        }
    }

    output = {"rubric_evaluation": rubric, "details": row_summaries}
    OUTPUT_FILE.write_text(json.dumps(output, indent=2))
    print("Evaluation written to eval_report.json")
    print(json.dumps(rubric, indent=2))

if __name__ == "__main__":
    main()

