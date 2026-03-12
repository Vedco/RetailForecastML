import json

with open("reports/drift_summary.json") as f:
    drift = json.load(f)

drift_detected = drift.get("data_drift_detected", False) or drift.get("concept_drift_detected", False)

with open("drift_result.txt", "w") as f:
    if drift_detected:
        f.write("true")
        print("Drift detected! Retrain triggered.")
    else:
        f.write("false")
        print("No drift detected; skipping retrain.")

