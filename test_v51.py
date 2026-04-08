import sys
import os
# Add the project root to sys.path
sys.path.append(r"c:\Users\bharg\AndroidStudioProjects\DRUGDOSAGEAPP")

from api.ai_pipeline import DentalAIPipeline

def test_pipeline():
    test_img = r"c:\Users\bharg\AndroidStudioProjects\DRUGDOSAGEAPP\final_dataset\xray\train\Caries\100.jpg"
    if not os.path.exists(test_img):
        print("Test image not found.")
        return

    print(f"Testing pipeline for: {test_img}")
    result = DentalAIPipeline.analyze_image(test_img)
    print("--- PIPELINE OUTPUT ---")
    print(result)
    print("-----------------------")

if __name__ == "__main__":
    test_pipeline()
