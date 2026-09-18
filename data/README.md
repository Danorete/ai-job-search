# Support Score data extracts

Target outputs for the partner communication app:

| File | Status |
| --- | --- |
| `symptom_weights.csv` | not yet produced |
| `phase_multipliers.csv` | not yet produced |
| `strategies.csv` | not yet produced |
| `SOURCES.md` | not yet produced |
| `validate.py` | done and tested |

## Why the CSVs are absent

Extraction is blocked on source URLs. The brief supplied two placeholders
rather than repository links. The two org pages that did come through were
enumerated in full and neither contains any file mentioning endometriosis or
PCOS/PMOS:

* `github.com/Open-Athena` (47 repositories) is machine learning
  infrastructure plus genomic and protein language models.
* `github.com/Biohub` (12 repositories) is protein models, CryoET, and
  immunology.
* `github.com/czbiohub-sf` (131 repositories) was also checked in case it was
  the intended Biohub. Single cell transcriptomics and microscopy.

No rows were generated, because with no sources every row would be an
invented number carrying a `source_file` value pointing at a file that does
not exist. Real source URLs are needed before Step 2 can run.

## validate.py

Loads all three CSVs with pandas and checks that required columns exist and
are non empty, that prevalence and impact fall in 0 to 1, that weight equals
prevalence times impact, that multipliers are plausible, that `cycle_phase`,
`score_band`, and `evidence_level` use only the allowed vocabulary, and that
every row carries provenance. Prints a row count by condition and a count of
rows flagged ASSUMPTION. Exits non zero on any failure.

```
python3 data/validate.py
```

Requires pandas.
