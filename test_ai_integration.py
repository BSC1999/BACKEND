import os
import django
from django.conf import settings

# Setup minimalist django environment for testing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.ai_pipeline import DentalAIPipeline
from api.drug_engine import DrugEngine
from api.models import Patient

def run_test():
    test_img = "test_img_1.png"
    if not os.path.exists(test_img):
        print("ERROR: test_img_1.png not found")
        return

    print("--- 1. Testing AI Pipeline (DentalAIPipeline.analyze_image) ---")
    try:
        report = DentalAIPipeline.analyze_image(test_img)
        print("AI Report Output:")
        print(report)
        print("SUCCESS: analyze_image ran perfectly.\n")
    except Exception as e:
        print(f"FAILED analyze_image: {str(e)}")

    print("--- 2. Testing AI Explanation (DentalAIPipeline.explain_image) ---")
    try:
        explanation = DentalAIPipeline.explain_image(test_img)
        print("Explanation status:", explanation.get('status'))
        print("Condition 1:", explanation.get('data', {}).get('issues', [{}])[0].get('condition', 'None'))
        print("SUCCESS: explain_image ran perfectly.\n")
    except Exception as e:
        print(f"FAILED explain_image: {str(e)}")

if __name__ == "__main__":
    run_test()
