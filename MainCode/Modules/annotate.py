import fitz  # PyMuPDF
import os
from typing import List

def annotate_pdf(input_pdf: str, errors: List[str], warnings: List[str], output_pdf: str):
    """
    Append a blank page to the PDF and annotate it with the provided errors and warnings,
    then save as output_pdf.

    - input_pdf: path to original PDF
    - errors: list of error messages to stamp
    - warnings: list of warning messages to stamp
    - output_pdf: path to write annotated PDF
    """
    doc = fitz.open(input_pdf)
    
    # Add a new blank page at end
    new_page = doc.new_page(-1)  # append at end
    
    # Build annotation text
    parts = []
    if errors:
        parts.append("Validation Errors:")
        parts += [f"- {e}" for e in errors]
        parts.append("")
    if warnings:
        parts.append("Validation Warnings:")
        parts += [f"- {w}" for w in warnings]
    text = "\n".join(parts)

    # Define margins
    margin = 50
    rect = fitz.Rect(
        margin,
        margin,
        new_page.rect.width - margin,
        new_page.rect.height - margin
    )

    # Insert text box on new page in red
    new_page.insert_textbox(
        rect,
        text,
        fontsize=12,
        fontname="helv",
        color=(1, 0, 0),
        align=0  # left align
    )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc.save(output_pdf)
