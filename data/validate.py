#!/usr/bin/env python3
"""Validate the three Support Score CSV extracts.

Checks, for each file:
  * every required column exists
  * no required cell is empty
  * numeric fields fall in valid ranges
  * categorical fields use only allowed vocabulary
  * every row carries provenance (source_repo and source_file)
Then prints a summary count by condition.

Exit status is 0 when everything passes, 1 otherwise.
"""

import sys
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent

SCHEMA = {
    "symptom_weights.csv": [
        "condition", "symptom", "prevalence", "impact", "weight",
        "source_repo", "source_file", "notes",
    ],
    "phase_multipliers.csv": [
        "condition", "cycle_phase", "day_range", "multiplier",
        "source_repo", "source_file", "notes",
    ],
    "strategies.csv": [
        "condition", "symptom", "strategy", "partner_action", "score_band",
        "evidence_level", "source_repo", "source_file",
    ],
}

# "notes" may legitimately be blank; everything else must be filled.
OPTIONAL = {"notes"}

ALLOWED_PHASES = {"menstrual", "follicular", "ovulatory", "luteal"}
ALLOWED_BANDS = {"steady", "heads up", "hard"}
ALLOWED_EVIDENCE = {"high", "moderate", "low"}

errors = []
warnings = []
frames = {}


def fail(filename, message):
    errors.append(f"[{filename}] {message}")


def warn(filename, message):
    warnings.append(f"[{filename}] {message}")


def load(filename, columns):
    path = DATA_DIR / filename
    if not path.exists():
        fail(filename, "file is missing")
        return None
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)

    missing = [c for c in columns if c not in frame.columns]
    if missing:
        fail(filename, f"missing required columns: {', '.join(missing)}")
        return None
    extra = [c for c in frame.columns if c not in columns]
    if extra:
        warn(filename, f"unexpected extra columns: {', '.join(extra)}")
    if frame.empty:
        fail(filename, "file has a header but no data rows")
        return frame

    for column in columns:
        if column in OPTIONAL:
            continue
        blank = frame[frame[column].astype(str).str.strip() == ""]
        if not blank.empty:
            rows = ", ".join(str(i + 2) for i in blank.index[:10])
            fail(filename, f"column '{column}' is empty on row(s) {rows}")
    return frame


def numeric(frame, filename, column, low, high):
    """Return the column as floats, recording any unparseable or out of range values."""
    values = pd.to_numeric(frame[column], errors="coerce")
    bad = frame[values.isna()]
    if not bad.empty:
        rows = ", ".join(str(i + 2) for i in bad.index[:10])
        fail(filename, f"column '{column}' is not numeric on row(s) {rows}")
    out = frame[(values < low) | (values > high)]
    if not out.empty:
        rows = ", ".join(str(i + 2) for i in out.index[:10])
        fail(filename, f"column '{column}' outside {low} to {high} on row(s) {rows}")
    return values


def check_vocabulary(frame, filename, column, allowed):
    seen = frame[column].astype(str).str.strip().str.lower()
    bad = sorted(set(seen) - allowed)
    if bad:
        fail(filename, f"column '{column}' has unrecognised value(s): {', '.join(bad)}")


# symptom_weights.csv
weights = load("symptom_weights.csv", SCHEMA["symptom_weights.csv"])
if weights is not None and not weights.empty:
    prevalence = numeric(weights, "symptom_weights.csv", "prevalence", 0.0, 1.0)
    impact = numeric(weights, "symptom_weights.csv", "impact", 0.0, 1.0)
    weight = numeric(weights, "symptom_weights.csv", "weight", 0.0, 1.0)
    product = (prevalence * impact - weight).abs()
    mismatched = weights[product > 0.005]
    if not mismatched.empty:
        rows = ", ".join(str(i + 2) for i in mismatched.index[:10])
        fail("symptom_weights.csv",
             f"weight does not equal prevalence times impact on row(s) {rows}")
    duplicates = weights.duplicated(subset=["condition", "symptom", "source_file"])
    if duplicates.any():
        warn("symptom_weights.csv",
             f"{int(duplicates.sum())} duplicate condition/symptom/source_file row(s)")
    frames["symptom_weights.csv"] = weights

# phase_multipliers.csv
phases = load("phase_multipliers.csv", SCHEMA["phase_multipliers.csv"])
if phases is not None and not phases.empty:
    numeric(phases, "phase_multipliers.csv", "multiplier", 0.1, 5.0)
    check_vocabulary(phases, "phase_multipliers.csv", "cycle_phase", ALLOWED_PHASES)
    for condition, group in phases.groupby("condition"):
        covered = set(group["cycle_phase"].str.strip().str.lower())
        gaps = sorted(ALLOWED_PHASES - covered)
        if gaps:
            warn("phase_multipliers.csv",
                 f"condition '{condition}' has no row for: {', '.join(gaps)}")
    frames["phase_multipliers.csv"] = phases

# strategies.csv
strategies = load("strategies.csv", SCHEMA["strategies.csv"])
if strategies is not None and not strategies.empty:
    check_vocabulary(strategies, "strategies.csv", "score_band", ALLOWED_BANDS)
    check_vocabulary(strategies, "strategies.csv", "evidence_level", ALLOWED_EVIDENCE)
    frames["strategies.csv"] = strategies

# Summary
print("=" * 60)
print("SUPPORT SCORE DATA VALIDATION")
print("=" * 60)

for filename in SCHEMA:
    frame = frames.get(filename)
    if frame is None:
        print(f"\n{filename}: not loaded")
        continue
    print(f"\n{filename}: {len(frame)} row(s)")
    for condition, count in frame["condition"].value_counts().items():
        print(f"    {condition}: {count}")
    if "notes" in frame.columns:
        assumptions = frame["notes"].astype(str).str.contains("ASSUMPTION", case=False).sum()
        if assumptions:
            print(f"    rows flagged ASSUMPTION: {int(assumptions)}")

if warnings:
    print("\nWARNINGS")
    for line in warnings:
        print(f"  ! {line}")

print()
if errors:
    print(f"FAILED with {len(errors)} error(s):")
    for line in errors:
        print(f"  x {line}")
    sys.exit(1)

print("PASSED: all checks clean.")
