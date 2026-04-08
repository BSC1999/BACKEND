import os
import time
import numpy as np
import cv2
import random
from .vision_model import QuantumVisionModel
from .pathology_engine import DentalPathologyEngine
from PIL import Image, ImageOps, ImageFilter

class DentalAIPipeline:
    """
    v21.0 Obsidian Pipeline (Medical-Fidelity).
    Orchestrates Verification -> Pathology -> Treatment Mapping.
    """

    @staticmethod
    def analyze_image(file_path: str) -> str:
        """
        v22.0 Multi-Spectral Report Generator.
        Provides high-fidelity text diagnostics.
        """
        try:
            nature = QuantumVisionModel.predict_image_nature(file_path)
            if nature.get("label") not in ["DENTAL_XRAY", "INTRAORAL_PHOTO"]:
                return "VERIFICATION FAILED: Absolute Non-Dental Rejection.\nCaries: 0%\nPeriapical: 0%\nImpacted: 0%"

            data = DentalPathologyEngine.analyze_xray(file_path) if nature["label"] == "DENTAL_XRAY" else DentalPathologyEngine.analyze_intraoral(file_path)
            
            # Extract top conditions for the report
            metrics = {"Caries": 5.0, "Impacted": 5.0, "Periapical": 5.0} # Base floor
            for issue in data.get("issues", []):
                cond = issue.get("condition", "")
                prob = round(issue.get("probability", 0.0) * 100, 1)
                if "Caries" in cond: metrics["Caries"] = max(metrics["Caries"], prob)
                elif "Impacted" in cond: metrics["Impacted"] = max(metrics["Impacted"], prob)
                elif "Periapical" in cond: metrics["Periapical"] = max(metrics["Periapical"], prob)

            return (f"AI Engine: Aria Ground Truth v61.0\n"
                    f"Classification: {nature['label']}\n"
                    f"Neural Caries Accuracy: {metrics['Caries']}%\n"
                    f"Neural Periapical Logic: {metrics['Periapical']}%\n"
                    f"Neural Impacted Precision: {metrics['Impacted']}%")
        except Exception as e:
            return f"DeepScan Offline: {str(e)}"

    @staticmethod
    def explain_image(file_path: str) -> dict:
        """
        Multi-stage diagnostic handoff for Android UI marking and Treatment screens.
        """
        if not os.path.exists(file_path):
            return {"status": "ERROR", "reason": "File not found"}

        try:
            # 1. Verification
            nature = QuantumVisionModel.predict_image_nature(file_path)
            if nature.get("label") not in ["DENTAL_XRAY", "INTRAORAL_PHOTO"]:
                return {"status": "REJECTED", "reason": "Non-dental image detected"}

            # 2. XAI Analysis
            diag_data = DentalPathologyEngine.analyze_xray(file_path) if nature["label"] == "DENTAL_XRAY" else DentalPathologyEngine.analyze_intraoral(file_path)
            
            # 3. Treatment Overlay Injection (Primary vs Alternative - App Parity)
            for issue in diag_data.get("issues", []):
                cond = issue.get("condition", "")
                
                # Dynamic Dual-Path Matrix (Standardized)
                if "Caries" in cond:
                    if issue["severity"] == "HIGH":
                        issue["best_treatment"] = "Root Canal Therapy"
                        issue["alternative_treatment"] = "Tooth Extraction"
                    else:
                        issue["best_treatment"] = "Dental Filling"
                        issue["alternative_treatment"] = "Root Canal Therapy"
                    issue["suggestions"] = [issue["best_treatment"], issue["alternative_treatment"], "Crown"]
                elif "Periapical" in cond:
                    issue["best_treatment"] = "Root Canal Therapy"
                    issue["alternative_treatment"] = "Tooth Extraction"
                    issue["suggestions"] = [issue["best_treatment"], issue["alternative_treatment"], "Antibiotics"]
                elif "Impacted" in cond:
                    issue["best_treatment"] = "Tooth Extraction"
                    issue["alternative_treatment"] = "Orthodontic Exposure"
                    issue["suggestions"] = [issue["best_treatment"], issue["alternative_treatment"], "Observation"]
                else:
                    issue["best_treatment"] = "Dental Consultation"
                    issue["alternative_treatment"] = "Diagnostic Scan"
                    issue["suggestions"] = ["General Consultation"]
                
                # Mawa, ensure both primary and alternative are passed for UI mapping
                issue["treatment"] = issue["best_treatment"] 
                issue["secondary_treatment"] = issue["alternative_treatment"]
                issue["timeline"] = "Multi-Session Protocol" if "Root Canal" in issue["best_treatment"] else "Standard Procedure"

            return {
                "status": "SUCCESS",
                "classification": nature["label"],
                "data": diag_data,
                "metrics": nature.get("metrics")
            }

        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

    # Legacy methods kept for class structure but not used by main pipeline
    @staticmethod
    def preprocess_image(image: Image): pass
    @staticmethod
    def model1_image_type_classifier(*args): pass
    @staticmethod
    def model2_disease_prediction(*args): pass
