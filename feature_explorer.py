import os
import cv2
import numpy as np

def extract_features():
    train_path = r"c:\Users\bharg\AndroidStudioProjects\DRUGDOSAGEAPP\final_dataset\xray\train"
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(12,12))
    
    categories = ["Caries", "Healthy Teeth"]
    
    print("category,filename,ratio,std_dev,norm_dist,h_w_ratio")
    
    for cat in categories:
        cat_path = os.path.join(train_path, cat)
        if not os.path.exists(cat_path): continue
        
        for f in os.listdir(cat_path):
            if not f.endswith(('.jpg', '.jpeg', '.png')): continue
            img_path = os.path.join(cat_path, f)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None: continue
            
            enhanced = clahe.apply(img)
            _, thresh = cv2.threshold(enhanced, 190, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                if cv2.contourArea(cnt) < 700: continue
                x, y, w, h = cv2.boundingRect(cnt)
                roi = enhanced[y:y+h, x:x+w]
                pixels = roi[roi > 0]
                if pixels.size < 100: continue
                
                p5 = np.percentile(pixels, 5)
                p50 = np.median(pixels)
                ratio = p5 / p50 if p50 > 0 else 1.0
                std_dev = np.std(pixels)
                h_w = h / w
                
                M = cv2.moments(cnt)
                if M["m00"] > 0:
                    cX = int(M["m10"] / M["m00"]) - x
                    cY = int(M["m01"] / M["m00"]) - y
                    dark_mask = (roi > 0) & (roi <= p5 * 1.1)
                    dark_coords = np.argwhere(dark_mask)
                    if dark_coords.size > 0:
                        dY, dX = np.mean(dark_coords, axis=0)
                        dist = np.sqrt((dX - cX)**2 + (dY - cY)**2)
                        norm_dist = dist / (max(w, h) / 2)
                        print(f"{cat},{f},{ratio:.3f},{std_dev:.3f},{norm_dist:.3f},{h_w:.3f}")

if __name__ == "__main__":
    extract_features()
