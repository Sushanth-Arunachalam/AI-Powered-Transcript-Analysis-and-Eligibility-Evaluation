import os

# This MUST be set before importing gradio
os.environ["GRADIO_SKIP_URL_CHECK"] = "1"

import gradio as gr
from transcript_pipeline import process_transcript


DEFAULT_THRESHOLD = 8.0

def analyze_transcript(file, threshold):
    if file is None:
        return None, "No file uploaded.", "", "", "", ""

    result = process_transcript(file, threshold)

    name = result["name"]
    gpa = result["gpa"]
    eligibility = result["eligibility"]
    summary = result["summary"]
    ocr_text = result["ocr_text"]
    preview_image = result["preview_image"]

    gpa_display = "Not found" if gpa is None else f"{gpa:.2f}"

    return (
        preview_image,            # Image preview
        f"Name: {name}",          # Name output
        f"GPA: {gpa_display}",    # GPA output
        f"Eligibility: {eligibility}",  # Eligibility label
        summary,                  # Summary sentence
        ocr_text                  # Full OCR text
    )


with gr.Blocks(title="Transcript Eligibility Checker") as demo:

    gr.Markdown("""
    # 📄 Transcript Eligibility Checker
    Upload a transcript (PDF/JPG/PNG).  
    The system extracts GPA and determines eligibility automatically.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
            label="Upload Transcript",
            file_types=[".pdf", ".png", ".jpg", ".jpeg"],
            type="filepath"   # <-- IMPORTANT
            )

            threshold_input = gr.Slider(
                minimum=0.0,
                maximum=10.0,
                value=DEFAULT_THRESHOLD,
                step=0.1,
                label="GPA Threshold"
            )
            analyze_button = gr.Button("Analyze Transcript")

        with gr.Column(scale=2):
            preview_output = gr.Image(label="Transcript Preview")
            name_output = gr.Textbox(label="Extracted Name")
            gpa_output = gr.Textbox(label="Extracted GPA")
            eligibility_output = gr.Textbox(label="Eligibility Result")
            summary_output = gr.Textbox(label="Summary", lines=3)

    ocr_output = gr.Textbox(
        label="OCR Text (for manual review)",
        lines=12
    )

    analyze_button.click(
        fn=analyze_transcript,
        inputs=[file_input, threshold_input],
        outputs=[
            preview_output,
            name_output,
            gpa_output,
            eligibility_output,
            summary_output,
            ocr_output,
        ]
    )


demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=True
)
