# transcript_pipeline.py

import io
import re
from typing import Dict, Any, Tuple
from pdf2image import convert_from_path

from PIL import Image
import pytesseract


def ocr_image(img: Image.Image) -> str:
    text = pytesseract.image_to_string(img)
    return text


def pdf_to_images(pdf_path: str):
    pages = convert_from_path(pdf_path)
    return pages


def extract_name(ocr_text: str) -> str:
    lines = [l.strip() for l in ocr_text.splitlines() if l.strip()]

    # Look for explicit label
    for i, line in enumerate(lines):
        if "NAME OF THE CANDIDATE" in line.upper():
            if i + 1 < len(lines):
                return clean_name(lines[i + 1])
            return clean_name(line.split(":")[-1])

    # Fallback: first ALL CAPS line with 2–4 words
    for line in lines[:20]:
        words = line.split()
        if line.isupper() and 2 <= len(words) <= 4:
            return clean_name(line)

    return "UNKNOWN"


def clean_name(name: str) -> str:
    tokens = name.split()
    if len(tokens) > 2 and len(tokens[-1]) == 1:
        tokens = tokens[:-1]

    cleaned = " ".join(tokens)
    return cleaned.title()


def extract_gpa(ocr_text: str) -> float | None:
    pattern = r"(CGPA|GPA|CUMULATIVE GRADE POINT AVERAGE)[^\d]*([0-9]+\.[0-9]+)"
    matches = re.findall(pattern, ocr_text, flags=re.IGNORECASE)

    if matches:
        try:
            return float(matches[-1][1])
        except:
            pass

    nums = re.findall(r"\d+\.\d+", ocr_text)
    if nums:
        return float(nums[-1])

    return None


def evaluate_eligibility(gpa: float | None, threshold: float) -> Tuple[str, str]:
    if gpa is None:
        return (
            "GPA NOT FOUND",
            "The system could not find a GPA in this transcript. Please verify manually."
        )

    if gpa >= threshold:
        return (
            "ELIGIBLE",
            f"The student has a GPA of {gpa:.2f}, which is above the threshold of {threshold:.2f}."
        )

    elif gpa >= threshold - 1:
        return (
            "REVIEW RECOMMENDED",
            f"The student has a GPA of {gpa:.2f}. This is slightly below the threshold of {threshold:.2f}. Manual review recommended."
        )

    return (
        "NOT ELIGIBLE",
        f"The student has a GPA of {gpa:.2f}, which is below the threshold of {threshold:.2f}."
    )


def process_transcript(file_path: str, gpa_threshold: float) -> Dict[str, Any]:
    """
    file_path: path string from Gradio (type='filepath')
    """
    if not isinstance(file_path, str):
        raise ValueError(f"Expected file path string, got {type(file_path)}")

    lower = file_path.lower()

    # PDF case
    if lower.endswith(".pdf"):
        images = pdf_to_images(file_path)
        ocr_text = "\n".join(ocr_image(img) for img in images)
        preview_image = images[0]

    # Image case (png/jpg/etc.)
    else:
        img = Image.open(file_path)
        ocr_text = ocr_image(img)
        preview_image = img

    name = extract_name(ocr_text)
    gpa = extract_gpa(ocr_text)
    eligibility, summary = evaluate_eligibility(gpa, gpa_threshold)

    return {
        "name": name,
        "gpa": gpa,
        "eligibility": eligibility,
        "summary": summary,
        "ocr_text": ocr_text,
        "preview_image": preview_image,
    }