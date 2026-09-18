#!/usr/bin/env python3
"""Generate the three Support Score CSVs from verified source values.

Every number below was read directly from the source PDFs (see SOURCES.md).
Derivations are done here rather than by hand so the arithmetic is
reproducible and auditable.

Derivation rules
----------------
symptom_weights.csv
    prevalence = 1 - ("symptom does not occur" share), Volpi Table 3
    impact     = mean distress M / 3          (distress is a 0 to 3 scale)
    weight     = prevalence * impact

phase_multipliers.csv
    Volpi reports absolute mean distress per phase on a 0 to 3 scale, not
    multipliers. Multipliers are derived by dividing each phase mean by the
    intermenstrual mean, which is the quietest phase and so serves as
    baseline.

strategies.csv
    prevalence of use and 0 to 10 pain relief come straight from Armour
    Tables (usage list, Table 3, Table 4). Ingestible and pharmacological
    modalities are excluded per project scope.
"""

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent

VOLPI = "Volpi & Konig 2026, Women's Health 22, doi:10.1177/17455057261462827"
VOLPI_F = "volpi-konig-2026-symptoms-and-distress-across-the-menstrual-cycle.pdf"
ARMOUR = "Armour et al. 2019, BMC Complement Altern Med 19:17, doi:10.1186/s12906-019-2431-x"
ARMOUR_F = "s12906-019-2431-x.pdf"


def row(**kw):
    return kw


# ---------------------------------------------------------------- symptoms
# (symptom, share reporting "does not occur", mean distress, phase observed)
VOLPI_SYMPTOMS = [
    ("headache",                      0.36, 1.76, "menstrual"),
    ("fatigue",                       0.35, 1.75, "menstrual"),
    ("concentration difficulties",    0.65, 1.74, "menstrual"),
    ("discomfort due to vaginal bleeding", 0.44, 1.72, "menstrual"),
    ("insomnia",                      0.63, 1.72, "menstrual"),
    ("abdominal pain",                0.13, 1.32, "premenstrual"),
    ("emotional instability",         0.17, 1.25, "premenstrual"),
    ("irritability or anger",         0.20, 1.21, "premenstrual"),
    ("increased need for sleep",      0.27, 1.02, "intermenstrual"),
]

symptom_rows = []
for name, absent, mean_distress, phase in VOLPI_SYMPTOMS:
    prevalence = round(1 - absent, 3)
    impact = round(mean_distress / 3, 3)
    symptom_rows.append(row(
        condition="general menstruating population",
        symptom=name,
        prevalence=prevalence,
        impact=impact,
        weight=round(prevalence * impact, 4),
        source_repo=VOLPI,
        source_file=f"{VOLPI_F} Table 3",
        notes=(f"Whole sample N=336. Values from the {phase} phase, where this "
               f"symptom appears in the paper's top five. Impact = mean distress "
               f"{mean_distress} on a 0 to 3 scale, rescaled to 0 to 1."),
    ))

# Endometriosis subgroup, from the post hoc sensitivity analysis. The paper
# reports subgroup means but no subgroup occurrence rate, so prevalence is
# carried over from the whole sample and flagged.
ENDO = [
    ("abdominal pain", 0.87, 2.12, "menstrual",
     "Comparison group M=1.66. This is the one contrast that did NOT reach "
     "significance (p=.057, d=0.48)."),
    ("pelvic pain", 0.80, 2.07, "intermenstrual",
     "Comparison group M=1.02, d=0.98."),
    ("discomfort due to vaginal bleeding", 0.56, 2.00, "intermenstrual",
     "Comparison group M=0.84, d=1.14."),
]
for name, prev, mean_distress, phase, detail in ENDO:
    impact = round(mean_distress / 3, 3)
    symptom_rows.append(row(
        condition="endometriosis",
        symptom=name,
        prevalence=prev,
        impact=impact,
        weight=round(prev * impact, 4),
        source_repo=VOLPI,
        source_file=f"{VOLPI_F} post hoc sensitivity analysis",
        notes=(f"ASSUMPTION on prevalence: the paper gives no occurrence rate for "
               f"the endometriosis subgroup, so the whole-sample {phase} rate is "
               f"carried over. Impact is measured ({mean_distress}/3). {detail}"),
    ))

# ------------------------------------------------------------------ phases
# Volpi phase means on the 0 to 3 distress scale.
MENSTRUAL, PREMENSTRUAL, INTERMENSTRUAL = 1.41, 1.06, 0.98
BASE = INTERMENSTRUAL

PHASE_MAP = [
    ("menstrual",  "1-5",   MENSTRUAL,      "menstrual",
     "Direct match. Study mean 1.41 (SD 0.62)."),
    ("follicular", "6-13",  INTERMENSTRUAL, "intermenstrual",
     "ASSUMPTION on phase mapping: the study's intermenstrual window covers both "
     "follicular and ovulatory days and does not separate them."),
    ("ovulatory",  "14-15", INTERMENSTRUAL, "intermenstrual",
     "ASSUMPTION on phase mapping: no separate ovulatory measurement exists in "
     "the source; the intermenstrual value is reused."),
    ("luteal",     "16-28", PREMENSTRUAL,   "premenstrual",
     "ASSUMPTION on phase mapping: the study measured a premenstrual window, "
     "which is the late luteal phase only. Applying it to the whole luteal "
     "phase likely overstates days 16 to 22."),
]

phase_rows = []
for phase, days, mean_distress, source_phase, note in PHASE_MAP:
    phase_rows.append(row(
        condition="endometriosis",
        cycle_phase=phase,
        day_range=days,
        multiplier=round(mean_distress / BASE, 3),
        source_repo=VOLPI,
        source_file=f"{VOLPI_F} Research question 2",
        notes=(f"Derived: source '{source_phase}' mean {mean_distress} divided by the "
               f"intermenstrual baseline {BASE}. The source reports absolute distress, "
               f"not multipliers. Phase means are whole sample, but the paper found no "
               f"phase-by-diagnosis interaction (p=.63), so the shape is applied to "
               f"endometriosis while the condition sets the baseline level. {note}"),
    ))

for phase, days, _, _, _ in PHASE_MAP:
    phase_rows.append(row(
        condition="PMOS",
        cycle_phase=phase,
        day_range=days,
        multiplier=1.0,
        source_repo="none",
        source_file="none",
        notes=("ASSUMPTION: no source in this set covers PMOS cycle variation. Set to "
               "1.0 (no clear pattern) as a neutral default. PMOS cycles are frequently "
               "anovulatory, so phase boundaries may not be well defined at all."),
    ))

# -------------------------------------------------------------- strategies
# (strategy, n users, usage share, pain relief 0-10, adverse rate %, common AE,
#  partner action, score band)
STRATEGIES = [
    ("heat", 259, 0.70, 6.5, 15.9, "burns including blistering",
     "Bring a heat pack or patch that holds a controlled temperature, and check "
     "in on the skin underneath. Burns are the most reported downside.",
     "hard"),
    ("rest", 252, 0.68, 5.3, 7.3, "increased fatigue, increased depression",
     "Take tasks off her plate and protect the space to lie down without her "
     "having to ask or justify it.",
     "hard"),
    ("meditation or breathing", 175, 0.47, 4.6, 3.4, "none above threshold",
     "Offer to do a breathing exercise together, and keep the room quiet. "
     "Lowest downside of anything in the survey.",
     "steady"),
    ("massage", 118, 0.32, 5.5, 6.8, "none above threshold",
     "Offer a back or shoulder massage, and follow her direction on pressure "
     "and location.",
     "heads up"),
    ("acupressure", 29, 0.08, 6.3, 7.1, "none above threshold",
     "Ask whether pressure on a specific point helps, and hold it for her.",
     "heads up"),
    ("cold", 18, 0.05, 5.5, 5.6, "none above threshold",
     "Have a cold pack ready as an alternative when heat is not helping.",
     "heads up"),
    ("stretching", 148, 0.40, 4.6, 14.8,
     "increased pelvic pain, increased nausea, increased flare ups",
     "Suggest gentle stretching only, and stop at the first sign it is making "
     "things worse.",
     "steady"),
    ("yoga or Pilates", 131, 0.35, 4.5, 15.9, "increased pelvic pain",
     "Good on steady days. The reported pain increases were linked mostly to "
     "Pilates rather than yoga, so favour yoga.",
     "steady"),
    ("taichi or qigong", 8, 0.02, 4.0, 0.0, "none reported",
     "Offer as a low intensity movement option. No adverse events were reported, "
     "though very few people used it.",
     "steady"),
    ("exercise", 158, 0.42, 4.9, 34.2,
     "increased pelvic pain, increased fatigue, increased flare ups",
     "Do NOT push exercise during a flare up. One in three users reported it "
     "made things worse. Offer it only on steady days, and let her set the pace.",
     "steady"),
]

strategy_rows = []
for (name, n, usage, relief, ae_rate, ae_kind, action, band) in STRATEGIES:
    # Evidence tracks subgroup size: one self-selected survey, so moderate at best.
    evidence = "moderate" if n >= 100 else "low"
    strategy_rows.append(row(
        condition="endometriosis",
        symptom="pelvic pain",
        strategy=(f"{name} (used by {usage:.0%} of respondents; mean pain relief "
                  f"{relief}/10; adverse events {ae_rate}%, {ae_kind})"),
        partner_action=action,
        score_band=band,
        evidence_level=evidence,
        source_repo=ARMOUR,
        source_file=f"{ARMOUR_F} usage list, Table 3, Table 4",
    ))


def write(name, rows, columns):
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {name}: {len(rows)} rows")


write("symptom_weights.csv", symptom_rows,
      ["condition", "symptom", "prevalence", "impact", "weight",
       "source_repo", "source_file", "notes"])
write("phase_multipliers.csv", phase_rows,
      ["condition", "cycle_phase", "day_range", "multiplier",
       "source_repo", "source_file", "notes"])
write("strategies.csv", strategy_rows,
      ["condition", "symptom", "strategy", "partner_action", "score_band",
       "evidence_level", "source_repo", "source_file"])
