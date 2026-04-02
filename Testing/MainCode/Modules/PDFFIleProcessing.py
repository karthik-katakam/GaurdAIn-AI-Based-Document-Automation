import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from typing import List

def process_pdf_images(pdf_files: List[str], output_folder: str) -> List[str]:
    """
    Extract images from the given list of PDF files.
    Converts each page of each PDF to an image and saves it to output_folder.

    :param pdf_files: List of paths to PDF files.
    :param output_folder: Directory where images will be saved.
    :return: List of saved image file paths.
    """
    if not pdf_files:
        print("No PDF files provided.")
        return []

    os.makedirs(output_folder, exist_ok=True)
    output_paths: List[str] = []

    for path in pdf_files:
        print(f"Processing: {path}")
        pdf_name = os.path.splitext(os.path.basename(path))[0]
        pages = convert_from_path(path, dpi=300)

        for i, page in enumerate(pages, start=1):
            # Convert PIL image to OpenCV BGR
            open_cv_image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
            height, width, _ = open_cv_image.shape
            print(f"Page {i} -> Width: {width}, Height: {height}")

            output_filename = os.path.join(output_folder, f"{pdf_name}_page_{i}.jpg")
            cv2.imwrite(output_filename, open_cv_image)
            print(f"Saved {output_filename}")
            output_paths.append(output_filename)

    return output_paths
