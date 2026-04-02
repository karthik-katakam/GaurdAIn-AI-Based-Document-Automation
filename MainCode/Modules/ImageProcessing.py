import os
import cv2
import numpy as np


def safe_imread(path, flag=cv2.IMREAD_GRAYSCALE):
    img = cv2.imread(path, flag)
    if img is None:
        raise FileNotFoundError(f"[ERROR] Image at '{path}' could not be read.")
    return img


def safe_imwrite(path, image):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    success = cv2.imwrite(path, image)
    if not success:
        raise IOError(f"[ERROR] Failed to write image to '{path}'.")


def process_images(img_grey, output_filename):
    """
    Clean the image:
    - Denoise while preserving text and lines.
    - Enhance contrast without harsh thresholding.

    :param img_grey: Grayscale image array.
    :param output_filename: Path where the processed image should be saved.
    :return: "Done Processing"
    """
    # Step 1: Apply a slight denoising filter to reduce noise but preserve edges
    denoised = cv2.fastNlMeansDenoising(img_grey, h=10, templateWindowSize=7, searchWindowSize=21)

    # Step 2: Slightly enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # Step 3: Save the cleaned output image
    safe_imwrite(output_filename, enhanced)
    print(f"[INFO] Preprocessing Completed: {output_filename}")

    return "Done Processing"