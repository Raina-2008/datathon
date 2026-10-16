"""Re-computes every number quoted in the apps and README.
Run from the repo root:  pip install pandas   then   python analysis/facts.py
"""
import pandas as pd
from pathlib import Path
D = Path(__file__).resolve().parent.parent / "data"
p, e = pd.read_csv(D/"patients.csv"), pd.read_csv(D/"encounters.csv")
d, t = pd.read_csv(D/"departments.csv"), pd.read_csv(D/"diagnostic_tests.csv")

m = e.merge(p, on="patient_id").merge(d, on="department_id")
print(f"Rows: patients={len(p)}, encounters={len(e)}, departments={len(d)}, tests={len(t)}")
print("\n-- Data quality --")
print("duplicate encounter ids:", e.encounter_id.duplicated().sum())
print("negative waits:", (e.wait_minutes < 0).sum())
print("tests not linked to an encounter:", (~t.encounter_id.isin(e.encounter_id)).sum())
print("patients with no chronic_condition recorded:", p.chronic_condition.isna().sum())

print("\n-- Waiting --")
print(f"average wait {e.wait_minutes.mean():.1f} min, median {e.wait_minutes.median():.0f}, 90th percentile {e.wait_minutes.quantile(.9):.0f}, max {e.wait_minutes.max()}")
print("average wait by triage:", e.groupby("triage_level").wait_minutes.mean().round(1).to_dict())
print("average wait by department:", m.groupby("department_name").wait_minutes.mean().round(1).sort_values().to_dict())
print("average wait by visit type:", e.groupby("visit_type").wait_minutes.mean().round(1).to_dict())

print("\n-- Forgotten patients (Low/Medium triage, wait > 90 min) --")
f = e[e.triage_level.isin(["Low", "Medium"]) & (e.wait_minutes > 90)]
print(f"{len(f)} visits ({len(f)/len(e):.1%} of all visits)")
print("left before care overall:", f"{(e.outcome=='Left before care').mean():.1%}", "| among forgotten:", f"{(f.outcome=='Left before care').mean():.1%}")

print("\n-- Waits beyond what triage explains (department level) --")
e["excess"] = e.wait_minutes - e.groupby("triage_level").wait_minutes.transform("mean")
sd = (e.excess**2).mean() ** .5
g = e.merge(d, on="department_id").groupby("department_name").excess.agg(["mean", "size"])
g["z"] = g["mean"] / (sd / g["size"] ** .5)
print(g.round(1).sort_values("z", ascending=False).to_string())

print("\n-- Diagnostic tests --")
t["tat"] = (pd.to_datetime(t.completion_time) - pd.to_datetime(t.requested_time)).dt.total_seconds() / 60
print(f"average turnaround {t.tat.mean():.0f} min, median {t.tat.median():.0f}")
print("by test type:", t.groupby("test_type").tat.mean().round(0).to_dict())
print("by priority:", t.groupby("priority").tat.mean().round(0).to_dict())
