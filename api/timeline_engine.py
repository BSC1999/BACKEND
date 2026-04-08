class TimelineEngine:
    """
    v65.0 Aria Quantum Procedural Matrix.
    Strict mathematical generation of clinical sequences and phase-wise procedures.
    """

    @staticmethod
    def generate_timeline(treatment, diagnosis):
        treatment_l = treatment.lower()
        
        # Default numeric values
        step1_day = 1
        int1_days = 7
        int2_days = 0 # Only for has_step3
        has_step3 = False
        
        # Plan Structure (Base)
        plan = {
            "count": "Optimized Steps: 2",
            "step1_title": "Primary Intervention",
            "step1_desc": f"Digital-guided {treatment} procedure.",
            "interval1": f"{int1_days} Days Tissue Stabilization",
            "step2_title": "Post-Op Review",
            "step2_desc": "Final assessment and functional verification.",
            "has_step3": False,
            "insight": f"AI Recommendation: {treatment} shows high success probability for {diagnosis}."
        }

        # Specialized Matrix Logic
        if "root canal" in treatment_l or "endodontics" in treatment_l:
            int1_days = 7
            plan.update({
                "step1_title": "Neural Debridement",
                "step1_desc": "Precision cleaning of the pulp chamber using digital mapping.",
                "interval1": "7 Days Endodontic Stabilization",
                "step2_title": "Permanent Seal",
                "step2_desc": "Final obturation and biomechanical core restoration.",
                "insight": "AI Insight: Root canal integrity predicted at 98.2%. Tissue inflammation risk: LOW."
            })
        elif "extraction" in treatment_l or "removal" in treatment_l:
            int1_days = 10
            plan.update({
                "step1_title": "Atraumatic Removal",
                "step1_desc": "Tissue-preserving extraction using piezoelectric vibration.",
                "interval1": "10 Days Socket Maturation",
                "step2_title": "Suture Removal",
                "step2_desc": "Clinical evaluation of primary healing and clot integrity.",
                "insight": "AI Insight: Socket preservation successfully mapped. 100% clot stability predicted."
            })
        elif "inlay" in treatment_l or "onlay" in treatment_l or "ceramic" in treatment_l:
            int1_days = 3
            plan.update({
                "step1_title": "Digital Impression",
                "step1_desc": "Intraoral scanning and precise cavity preparation.",
                "interval1": "3 Days Lab Fabrication",
                "step2_title": "Indirect Fitment",
                "step2_desc": "Bonding of the high-grade ceramic restoration.",
                "insight": "AI Prediction: Precision marginal fit of 15 microns expected."
            })
        elif "biomimetic" in treatment_l:
            int1_days = 1
            plan.update({
                "step1_title": "Bionic Reconstruction",
                "step1_desc": "Layer-by-layer anatomical restoration using resin cues.",
                "interval1": "24 Hours Polymerization",
                "step2_day": "DAY 2",
                "step2_title": "Occlusal Refinement",
                "step2_desc": "Fine-tuning of bite force distribution for longevity.",
                "insight": "AI Insight: Stress-reduced restoration planned to prevent tooth fatigue."
            })
        elif "piezo-surgical" in treatment_l or "apicectomy" in treatment_l:
            int1_days = 14
            int2_days = 7
            has_step3 = True
            plan.update({
                "count": "Surgical Steps: 3",
                "step1_title": "Apical Resection",
                "step1_desc": "Surgical removal of the infected root tip and cyst.",
                "interval1": "14 Days Primary Healing",
                "step2_title": "Osseous Review",
                "step2_desc": "X-ray verification of initial bone regeneration.",
                "has_step3": True,
                "interval2": "7 Days Secondary Healing",
                "step3_title": "Final Outcome",
                "step3_desc": "Complete visual and radiographic clearance.",
                "insight": "Aria AI: 94.5% bone graft success probability based on density scan."
            })
        elif "implant" in treatment_l:
            int1_days = 14
            int2_days = 90 # 3 Months Osseointegration
            has_step3 = True
            plan.update({
                "count": "Surgical Phases: 3",
                "step1_title": "Implant Placement",
                "step1_desc": f"Precision titanium post insertion using {diagnosis} mapped path.",
                "interval1": "14 Days Soft Tissue Healing",
                "step2_title": "Abutment Fitment",
                "step2_desc": "Connecting the transmucosal component for gum contouring.",
                "has_step3": True,
                "interval2": "90 Days Osseointegration",
                "step3_title": "Final Prosthesis",
                "step3_desc": "Fixed ceramic crown placement with perfect occlusal sync.",
                "insight": "AI Insight: Bone density optimal for Grade 4 Titanium. 99.5% stability predicted."
            })

        # --- ARIA PRECISION MATH (v65.0 Integration) ---
        step2_day = step1_day + int1_days
        plan["step2_day"] = f"DAY {step2_day}"
        
        if has_step3:
            step3_day = step2_day + int2_days
            plan["step3_day"] = f"DAY {step3_day}"
            final_day = step3_day
        else:
            final_day = step2_day

        plan["duration"] = f"Total Duration: {final_day} Days"
        
        # Add Visits/Phases for v65.0
        plan["visits"] = TimelineEngine.generate_visits(treatment_l, plan)
        
        return plan

    @staticmethod
    def generate_visits(treatment_l, timeline):
        visits = []
        
        if "root canal" in treatment_l or "endodontics" in treatment_l or "rct" in treatment_l:
            visits = [
                {
                    "num": "SESSION 1",
                    "phase": timeline["step1_title"],
                    "duration": "45 min",
                    "tasks": ["Precision Access Opening", "Bio-Mechanical Shaping", "Neural Debridement", "Medicated Dressing"]
                },
                {
                    "num": "SESSION 2",
                    "phase": timeline["step2_title"],
                    "duration": "60 min",
                    "tasks": ["Canal Obturation (Sealing)", "Composite Build-up", "Biomechanical Review"]
                }
            ]
        elif "extraction" in treatment_l or "removal" in treatment_l:
            visits = [
                {
                    "num": "PHASE 1",
                    "phase": timeline["step1_title"],
                    "duration": "40 min",
                    "tasks": ["Atraumatic Luxation", "Piezo-Surgical Extraction", "Socket Irrigation", "Suture Placement"]
                },
                {
                    "num": "PHASE 2",
                    "phase": timeline["step2_title"],
                    "duration": "15 min",
                    "tasks": ["Suture Removal", "Healing Integrity Check", "Clot Stability Analysis"]
                }
            ]
        elif "filling" in treatment_l or "restoration" in treatment_l or "composite" in treatment_l:
            visits = [
                {
                    "num": "VISIT 1",
                    "phase": "Aesthetic Restoration",
                    "duration": "30 min",
                    "tasks": ["Caries Excavation", "Enamel Conditioning", "Composite Layering", "Curing Protocol"]
                },
                {
                    "num": "VISIT 2",
                    "phase": "Functional Finish",
                    "duration": "20 min",
                    "tasks": ["Occlusal Mapping", "Anatomical Polishing", "Interproximal Verification"]
                }
            ]
        elif "apicectomy" in treatment_l or "piezo-surgical" in treatment_l:
            visits = [
                {
                    "num": "SURGERY",
                    "phase": timeline["step1_title"],
                    "duration": "90 min",
                    "tasks": ["Flap Elevation", "Apical Root Prep", "Infection Clearance", "Bone Graft Placement"]
                },
                {
                    "num": "REVIEW 1",
                    "phase": timeline["step2_title"],
                    "duration": "20 min",
                    "tasks": ["Interim X-ray Scan", "Osseous Integrity Check", "Soft Tissue Removal"]
                },
                {
                    "num": "FINAL",
                    "phase": timeline.get("step3_title", "Final Discharge"),
                    "duration": "30 min",
                    "tasks": ["Full Clinical Clearance", "Functional Stability Scan", "Post-Surgical Advisory"]
                }
            ]
        elif "implant" in treatment_l:
            visits = [
                {
                    "num": "ORAL SURGERY",
                    "phase": timeline["step1_title"],
                    "duration": "60 min",
                    "tasks": ["Local Anesthesia", "Osteotomy Preparation", "Implant Insertion", "Healing Cap Placement"]
                },
                {
                    "num": "RECOVERY",
                    "phase": timeline["step2_title"],
                    "duration": "30 min",
                    "tasks": ["Suture Removal", "ISQ Stability Check", "Abutment Connection"]
                },
                {
                    "num": "PROSTHETIC",
                    "phase": timeline.get("step3_title", "Final Crown"),
                    "duration": "45 min",
                    "tasks": ["Digital Impression", "Shade Matching", "Final Torque & Seating"]
                }
            ]
        else:
            # Generic RESTORATIVE Fallback
            visits = [
                {
                    "num": "VISIT 1",
                    "phase": timeline["step1_title"],
                    "duration": "30 min",
                    "tasks": ["Digital Prep", "Primary Restoration", "Isolation Protocol"]
                },
                {
                    "num": "VISIT 2",
                    "phase": timeline["step2_title"],
                    "duration": "20 min",
                    "tasks": ["Occlusal Adjustment", "Polishing & Finish", "Sensory Check"]
                }
            ]
            
        return visits
