# AI-Powered Transcript Parsing and GPA-Based Eligibility Assessment

📄 **Automated Transcript Analysis using OCR, LayoutLMv3, and Rule-Based Eligibility Logic**

This repository contains the full implementation, experiments, and research artifacts for an AI-assisted admissions support system that automatically extracts GPA and subject information from academic transcripts and evaluates program-specific eligibility.

The project was developed as a **research-oriented capstone** and is designed to operate under **strict privacy (FERPA) constraints**, using only local processing and open-source tools.

---

##  Project Overview

University admissions workflows still rely heavily on manual transcript evaluation. Admissions officers must visually inspect scanned PDFs or images, identify GPA values, and verify eligibility criteria. This process is time-consuming, error-prone, and difficult to scale.

This project proposes a **hybrid Document AI pipeline** that combines:
- Local Optical Character Recognition (OCR)
- Layout-aware deep learning (LayoutLMv3)
- Rule-based GPA extraction and eligibility reasoning
- A transparent, human-in-the-loop user interface

The system is intended as a **decision-support tool**, not an autonomous decision-maker.

---

##  System Architecture

The pipeline consists of the following stages:

1. **Input Handling**
   - PDF / JPG / PNG transcripts
   - PDF pages converted to images

2. **OCR (FERPA-safe)**
   - Local Tesseract OCR
   - No third-party cloud APIs

3. **Layout-Aware Modeling**
   - Fine-tuned LayoutLMv3 for token classification
   - Entities: NAME, GPA, SUBJECT

4. **Hybrid GPA Extraction**
   - Regex + keyword-based GPA detection
   - Confidence scoring (HIGH / MEDIUM / LOW)

5. **Eligibility Decision Engine**
   - Program-specific GPA thresholds
   - Subject prerequisite checks
   - Outputs: Eligible / Not Eligible / Review Recommended

6. **User Interface**
   - Gradio-based web UI
   - Full OCR text exposed for transparency

 Architecture diagrams and workflow figures are included in the paper and `/images` directory.

---

##  Repository Structure

```text
.
├── images/                         # Architecture diagrams and UI screenshots
│   ├── End_to_end_Architecture.jpg
│   ├── layoutlmv3_training_pipeline.jpg
│   ├── ocr_gpa_flow.jpg
│   ├── eligibility_flow.jpg
│   ├── ui_overview.png
│   └── ui_results.png
│
├── notebooks/
│   └── AI_Automated_Transcript_Eligibility_UI.ipynb
│
├── synthetic_data/
│   └── synthetic_transcript_generator.py
│
├── paper/
│   └── capstone_final.pdf
│
├── requirements.txt
└── README.md
