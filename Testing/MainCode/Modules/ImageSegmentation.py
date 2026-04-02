import os
import cv2
import pandas as pd


def segment_images_from_master_csv(
    image_dir: str,
    csv_path: str,
    output_dir: str,
    image_extension: str = ".png"
) -> str:
    """
    Segment images based on annotations in a CSV.

    :param image_dir: Directory containing preprocessed images.
    :param csv_path: Path to the CSV with columns ['annotation_id','xmin','ymin','xmax','ymax','label'].
    :param output_dir: Directory to write segmented patches. Will create subfolders per annotation.
    :param image_extension: File extension of preprocessed images (e.g. '.png' or '.jpg').
    :return: Completion message.
    """
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"[!] CSV not found: {csv_path}")
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    grouped = df.groupby("annotation_id")

    for annotation_id, group in grouped:
        image_filename = f"{annotation_id}{image_extension}"
        image_path = os.path.join(image_dir, image_filename)
        if not os.path.isfile(image_path):
            print(f"[!] Skipping: {annotation_id} image not found at {image_path}")
            continue

        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None:
            print(f"[!] Failed to load image: {image_path}")
            continue

        save_root = os.path.join(output_dir, annotation_id, "SegmentedPatches")
        os.makedirs(save_root, exist_ok=True)

        for idx, row in group.iterrows():
            try:
                x1, y1, x2, y2 = map(int, (
                    row['xmin'], row['ymin'], row['xmax'], row['ymax']
                ))
                label = str(row['label']).replace(" ", "_").replace("/", "_")

                patch = img[y1:y2, x1:x2]
                gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(
                    gray, 0, 255,
                    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
                )

                patch_name = f"{label}_{idx}{image_extension}"
                patch_path = os.path.join(save_root, patch_name)
                cv2.imwrite(patch_path, binary)
            except Exception as e:
                print(f"[!] Error cropping {annotation_id} row {idx}: {e}")

        print(f"[✓] Done segmenting {annotation_id}")

    return "Segmentation completed for all pages."