import os
import cv2
import numpy as np
from api.pathology_engine import DentalPathologyEngine

def verify_accuracy():
    test_path = r"c:\Users\bharg\AndroidStudioProjects\DRUGDOSAGEAPP\final_dataset\xray\test"
    
    test_cases = {
        "Caries": "Dental Caries",
        "Impacted teeth": "Impacted Tooth",
        "Healthy Teeth": "Healthy Teeth"
    }

    results = {k: {"pass": 0, "fail": 0} for k in test_cases.keys()}

    print("--- v21.0 Precision Verification ---")
    for cat_name, expected_label in test_cases.items():
        cat_path = os.path.join(test_path, cat_name)
        if not os.path.exists(cat_path): continue
        
        files = [f for f in os.listdir(cat_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Testing {cat_name} ({len(files)} images)...")
        
        for f in files[:50]: # Test 50 per category
            img_path = os.path.join(cat_path, f)
            res = DentalPathologyEngine.analyze_xray(img_path)
            
            actual_label = res.get("label", "Unknown")
            
            # For Caries/Impacted, we check if the expected condition is present in any issue
            if expected_label == "Healthy Teeth":
                if actual_label == "Healthy Teeth": results[cat_name]["pass"] += 1
                else: 
                    print(f"FAIL: {f} expected Healthy but got {actual_label}")
                    results[cat_name]["fail"] += 1
            else:
                found = any(expected_label in issue["condition"] for issue in res.get("issues", []))
                if found: results[cat_name]["pass"] += 1
                else: 
                    print(f"FAIL: {f} expected {expected_label} but found {res.get('issues')}")
                    results[cat_name]["fail"] += 1

    total_accuracy = 0
    for cat, stat in results.items():
        acc = (stat["pass"] / (stat["pass"] + stat["fail"])) * 100 if (stat["pass"] + stat["fail"]) > 0 else 0
        print(f"{cat}: {acc:.1f}% Accuracy ({stat['pass']} Pass, {stat['fail']} Fail)")
        total_accuracy += acc
    
    print(f"\nFinal Precision Score: {total_accuracy / 3:.1f}%")

if __name__ == "__main__":
    verify_accuracy()
