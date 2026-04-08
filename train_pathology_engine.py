import os
import cv2
import numpy as np
import json

def profile_xrays():
    dataset_path = r"c:\Users\bharg\AndroidStudioProjects\DRUGDOSAGEAPP\final_dataset\xray\train"
    categories = {"Caries": "caries", "Healthy Teeth": "healthy", "Impacted teeth": "impacted"}
    raw_data = {k: [] for k in categories.values()}
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(16,16))

    for cat_name, key in categories.items():
        cat_path = os.path.join(dataset_path, cat_name)
        if not os.path.exists(cat_path): continue
        for f in os.listdir(cat_path)[:100]:
            img = cv2.imread(os.path.join(cat_path, f), cv2.IMREAD_GRAYSCALE)
            if img is None: continue
            enhanced = clahe.apply(img)
            _, thresh = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            icrs = []; aspects = []
            for cnt in contours:
                if cv2.contourArea(cnt) < 500: continue
                x,y,w,h = cv2.boundingRect(cnt)
                roi = enhanced[y:y+h, x:x+w]
                pixels = roi[roi > 0]
                if pixels.size > 0:
                    icrs.append(np.percentile(pixels, 5) / np.mean(pixels))
                    aspects.append(w/h)

            if icrs:
                raw_data[key].append({"icr": np.min(icrs), "aspect": np.max(aspects)})

    # Calculate midpoints for 100% separation attempt
    h_icr = [d['icr'] for d in raw_data['healthy']]
    c_icr = [d['icr'] for d in raw_data['caries']]
    
    # We want a threshold BELOW which is Caries, but ABOVE which is Healthy.
    # To avoid False Positives (Healthy as Caries), the threshold MUST BE < min(Healthy)
    best_caries_icr = min(h_icr) - 0.05 if h_icr else 0.5
    
    h_asp = [d['aspect'] for d in raw_data['healthy']]
    i_asp = [d['aspect'] for d in raw_data['impacted']]
    best_impacted_asp = (max(h_asp) + min(i_asp)) / 2 if h_asp and i_asp else 5.2

    print(f"Healthy ICR Min: {min(h_icr):.2f}, Caries ICR Min: {min(c_icr):.2f}")
    print(f"Target Threshold: {best_caries_icr:.2f}")

    optimized = {
        "caries_icr_limit": round(best_caries_icr, 2),
        "impacted_aspect_limit": round(best_impacted_asp, 2)
    }

    with open("optimized_params.json", "w") as jf:
        json.dump(optimized, jf)

if __name__ == "__main__":
    profile_xrays()
