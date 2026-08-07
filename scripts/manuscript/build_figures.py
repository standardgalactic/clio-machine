#!/usr/bin/env python3
"""Generate deterministic manuscript figure data artifacts."""

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "figures" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

rows = [
    ("iteration", "incompatibility"),
    (0, 1.0),
    (1, 0.74),
    (2, 0.51),
    (3, 0.33),
    (4, 0.19),
    (5, 0.11),
]

with (OUT / "incompatibility_decay.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerows(rows)

print(f"Wrote {(OUT / 'incompatibility_decay.csv').relative_to(ROOT)}")
