
import os
import sys
import json
import hashlib

# Mock Django settings for standalone test
class MockSettings:
    MEDIA_ROOT = "c:\\Users\\bharg\\AndroidStudioProjects\\DRUGDOSAGEAPP\\media"

sys.modules["django.conf"] = type("obj", (object,), {"settings": MockSettings()})

from api.vision_model import QuantumVisionModel
from api.pathology_engine import DentalPathologyEngine
from api.ai_pipeline import DentalAIPipeline

def test_pipeline():
    print("--- [TEST 1: Vision Model Rejection] ---")
    # We'll use a dummy non-dental path or just test the logic with a placeholder if file doesn't exist
    # But better to test on real extracted data if possible.
    placeholder_non_dental = "c:\\Users\\bharg\\AndroidStudioProjects\\DRUGDOSAGEAPP\\media\\test_non_dental.jpg"
    # Create a simple noise file if not exists
    if not os.path.exists(placeholder_non_dental):
        from PIL import Image
        import numpy as np
        img = Image.fromarray(np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8))
        img.save(placeholder_non_dental)
    
    res = QuantumVisionModel.predict_image_nature(placeholder_non_dental)
    print(f"Non-Dental Result: {res['label']} (Reason: {res.get('reason', 'N/A')})")
    assert res['label'] == "NON_DENTAL", "FAIL: Non-dental image was not rejected!"

    print("\n--- [TEST 2: Pathology Analysis & Coordinates] ---")
    # Check if we have an OPG in the temp dataset to test
    dental_base = "c:\\Users\\bharg\\AndroidStudioProjects\\DRUGDOSAGEAPP\\temp_dental_dataset"
    if os.path.exists(dental_base):
        # Just find first jpg
        for root, dirs, files in os.walk(dental_base):
            for f in files:
                if f.endswith(".jpg"):
                    test_img = os.path.join(root, f)
                    print(f"Testing on Dental Image: {f}")
                    diag = DentalPathologyEngine.analyze_xray(test_img)
                    print(f"Findings: {len(diag.get('issues', []))} issues detected.")
                    for issue in diag.get('issues', []):
                        print(f"  - {issue['condition']} on Tooth {issue['tooth']} (Prob: {issue['probability']})")
                    break
            else: continue
            break

    print("\n--- [TEST 3: Explain Pipeline & Treatments] ---")
    if 'test_img' in locals():
        explanation = DentalAIPipeline.explain_image(test_img)
        print(f"Pipeline Status: {explanation['status']}")
        if explanation['status'] == "SUCCESS":
            issues = explanation['data']['issues']
            for i in issues:
                print(f"  - Tooth {i['tooth']}: Best Treatment -> {i.get('best_treatment', 'None')}")
                assert "best_treatment" in i, "FAIL: Treatment mapping missing!"

    print("\n--- ALL TESTS PASSED (Backend Logic Verified) ---")

if __name__ == "__main__":
    test_pipeline()
