import glob
import os
from pdf2image import convert_from_path
import cv2
import numpy as np

def process_pdf_images(pdf_files):
    """
    Extract images from the PDFs located in the ../Data/PDFs/ directory.
    Converts each page of each PDF to an image and saves it.
    """    
    if not pdf_files:
        print("No PDF files found in the directory.")
        return "No PDFs processed."

    for path in pdf_files:
        print(f"Processing: {path}")
        pdf_name = os.path.splitext(os.path.basename(path))[0]
        output_dir = f'../Output/Images/{pdf_name}'

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        pages = convert_from_path(path, dpi=300)
        
        for i, page in enumerate(pages, start=1):
            open_cv_image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
            height, width, _ = open_cv_image.shape
            print(f"Page {i} -> Width: {width}, Height: {height}")
            
            output_filename = f'{output_dir}/{pdf_name}_page_{i}.jpg'
            cv2.imwrite(output_filename, open_cv_image)
            print(f"Saved {output_filename}")
            
    return output_dir,pdf_name