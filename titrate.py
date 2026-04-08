import os
import cv2
import numpy as np

def titrate():
    test_path = r"c:\Users\bharg\AndroidStudioProjects\DRUGDOSAGEAPP\final_dataset\xray\train"
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(16,16))
    
    stats = {"Caries": [], "Healthy": []}
    
    for cat in ["Caries", "Healthy Teeth"]:
        path = os.path.join(test_path, cat)
        if not os.path.exists(path): continue
        key = "Caries" if cat == "Caries" else "Healthy"
        
        for f in os.listdir(path)[:50]:
            img = cv2.imread(os.path.join(path, f), cv2.IMREAD_GRAYSCALE)
            if img is None: continue
            enhanced = clahe.apply(img)
            _, thresh = cv2.threshold(enhanced, 195, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                if cv2.contourArea(cnt) < 1000: continue
                x,y,w,h = cv2.boundingRect(cnt)
                roi = enhanced[y:y+h, x:x+w]
                mid = w // 2
                diff = cv2.absdiff(roi[:, :mid], cv2.flip(roi[:, w-mid:w], 1))
                sym = np.mean(diff)
                
                sobelx = cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=3)
                sobely = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)
                flux = np.std(np.sqrt(sobelx**2 + sobely**2))
                
                stats[key].append((sym, flux))

    if stats["Healthy"]:
        max_h_sym = max([s[0] for s in stats["Healthy"]])
        max_h_flux = max([s[1] for s in stats["Healthy"]])
        print(f"Healthy MAX - Symmetry: {max_h_sym:.1f}, Flux: {max_h_flux:.1f}")
    if stats["Caries"]:
        min_c_sym = min([s[0] for s in stats["Caries"]])
        min_c_flux = min([s[1] for s in stats["Caries"]])
        print(f"Caries MIN - Symmetry: {min_c_sym:.1f}, Flux: {min_c_flux:.1f}")

if __name__ == "__main__":
    titrate()
