# Support Score data extracts

Data behind the partner communication app's Support Score formula.

| File | Rows | Purpose |
| --- | --- | --- |
| `symptom_weights.csv` | 16 | Per symptom prevalence, impact and weight |
| `phase_multipliers.csv` | 8 | Cycle phase adjustment per condition |
| `strategies.csv` | 10 | Comfort strategies rewritten as partner actions |
| `SOURCES.md` | | Licences, derivations, assumptions, gaps |
| `build.py` | | Regenerates all three CSVs from verified source values |
| `validate.py` | | Schema, range and provenance checks |

```
python3 data/build.py      # regenerate
python3 data/validate.py   # check
```

Both require pandas for validation; `build.py` uses only the standard library.

## Sources

Three peer reviewed studies. The first two are CC BY 4.0. The third is CC
BY-NC, which makes the combined dataset non commercial only until the PMOS
rows are re-sourced. See `SOURCES.md`.

* Volpi and Konig (2026), Women's Health 22, doi:10.1177/17455057261462827
* Armour et al. (2019), BMC Complement Altern Med 19:17, doi:10.1186/s12906-019-2431-x
* Begum et al. (2024), Future Science OA 10(1):2430878, doi:10.1080/20565623.2024.2430878 (CC BY-NC)

Every derivation is documented in `SOURCES.md` and implemented in `build.py`
rather than done by hand, so the arithmetic is auditable.

## Known limits

Read `SOURCES.md` before presenting any of this. In short: there is no PMOS
data for cycle phases or strategies, most symptom weights describe people in
general rather than endometriosis specifically, and two of the four cycle
phases reuse a value because the source measured three phases rather than
four.
