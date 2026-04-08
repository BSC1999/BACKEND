import os
import cv2
import numpy as np

def deep_analysis():
    test_path = r"c:\Users\bharg\AndroidStudioProjects\DRUGDOSAGEAPP\final_dataset\xray\train"
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(16,16))
    
    for cat in ["Caries", "Healthy Teeth"]:
        path = os.path.join(test_path, cat)
        if not os.path.exists(path): continue
        edrs = []
        for f in os.listdir(path)[:50]:
            img = cv2.imread(os.path.join(path, f), cv2.IMREAD_GRAYSCALE)
            if img is None: continue
            enhanced = clahe.apply(img)
            _, thresh = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                if cv2.contourArea(cnt) < 500: continue
                x,y,w,h = cv2.boundingRect(cnt)
                roi = enhanced[y:y+h, x:x+w]
                pixels = roi[roi > 0]
                if pixels.size > 200:
                    edrs.append(np.percentile(pixels, 15) / np.percentile(pixels, 85))
        
        if edrs:
            print(f"{cat} EDR - Min: {min(edrs):.3f}, Max: {max(edrs):.3f}, Mean: {np.mean(edrs):.3f}")

if __name__ == "__main__":
    deep_analysis()
