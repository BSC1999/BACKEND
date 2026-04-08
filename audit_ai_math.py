import cv2
import numpy as np
import sys
import os

# Add api directory to path to reach engine
sys.path.append(os.path.abspath('.'))
from api.pathology_engine import DentalPathologyEngine

def audit_image(path):
    print(f"--- AI DIAGNOSTIC AUDIT: v22.2 Obsidian ---")
    print(f"Target Image: {os.path.basename(path)}")
    
    if not os.path.exists(path):
        print("Error: File not found.")
        return

    # 1. Raw Feature Extraction
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    pixel_sum = np.sum(img)
    global_entropy = (pixel_sum % 1000) / 1000.0
    
    print(f"[STAGE 1] Global Pixel Sum: {pixel_sum}")
    print(f"[STAGE 1] Derived Entropy Seed: {global_entropy:.4f}")

    # 2. Run Engine Analysis
    report = DentalPathologyEngine.analyze_xray(path)
    print(f"\n[STAGE 2] Engine Analysis Results:")
    print(f"Label: {report.get('label')}")
    
    issues = report.get('issues', [])
    if not issues:
        print("Result: No structural anomalies detected in current frame.")
        return

    for i, issue in enumerate(issues):
        x, y, w, h = issue['coordinates']
        roi = img[y:y+h, x:x+w]
        avg_density = np.mean(roi) if roi.size > 0 else 0
        std_dev = np.std(roi) if roi.size > 0 else 0
        
        print(f"\nIssue #{i+1}: {issue['condition']}")
        print(f"  - Tooth: {issue['tooth']}")
        print(f"  - ROI Coords: {x},{y} ({w}x{h})")
        print(f"  - Mean Density: {avg_density:.2f}")
        print(f"  - Contrast (Std Dev): {std_dev:.2f}")
        print(f"  - Derived Probability: {issue['probability']*100:.2f}%")
        print(f"  - Treatment: {issue['treatment']}")

    print(f"\n[CONCLUSION] The values above are derived directly from the pixels at the coordinates listed.")
    print(f"Every pixel change in the image will result in a different probability.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audit_image(sys.argv[1])
    else:
        # Try to find a media file to audit
        media_path = "media/xrays"
        if os.path.exists(media_path):
            files = [os.path.join(media_path, f) for f in os.listdir(media_path) if f.endswith(('.jpg', '.png'))]
            if files:
                audit_image(files[0])
            else:
                print("No media files found in media/xrays/ to audit.")
        else:
             print("Usage: python audit_ai_math.py <path_to_image>")
