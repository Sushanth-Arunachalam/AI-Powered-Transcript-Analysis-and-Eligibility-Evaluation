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

Dataset and Annotation
Real Transcripts

No public transcript datasets were used (FERPA).

A private dataset of 9 transcript pages was manually curated.

All personally identifiable information was removed.

Annotation

Tool: Label Studio

Labeling scheme: BIO tagging

B-NAME, I-NAME

B-GPA, I-GPA

B-SUBJECT, I-SUBJECT

O

GPA appears explicitly in only 3 pages, resulting in extreme class imbalance.

LayoutLMv3 Training

Model: LayoutLMv3 (Hugging Face)

Task: Token classification (NER-style)

Epochs: 10

Loss: Cross-entropy

Training loss: ~0.89 → ~0.08

Observations

NAME and SUBJECT entities learned reasonably well

GPA extraction unreliable due to data scarcity

OCR-token misalignment affected GPA labeling

Design decision:
LayoutLMv3 retained as a research and structural component, not the sole production extractor.

OCR-Based GPA Extraction (Production Pipeline)

The production system uses a robust OCR + rules approach:

Steps

Run local Tesseract OCR

Detect GPA-related keywords

Extract numeric candidates via regex

Filter candidates by valid GPA range

Assign confidence level

Confidence Levels

HIGH: Clear keyword + valid numeric match

MEDIUM: Keyword present, multiple numeric candidates

LOW: Weak keyword or noisy OCR → triggers manual review

GPA extraction accuracy on tested transcripts: ~95%

Eligibility Decision Engine

Eligibility rules are configurable per program.

Program	Minimum GPA	Subject Requirement
General Admission	8.0	None
Computer Science	8.2	Math / CS keywords
Data Science	8.3	Statistics-related keywords
Decision Outputs

Eligible

Not Eligible

Review Recommended (borderline / ambiguous)

Each decision includes a human-readable explanation.

Synthetic Transcript Generator

To address data scarcity, a synthetic transcript generator was implemented using PIL:

Randomized student names

Randomized subjects, grades, GPA

Layout variability (spacing, font size, GPA position)

Optional noise / blur for realism

Automatic ground-truth export (bounding boxes + labels)

Currently used as:

Proof-of-concept

Future training and augmentation strategy

User Interface

Built using Gradio.

Features

Upload transcript (PDF / image)

Select program

Adjust GPA threshold

View transcript preview

Extracted GPA + confidence

Eligibility decision + explanation

Full OCR text for verification

Designed explicitly for transparency and human oversight.

Evaluation Strategy

Due to limited real data:

Qualitative evaluation

Task-level metrics

Ablation study

Ablation Results

OCR-only: Reliable GPA, no structure

LayoutLMv3-only: Structure learned, GPA unreliable

Hybrid system: Best overall performance

Ethics and Privacy

Fully FERPA-conscious design

No cloud OCR or third-party APIs

Local inference only

Human-in-the-loop decision support

Conservative handling of ambiguity
