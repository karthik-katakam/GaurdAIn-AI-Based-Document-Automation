# import glob
# import json
# import cv2
# from pathlib import Path

# import PDFFIleProcessing
# import ImageProcessing
# import ImageSegmentation
# import TextExtraction
# import Tabledataextraction
# import CheckboxUpdated
# from validators import validate_report
# from annotate import annotate_pdf

# def main_pipeline():
#     # 1) PDF → Images
#     images_dir = Path('../Output/Images')
#     images_dir.mkdir(parents=True, exist_ok=True)
#     pdf_list = glob.glob('../Data/PDF/11800_grdnshp_ez_accting.pdf')
#     pdf_pages = PDFFIleProcessing.process_pdf_images(pdf_list)

#     # 2) Preprocess images
#     pre_dir = Path('../Output/Preprocessed_Images')
#     pre_dir.mkdir(parents=True, exist_ok=True)
#     prepped = []
#     for page in pdf_pages:
#         img = cv2.imread(page)
#         if img is None:
#             print(f"[!] Failed to load {page}")
#             continue
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         out_path = pre_dir / (Path(page).stem + '.png')
#         ImageProcessing.process_images(gray, str(out_path))
#         prepped.append(str(out_path))

#     # 3) Segment images
#     csv_master = '../Output/Processed_CSV/11800_grdnshp_ez_accting.csv'
#     seg_root = Path('../Output/Segmented_Images')
#     seg_root.mkdir(parents=True, exist_ok=True)
#     ImageSegmentation.segment_images_from_master_csv(
#         image_dir=str(pre_dir),
#         csv_path=csv_master,
#         output_dir=str(seg_root)
#     )

#     # 4) OCR text
#     text_patches = glob.glob(str(seg_root / '*' / 'SegmentedPatches' / '*.jpg'))
#     TextExtraction.recognize_text(text_patches)
#     json_path = '../Output/JSON/ExtractedText.json'

#     # 5) Table extraction
#     for subdir in seg_root.iterdir():
#         table_folder = subdir / 'SegmentedPatches'
#         if table_folder.exists():
#             Tabledataextraction.extract_table(
#                 image_folder=str(table_folder),
#                 output_json_path=json_path
#             )

#     # 6) Checkbox extraction
#     checkbox_paths = glob.glob(
#         '../Output/Segmented_Images/*/SegmentedPatches/Checkbox*.jpg',
#         recursive=True
#     )
#     CheckboxUpdated.extract_all_checkboxes(
#         image_paths=checkbox_paths,
#         json_path=json_path
#     )

#     # 7) Load extracted JSON
#     with open(json_path, 'r', encoding='utf-8') as f:
#         extracted = json.load(f)

#     # 8) Validate
#     validation = validate_report(extracted)

#     # 9) Print results
#     print("\n=== Validation Errors ===")
#     for err in validation["errors"]:
#         print("  -", err)
#     print("\n=== Validation Warnings ===")
#     for w in validation["warnings"]:
#         print("  -", w)

#     input_pdf  = "../Data/PDF/11800_grdnshp_ez_accting.pdf"
#     output_pdf = "../Output/Annotated/11800_grdnshp_ez_accting_validated.pdf"

#     annotate_pdf(input_pdf, validation["errors"], validation["warnings"], output_pdf)
#     print(f"Annotated PDF written to {output_pdf}")

#     return {
#         'pdf_pages': pdf_pages,
#         'preprocessed': prepped,
#         'segmented_root': str(seg_root),
#         'json_path': json_path,
#         'validation': validation
#     }

# if __name__ == '__main__':
#     results = main_pipeline()
#     print("\nPipeline executed successfully!")
#     for k, v in results.items():
#         print(f"{k}: {v}")

import glob
import json
import cv2
from pathlib import Path

import PDFFIleProcessing
import ImageProcessing
import ImageSegmentation
import TextExtraction
import Tabledataextraction
import CheckboxUpdated
from validators import validate_report
from annotate import annotate_pdf

def main_pipeline(input_pdf_path: str, output_dir: str) -> dict:
    """
    Runs the PDF processing pipeline.

    :param input_pdf_path: Path to the input PDF file.
    :param output_dir: Directory where all outputs will be saved.
    :return: {
        "json": {"extracted": ..., "validation": ...},
        "pdf_path": "<path_to_annotated_pdf>"
    }
    """
    base = Path(output_dir)
    images_dir = base / "Images"
    pre_dir = base / "Preprocessed_Images"
    processed_csv = base / "Processed_CSV"
    seg_root = base / "Segmented_Images"
    json_dir = base / "JSON"
    annotated_dir = base / "Annotated"

    # Create directories
    for d in (images_dir, pre_dir, processed_csv, seg_root, json_dir, annotated_dir):
        d.mkdir(parents=True, exist_ok=True)

    stem = Path(input_pdf_path).stem

    # 1) PDF → Images
    pdf_pages = PDFFIleProcessing.process_pdf_images(
        [input_pdf_path],
        output_folder=str(images_dir)
    )

    # 2) Preprocess images
    prepped = []
    for page_path in pdf_pages:
        img = cv2.imread(page_path)
        if img is None:
            print(f"[!] Failed to load {page_path}")
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        out_path = pre_dir / f"{Path(page_path).stem}.png"
        ImageProcessing.process_images(gray, str(out_path))
        prepped.append(str(out_path))

    # 3) Segment images
    csv_master = processed_csv / f"{stem}.csv"
    ImageSegmentation.segment_images_from_master_csv(
        image_dir=str(pre_dir),
        csv_path=str(csv_master),
        output_dir=str(seg_root)
    )

    # 4) OCR text
    text_patches = glob.glob(str(seg_root / "*" / "SegmentedPatches" / "*.png"))
    print(text_patches)
    json_path = json_dir / f"{stem}_ExtractedText.json"
    TextExtraction.recognize_text(text_patches,json_path)
    # json_path = json_dir / f"{stem}_ExtractedText1.json"


    # 5) Table extraction
    for subdir in seg_root.iterdir():
        table_folder = subdir / "SegmentedPatches"
        print(table_folder)
        if table_folder.exists():
            Tabledataextraction.extract_table(
                image_folder=str(table_folder),
                output_json_path=str(json_path)
            )

    # 6) Checkbox extraction
    checkbox_paths = glob.glob(
        str(seg_root / "*" / "SegmentedPatches" / "Checkbox*.png")
    )
    CheckboxUpdated.extract_all_checkboxes(
        image_paths=checkbox_paths,
        json_path=str(json_path)
    )

    # 7) Load & validate JSON
    with open(json_path, "r", encoding="utf-8") as f:
        extracted = json.load(f)
    validation = validate_report(extracted)

    # 8) Annotate PDF
    annotated_pdf = annotated_dir / f"{stem}_validated.pdf"
    annotate_pdf(
        input_pdf_path,
        validation["errors"],
        validation["warnings"],
        str(annotated_pdf)
    )

    return {
        "json": {
            "extracted": extracted,
            "validation": validation
        },
        "pdf_path": str(annotated_pdf)
    }
