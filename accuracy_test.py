import os
import sys
import numpy as np
from PIL import Image

# Add current directory to sys.path to import from 'api'
sys.path.append(os.path.abspath('.'))

# Mock Django settings if needed
class MockSettings:
    MEDIA_ROOT = os.path.join(os.path.abspath('.'), "media")
sys.modules["django.conf"] = type("obj", (object,), {"settings": MockSettings()})

from api.pathology_engine import DentalPathologyEngine
from api.vision_model import QuantumVisionModel

def run_accuracy_test():
    test_base = r"C:\Users\bharg\OneDrive\Desktop\DRUGDOSAGEAPP\final_dataset\xray\test"
    categories = {
        "Caries": "Dental Caries",
        "Impacted teeth": "Impacted Tooth",
        "Healthy Teeth": "Healthy Teeth"
    }

    total_samples = 0
    correct_samples = 0
    
    # Metrics per class
    class_stats = {cat: {"tp": 0, "fn": 0, "total": 0} for cat in categories.values()}

    print(f"--- AI ACCURACY TEST SUITE: Aria Quantum v63.6 ---")
    
    for folder, expected_cond in categories.items():
        folder_path = os.path.join(test_base, folder)
        if not os.path.exists(folder_path):
            print(f"Warning: Folder {folder_path} not found.")
            continue
            
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Processing {folder}: {len(files)} images...")
        
        for f in files:
            img_path = os.path.join(folder_path, f)
            total_samples += 1
            class_stats[expected_cond]["total"] += 1
            
            # 1. Vision Model Pre-check
            try:
                vision = QuantumVisionModel.predict_image_nature(img_path)
                if vision["label"] not in ["DENTAL_XRAY", "INTRAORAL_PHOTO"]:
                    is_correct = False
                else:
                    # 2. Pathology Analysis
                    diag = DentalPathologyEngine.analyze_xray(img_path)
                    issues = diag.get("issues", [])
                    
                    if expected_cond == "Healthy Teeth":
                        # If ground truth is Healthy, we expect no issues detected
                        is_correct = (len(issues) == 0)
                    else:
                        # Check if the expected condition is among the findings
                        found_conditions = [i["condition"] for i in issues]
                        is_correct = (expected_cond in found_conditions)
            except Exception as e:
                print(f"Error processing {f}: {e}")
                is_correct = False
            
            if is_correct:
                correct_samples += 1
                class_stats[expected_cond]["tp"] += 1
            else:
                class_stats[expected_cond]["fn"] += 1

    overall_accuracy = (correct_samples / total_samples) * 100 if total_samples > 0 else 0
    
    print("\n" + "="*40)
    print("        PERFORMANCE SUMMARY")
    print("="*40)
    print(f"{'Condition':<20} | {'Total':<6} | {'Correct':<8} | {'Recall'}")
    print("-" * 55)
    
    for cat, stats in class_stats.items():
        recall = (stats["tp"] / (stats["tp"] + stats["fn"])) * 100 if (stats["tp"] + stats["fn"]) > 0 else 0
        print(f"{cat:<20} | {stats['total']:<6} | {stats['tp']:<8} | {recall:.2f}%")

    print("-" * 55)
    print(f"OVERALL AI ACCURACY: {overall_accuracy:.2f}%")
    print("="*40)
    
    # Write result to a file for easy reading
    with open("accuracy_report.txt", "w") as rf:
        rf.write(f"Overall Accuracy: {overall_accuracy:.2f}%\n\n")
        rf.write(f"{'Condition':<20} | {'Total':<6} | {'Correct':<8} | {'Recall'}\n")
        rf.write("-" * 55 + "\n")
        for cat, stats in class_stats.items():
            recall = (stats["tp"] / (stats["tp"] + stats["fn"])) * 100 if (stats["tp"] + stats["fn"]) > 0 else 0
            rf.write(f"{cat:<20} | {stats['total']:<6} | {stats['tp']:<8} | {recall:.2f}%\n")

if __name__ == "__main__":
    run_accuracy_test()
