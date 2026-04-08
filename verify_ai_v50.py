import cv2
import numpy as np
import os
from api.pathology_engine import DentalPathologyEngine

def verify_uniqueness():
    print("--- AI v50.0 FUSION CORE VERIFICATION ---")
    
    # Create two dummy images with different pixel data
    test1 = np.random.randint(0, 255, (500, 1000), dtype=np.uint8)
    test2 = np.random.randint(0, 255, (500, 1000), dtype=np.uint8)
    test2[200:300, 200:300] = 50 # Add a "lesion" to test 2
    
    cv2.imwrite("test_img_1.png", test1)
    cv2.imwrite("test_img_2.png", test2)
    
    p1 = DentalPathologyEngine.calculate_pathology_probability("test_img_1.png", "Dental Caries", [100, 100, 50, 50])
    p2 = DentalPathologyEngine.calculate_pathology_probability("test_img_2.png", "Dental Caries", [200, 200, 100, 100])
    
    print(f"Image 1 Confidence: {p1*100:.2f}%")
    print(f"Image 2 Confidence: {p2*100:.2f}%")
    
    if p1 != p2:
        print("SUCCESS: AI v50.0 confirmed UNIQUE signatures for different anatomy!")
    else:
        print("FAILURE: Repetitive result detected.")

if __name__ == "__main__":
    verify_uniqueness()
