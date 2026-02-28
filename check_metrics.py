import json
import os
import sys

# Load new results
with open("output/results/results.json", "r") as f:
    results = json.load(f)
new_r2 = results["R2"]

# Get baseline from GitHub Variable
best_r2 = float(os.getenv("BEST_METRIC", -1.0))

print(f"Current Best R2: {best_r2}")
print(f"New Model R2: {new_r2}")

if new_r2 > best_r2:
    print("Model Improved! Proceeding to deploy.")
    print(f"NEW_METRIC_VALUE={new_r2}") 
    sys.exit(0) # Success
else:
    print("Model did not improve. Stopping.")
    sys.exit(1) # Fail the pipeline